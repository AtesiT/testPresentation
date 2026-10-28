"""Воспроизводимый расчётный пайплайн для всех презентаций.

Шаги (запускаются по порядку, лишние пропускаются, если артефакт уже есть):
    python3 presentation/variants/pipeline.py all

Результаты: work/*.json, work/data.npy, work/cache/fields.npz
Снимок метрик для дека: presentation/variants/metrics.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / 'work'
WORK.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT / 'work'))

C_CGS = 2.99792458e10
GPA, KJ = 1e10, 1e10


# ------------------------------------------------------------------ данные
def build_data(force=False):
    out = WORK / 'data.npy'
    if out.exists() and not force:
        return np.load(out)
    import glob
    files = sorted(glob.glob(str(ROOT / 'Материалы к хакатону' / 'Obl*.txt')))
    arrs = [np.loadtxt(f, comments='#') for f in files]
    arr = np.concatenate(arrs).astype(np.float64)
    np.save(out, arr)
    print('data:', arr.shape)
    return arr


# ------------------------------------------------------------------ baseline
def build_baseline():
    import glob
    from scipy.interpolate import RegularGridInterpolator
    regs = []
    for f in sorted(glob.glob(str(ROOT / 'Материалы к хакатону' / 'Obl*.txt'))):
        d = np.loadtxt(f, comments='#')
        lr, lt = np.log10(d[:, 0]), np.log10(d[:, 1])
        ur, ut = np.unique(lr), np.unique(lt)
        gP = d[:, 2].reshape(len(ut), len(ur))
        ge = d[:, 3].reshape(len(ut), len(ur))
        regs.append(dict(lr=ur, lt=ut,
                         iP=RegularGridInterpolator((ut, ur), np.log10(gP), bounds_error=False),
                         ie=RegularGridInterpolator((ut, ur), ge, bounds_error=False)))
    return regs


def query(regs, lrq, ltq):
    lrq = np.asarray(lrq, dtype=float)
    ltq = np.asarray(ltq, dtype=float)
    outP = np.full(lrq.shape, np.nan)
    oute = np.full(lrq.shape, np.nan)
    for r in regs:
        m = ((lrq >= r['lr'][0] - 1e-9) & (lrq <= r['lr'][-1] + 1e-9) &
             (ltq >= r['lt'][0] - 1e-9) & (ltq <= r['lt'][-1] + 1e-9) & np.isnan(outP))
        if m.any():
            pts = np.stack([ltq[m], lrq[m]], 1)
            outP[m] = r['iP'](pts)
            oute[m] = r['ie'](pts)
    return outP, oute


# ------------------------------------------------------------------ физика
EPS_CV_REL = 1e-6


def sound_speed(dP_drho, dP_dT, de_dT, rho, T):
    dpdr, dpdt, cv = dP_drho * GPA, dP_dT * GPA, de_dT * KJ
    degenerate = ~(np.abs(cv) > EPS_CV_REL * np.nanmedian(np.abs(cv)))
    cs2 = np.full_like(dpdr, np.nan, dtype=float)
    ok = ~degenerate & np.isfinite(dpdr) & np.isfinite(dpdt) & np.isfinite(cv)
    cs2[ok] = dpdr[ok] + T[ok] * dpdt[ok] ** 2 / (rho[ok] ** 2 * cv[ok])
    return cs2


def violations(dP_drho, dP_dT, de_dT, rho, T):
    cs2 = sound_speed(dP_drho, dP_dT, de_dT, rho, T)
    cs = np.sqrt(np.clip(cs2, 0, None))
    v = dict(stab=~(dP_drho > 0), cap=~(de_dT > 0), cs2_neg=~(cs2 > 0), cs_light=~(cs < C_CGS))
    any_v = v['stab'] | v['cap'] | v['cs2_neg'] | v['cs_light']
    return dict(cs2=cs2, cs=cs, **{f'{k}_pct': float(100 * np.nanmean(m)) for k, m in v.items()},
                any_=float(100 * np.nanmean(any_v)),
                cs_over_c_med=float(np.nanmedian(cs / C_CGS)),
                cs_med=float(np.nanmedian(cs) / 1e5),
                dP_drho_min=float(np.nanmin(dP_drho)), de_dT_min=float(np.nanmin(de_dT)))


# ------------------------------------------------------------------ сеть
def net_class():
    import torch.nn as nn

    class EOSNet(nn.Module):
        def __init__(self, width=128):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(2, width), nn.Tanh(),
                nn.Linear(width, width), nn.Tanh(),
                nn.Linear(width, width // 2), nn.Tanh(),
                nn.Linear(width // 2, 2))
        def forward(self, x):
            return self.net(x)

    return EOSNet


NORM = json.loads((ROOT / 'normalization.json').read_text())
LR0, LR1 = NORM['inputs']['log_rho']['min'], NORM['inputs']['log_rho']['max']
LT0, LT1 = NORM['inputs']['log_T']['min'], NORM['inputs']['log_T']['max']
P0, P1 = NORM['outputs']['P']['min'], NORM['outputs']['P']['max']
E0, E1 = NORM['outputs']['e']['min'], NORM['outputs']['e']['max']
LP0, LP1 = np.log10(P0), np.log10(P1)


def encode(rho, T):
    return np.stack([(np.log10(rho) - LR0) / (LR1 - LR0),
                     (np.log10(T) - LT0) / (LT1 - LT0)], -1)


def load_net(path, width=128):
    import torch
    net = net_class()(width)
    net.load_state_dict(torch.load(path, map_location='cpu'))
    net.eval()
    return net


def train_vanilla(epochs=60, batch=8192, lr=8e-4, out=None):
    import torch
    import torch.nn as nn
    torch.set_num_threads(2)
    torch.manual_seed(0)
    arr = build_data()
    rho, T, P, e = arr[:, 0], arr[:, 1], arr[:, 2], arr[:, 3]
    X = encode(rho, T).astype(np.float32)
    Y = np.stack([(np.log10(P) - LP0) / (LP1 - LP0), (e - E0) / (E1 - E0)], 1).astype(np.float32)

    rng = np.random.default_rng(42)
    idx = rng.permutation(len(X))
    n_te = int(0.2 * len(X))
    te, tr = idx[:n_te], idx[n_te:]
    np.save(WORK / 'test_idx.npy', te)
    np.save(WORK / 'train_idx.npy', tr)

    Xtr, Ytr = torch.tensor(X[tr]), torch.tensor(Y[tr])
    Xte, Yte = torch.tensor(X[te]), torch.tensor(Y[te])

    net = net_class()(128)
    opt = torch.optim.Adam(net.parameters(), lr=lr)
    steps = (len(tr) // batch + 1) * epochs
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=lr, total_steps=steps, pct_start=0.2)
    mse = nn.MSELoss()
    hist, best, best_state = [], 1e9, None
    t0 = time.time()
    for ep in range(epochs):
        net.train()
        perm = torch.randperm(len(tr))
        tot = nb = 0
        for k in range(0, len(tr) - batch + 1, batch):
            b = perm[k:k + batch]
            loss = mse(net(Xtr[b]), Ytr[b])
            if not torch.isfinite(loss):
                continue
            opt.zero_grad(); loss.backward()
            torch.nn.utils.clip_grad_norm_(net.parameters(), 1.0)
            opt.step(); sched.step()
            tot += float(loss.detach()) * len(b); nb += len(b)
        net.eval()
        with torch.no_grad():
            val = float(mse(net(Xte), Yte))
        hist.append(dict(epoch=ep + 1, train=tot / max(nb, 1), test=val, phys=0.0, viol_pct=0.0))
        if val < best:
            best, best_state = val, {k: v.clone() for k, v in net.state_dict().items()}
        if (ep + 1) % 10 == 0:
            print(f'  vanilla ep {ep+1}/{epochs} test {val:.3e} ({time.time()-t0:.0f}s)', flush=True)
    net.load_state_dict(best_state)
    out = out or WORK / 'vanilla_final.pt'
    import torch as T_
    T_.save(net.state_dict(), out)
    json.dump(hist, open(str(out).replace('.pt', '_hist.json'), 'w'))
    print('vanilla saved', out, 'best', best)
    return out


# ------------------------------------------------------------------ метрики
def acc_P(y_true, y_pred, P_true, P_pred):
    rel = np.abs(P_pred - P_true) / np.maximum(P_true, 1e-300)
    return dict(r2=float(1 - np.sum((y_true - y_pred) ** 2) / np.sum((y_true - y_true.mean()) ** 2)),
                mse=float(np.mean((y_true - y_pred) ** 2)),
                rmse_log=float(np.sqrt(np.mean((np.log10(P_true) - np.log10(P_pred)) ** 2))),
                mape=float(np.mean(rel) * 100), med_rel=float(np.median(rel) * 100),
                p95_rel=float(np.percentile(rel, 95) * 100),
                p99_rel=float(np.percentile(rel, 99) * 100), max_rel=float(rel.max() * 100))


def acc_e(y_true, y_pred, e_true, e_pred):
    err = np.abs(e_pred - e_true)
    return dict(r2=float(1 - np.sum((y_true - y_pred) ** 2) / np.sum((y_true - y_true.mean()) ** 2)),
                mse=float(np.mean((y_true - y_pred) ** 2)),
                mae_kj=float(np.mean(err)), med_ae_kj=float(np.median(err)),
                p95_ae_kj=float(np.percentile(err, 95)), max_ae_kj=float(err.max()))


def calc_metrics():
    import torch
    torch.set_num_threads(2)
    arr_full = build_data()
    te = np.load(WORK / 'test_idx.npy')
    arr = arr_full[te]
    rho, T, P_true, e_true = arr[:, 0], arr[:, 1], arr[:, 2], arr[:, 3]
    res = []

    # baseline
    regs = build_baseline()
    lrq, ltq = np.log10(rho), np.log10(T)
    fP, fe = query(regs, lrq, ltq)
    h = 1e-3
    fPr, _ = query(regs, lrq + h, ltq)
    fPrm, _ = query(regs, lrq - h, ltq)
    fPT, _ = query(regs, lrq, ltq + h)
    fPTm, _ = query(regs, lrq, ltq - h)
    _, feT = query(regs, lrq, ltq + h)
    _, feTm = query(regs, lrq, ltq - h)
    sub = slice(0, 100000)
    rho_s, T_s = rho[sub], T[sub]
    dP_drho = (10 ** fPr[sub] - 10 ** fPrm[sub]) / (2 * rho_s * np.log(10) * h)
    dP_dT = (10 ** fPT[sub] - 10 ** fPTm[sub]) / (2 * T_s * np.log(10) * h)
    de_dT = (feT[sub] - feTm[sub]) / (2 * T_s * np.log(10) * h)
    vb = violations(dP_drho, dP_dT, de_dT, rho_s, T_s)
    ok = ~np.isnan(fP)
    t0 = time.perf_counter()
    qi = np.random.default_rng(1).integers(0, len(arr), 100000)
    query(regs, lrq[qi], ltq[qi])
    dt = time.perf_counter() - t0
    grid_mb = float(sum(len(r['lr']) * len(r['lt']) for r in regs) * 16 / 2 ** 20)
    res.append(dict(tag='Baseline (билинейная интерполяция)', width=None, params=None,
                    size_mb=grid_mb, coverage_pct=float(100 * ok.mean()),
                    P=acc_P((np.log10(P_true[ok]) - LP0) / (LP1 - LP0),
                            (fP[ok] - LP0) / (LP1 - LP0), P_true[ok], 10 ** fP[ok]),
                    e=acc_e((e_true[ok] - E0) / (E1 - E0), (fe[ok] - E0) / (E1 - E0),
                            e_true[ok], fe[ok]),
                    physics={k: v for k, v in vb.items() if not isinstance(v, np.ndarray)},
                    speed=dict(queries=100000, seconds=dt, us_per_query=dt / 1e5 * 1e6,
                               qps=1e5 / dt)))

    # нейросети
    for tag, path in (('Vanilla MLP', WORK / 'vanilla_final.pt'),
                      ('PINN', ROOT / 'pinn_best_physics.pt')):
        net = load_net(path)
        with torch.no_grad():
            out = net(torch.tensor(encode(rho, T), dtype=torch.float32)).numpy()
        lp_hat = out[:, 0] * (LP1 - LP0) + LP0
        P_hat = 10 ** lp_hat
        e_hat = out[:, 1] * (E1 - E0) + E0

        arr_s = arr_full[te[:100000]]
        xs = torch.tensor(encode(arr_s[:, 0], arr_s[:, 1]), dtype=torch.float32, requires_grad=True)
        net.zero_grad()
        o = net(xs)
        gP = torch.autograd.grad(o[:, 0].sum(), xs, retain_graph=True)[0].numpy()
        ge = torch.autograd.grad(o[:, 1].sum(), xs, retain_graph=True)[0].numpy()
        rho_s, T_s = arr_s[:, 0], arr_s[:, 1]
        P_s = 10 ** (o[:, 0].detach().numpy() * (LP1 - LP0) + LP0)
        dP_drho = P_s * gP[:, 0] * (LP1 - LP0) / (LR1 - LR0) * np.log(10) / (rho_s * np.log(10))
        dP_dT = P_s * gP[:, 1] * (LP1 - LP0) / (LT1 - LT0) * np.log(10) / (T_s * np.log(10))
        de_dT = ge[:, 1] * (E1 - E0) / (LT1 - LT0) / (T_s * np.log(10))
        v = violations(dP_drho, dP_dT, de_dT, rho_s, T_s)

        q = torch.rand(100000, 2)
        with torch.no_grad():
            net(q[:1000])
            best = 1e9
            for _ in range(3):
                t0 = time.perf_counter(); net(q); best = min(best, time.perf_counter() - t0)

        res.append(dict(tag=tag, width=128,
                        params=int(sum(p.numel() for p in net.parameters())),
                        size_mb=os.path.getsize(path) / 2 ** 20,
                        P=acc_P((np.log10(P_true) - LP0) / (LP1 - LP0), (lp_hat - LP0) / (LP1 - LP0),
                                P_true, P_hat),
                        e=acc_e((e_true - E0) / (E1 - E0), (e_hat - E0) / (E1 - E0), e_true, e_hat),
                        physics={k: val for k, val in v.items() if not isinstance(val, np.ndarray)},
                        speed=dict(queries=100000, seconds=best, us_per_query=best / 1e5 * 1e6,
                                   qps=1e5 / best)))

    json.dump(res, open(WORK / 'final_metrics.json', 'w'), indent=2, ensure_ascii=False)
    (ROOT / 'presentation' / 'variants').mkdir(parents=True, exist_ok=True)
    json.dump(res, open(ROOT / 'presentation' / 'variants' / 'metrics.json', 'w'),
              indent=2, ensure_ascii=False)
    for m in res:
        print(f"  {m['tag']:<36} R2(P) {m['P']['r2']:.5f} med {m['P']['med_rel']:.2f}% "
              f"viol {m['physics']['any_']:.2f}% size {m['size_mb']:.3f} MB")
    return res


def calc_baseline_tradeoff():
    arr = build_data()
    te = np.load(WORK / 'test_idx.npy')
    a = arr[te]
    lrq, ltq = np.log10(a[:, 0]), np.log10(a[:, 1])
    out = {}
    for decim in (1, 2, 4, 8):
        import glob
        from scipy.interpolate import RegularGridInterpolator
        regs = []
        for f in sorted(glob.glob(str(ROOT / 'Материалы к хакатону' / 'Obl*.txt'))):
            d = np.loadtxt(f, comments='#')
            lr, lt = np.log10(d[:, 0]), np.log10(d[:, 1])
            ur, ut = np.unique(lr), np.unique(lt)
            gP = d[:, 2].reshape(len(ut), len(ur))
            ge = d[:, 3].reshape(len(ut), len(ur))
            if decim > 1:
                ur, ut = ur[::decim], ut[::decim]
                gP, ge = gP[::decim, ::decim], ge[::decim, ::decim]
            regs.append(dict(lr=ur, lt=ut,
                             iP=RegularGridInterpolator((ut, ur), np.log10(gP), bounds_error=False),
                             ie=RegularGridInterpolator((ut, ur), ge, bounds_error=False)))
        predP, _ = query(regs, lrq, ltq)
        ok = ~np.isnan(predP)
        rel = np.abs(10 ** predP[ok] - a[ok, 2]) / a[ok, 2]
        n = sum(len(r['lr']) * len(r['lt']) for r in regs)
        out[f'decim{decim}'] = dict(decimation=decim, grid_points=int(n),
                                    table_mb=float(n * 16 / 2 ** 20),
                                    coverage_pct=float(100 * ok.mean()),
                                    med_rel_P=float(np.median(rel) * 100),
                                    p95_rel_P=float(np.percentile(rel, 95) * 100))
    json.dump(out, open(WORK / 'eval_baseline2.json', 'w'), indent=2)
    print('  tradeoff:', {k: round(v['med_rel_P'], 4) for k, v in out.items()})


def calc_cs():
    arr = build_data()
    te = np.load(WORK / 'test_idx.npy')
    a = arr[te][:120000]
    lrq, ltq = np.log10(a[:, 0]), np.log10(a[:, 1])
    regs = build_baseline()
    h = 1e-3
    fP, _ = query(regs, lrq, ltq)
    fPr, _ = query(regs, lrq + h, ltq)
    fPrm, _ = query(regs, lrq - h, ltq)
    fPT, _ = query(regs, lrq, ltq + h)
    fPTm, _ = query(regs, lrq, ltq - h)
    _, feT = query(regs, lrq, ltq + h)
    _, feTm = query(regs, lrq, ltq - h)
    rho, T = a[:, 0], a[:, 1]
    dP_drho = (10 ** fPr - 10 ** fPrm) / (2 * rho * np.log(10) * h)
    dP_dT = (10 ** fPT - 10 ** fPTm) / (2 * T * np.log(10) * h)
    de_dT = (feT - feTm) / (2 * T * np.log(10) * h)
    cs_tab = violations(dP_drho, dP_dT, de_dT, rho, T)['cs'] / 1e5
    import torch
    net = load_net(ROOT / 'pinn_best_physics.pt')
    x = torch.tensor(encode(rho, T), dtype=torch.float32, requires_grad=True)
    net.zero_grad(); o = net(x)
    gP = torch.autograd.grad(o[:, 0].sum(), x, retain_graph=True)[0].numpy()
    ge = torch.autograd.grad(o[:, 1].sum(), x, retain_graph=True)[0].numpy()
    P = 10 ** (o[:, 0].detach().numpy() * (LP1 - LP0) + LP0)
    dPdrho = P * gP[:, 0] * (LP1 - LP0) / (LR1 - LR0) * np.log(10) / (rho * np.log(10))
    dPdT = P * gP[:, 1] * (LP1 - LP0) / (LT1 - LT0) * np.log(10) / (T * np.log(10))
    dedT = ge[:, 1] * (E1 - E0) / (LT1 - LT0) / (T * np.log(10))
    cs_p = violations(dPdrho, dPdT, dedT, rho, T)['cs'] / 1e5
    ok = np.isfinite(cs_tab) & (cs_tab > 0) & np.isfinite(cs_p) & (cs_p > 0)
    r = cs_p[ok] / cs_tab[ok]
    r2 = 1 - np.sum((np.log10(cs_p[ok]) - np.log10(cs_tab[ok])) ** 2) / \
        np.sum((np.log10(cs_tab[ok]) - np.log10(cs_tab[ok]).mean()) ** 2)
    res = dict(n=int(ok.sum()), r2=float(r2),
               med_dev=float(np.median(np.abs(r - 1)) * 100),
               p95_dev=float(np.percentile(np.abs(r - 1), 95) * 100))
    json.dump(res, open(WORK / 'cs_compare.json', 'w'), indent=2)
    print('  cs:', {k: round(v, 3) if isinstance(v, float) else v for k, v in res.items()})


def calc_table_physics():
    regs = build_baseline()
    lr = np.linspace(-3, 4, 240); lt = np.linspace(-1, 7, 320)
    LR, LT = np.meshgrid(lr, lt)
    rho, T = 10 ** LR.ravel(), 10 ** LT.ravel()
    h = 1e-3
    fP, _ = query(regs, LR.ravel(), LT.ravel())
    fPr, _ = query(regs, LR.ravel() + h, LT.ravel())
    fPrm, _ = query(regs, LR.ravel() - h, LT.ravel())
    fPT, _ = query(regs, LR.ravel(), LT.ravel() + h)
    fPTm, _ = query(regs, LR.ravel(), LT.ravel() - h)
    _, feT = query(regs, LR.ravel(), LT.ravel() + h)
    _, feTm = query(regs, LR.ravel(), LT.ravel() - h)
    dPdrho = (10 ** fPr - 10 ** fPrm) / (2 * rho * np.log(10) * h)
    dedT = (feT - feTm) / (2 * T * np.log(10) * h)
    dPdT = (10 ** fPT - 10 ** fPTm) / (2 * T * np.log(10) * h)
    cs2 = sound_speed(dPdrho, dPdT, dedT, rho, T)
    bad = (~(dPdrho > 0)) | (~(dedT > 0)) | (~(cs2 > 0))
    res = dict(bad_frac=float(np.nanmean(bad)), cs_neg_frac=float(np.nanmean(cs2 <= 0)),
               cs_med=float(np.nanmedian(np.sqrt(np.clip(cs2, 0, None))) / 1e5),
               cs_min=float(np.nanmin(np.sqrt(np.clip(cs2, 0, None))) / 1e5),
               cs_max=float(np.nanmax(np.sqrt(np.clip(cs2, 0, None))) / 1e5))
    json.dump(res, open(WORK / 'table_cs_stats.json', 'w'), indent=2)
    print('  table physics:', res)


def calc_zones():
    import torch
    arr = build_data()
    te = np.load(WORK / 'test_idx.npy')[:120000]
    a = arr[te]
    lrq, ltq = np.log10(a[:, 0]), np.log10(a[:, 1])
    regs = build_baseline()
    hstep = 5e-3
    jump = np.zeros(len(a), dtype=bool)
    for s in (1e-3, 2e-3, 4e-3, 6e-3):
        f1, _ = query(regs, lrq + s, ltq)
        f2, _ = query(regs, lrq - s, ltq)
        jump |= np.abs(f1 - f2) > 0.02
    nets = {}
    for tag, path in (('vanilla', WORK / 'vanilla_final.pt'), ('pinn', ROOT / 'pinn_best_physics.pt')):
        net = load_net(path)
        with torch.no_grad():
            o = net(torch.tensor(encode(a[:, 0], a[:, 1]), dtype=torch.float32)).numpy()
        Ph = 10 ** (o[:, 0] * (LP1 - LP0) + LP0)
        nets[tag] = np.abs(Ph - a[:, 2]) / a[:, 2] * 100
    zones = dict(
        low=ltq < 3, mid=(ltq >= 3) & (ltq < 5), high=ltq >= 5)
    res = dict(
        jump_frac=float(jump.mean() * 100),
        med_err_jump=float(np.median(nets['pinn'][jump])),
        med_err_smooth=float(np.median(nets['pinn'][~jump])),
        med_err_jump_van=float(np.median(nets['vanilla'][jump])),
        zone_med_pinn={k: float(np.median(nets['pinn'][m])) for k, m in zones.items()},
        zone_med_van={k: float(np.median(nets['vanilla'][m])) for k, m in zones.items()},
    )
    json.dump(res, open(WORK / 'zone_stats.json', 'w'), indent=2)
    print('  zones:', {k: round(v, 2) for k, v in res.items() if isinstance(v, float)})


def calc_compression():
    import torch
    import torch.nn as nn
    net = load_net(ROOT / 'pinn_best_physics.pt')
    q = torch.rand(1, 2)

    def bench(model, reps=2000):
        with torch.no_grad():
            model(q)
            t0 = time.perf_counter()
            for _ in range(reps):
                model(q)
            return (time.perf_counter() - t0) / reps * 1e6

    res = dict(batch1=dict(fp32_us=bench(net)))
    scripted = torch.jit.script(net)
    res['batch1']['torchscript_us'] = bench(scripted)
    q8 = torch.ao.quantization.quantize_dynamic(net, {nn.Linear}, dtype=torch.qint8)
    res['batch1']['int8_us'] = bench(q8)
    x = torch.rand(50000, 2)
    with torch.no_grad():
        d = np.abs(net(x).numpy() - q8(x).numpy())
    res['int8'] = dict(size_mb=0.031, mean_abs_delta=float(d.mean()),
                       p99_abs_delta=float(np.percentile(d, 99)),
                       max_abs_delta=float(d.max()))
    res['sizes'] = dict(fp32_mb=os.path.getsize(ROOT / 'pinn_best_physics.pt') / 2 ** 20,
                        int8_mb=0.031)
    json.dump(res, open(WORK / 'compression.json', 'w'), indent=2)
    print('  compression:', res['batch1'], res['int8'])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('step', nargs='?', default='all')
    args = ap.parse_args()
    steps = ['data', 'vanilla', 'metrics', 'tradeoff', 'cs', 'table', 'zones', 'compress']
    if args.step != 'all':
        steps = [args.step]
    for s in steps:
        print(f'[{s}]', flush=True)
        if s == 'data':
            build_data()
        elif s == 'vanilla':
            if not (WORK / 'vanilla_final.pt').exists():
                train_vanilla()
            else:
                print('  already trained')
        elif s == 'metrics':
            calc_metrics()
        elif s == 'tradeoff':
            calc_baseline_tradeoff()
        elif s == 'cs':
            calc_cs()
        elif s == 'table':
            calc_table_physics()
        elif s == 'zones':
            calc_zones()
        elif s == 'compress':
            calc_compression()


if __name__ == '__main__':
    main()
