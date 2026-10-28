"""Светлые версии ключевых графиков (по одной на каждую светлую тему).

Запуск: python3 presentation/variants/figures_light.py
Пишет presentation/variants/figs_light/<theme>/*.png и work/cache/fields.npz
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pipeline as P  # noqa: E402

OUT = Path(__file__).resolve().parent / 'figs_light'
WORK = P.WORK

PALETTES = {
    'swiss': dict(bg='#FFFFFF', ink='#111111', muted='#8A8A8A', accent='#E2231A',
                  accent2='#111111', grid='#E4E4E4', soft='#F2F2F2',
                  ramp=['#FBE7E2', '#F0A79A', '#D01E15']),
    'editorial': dict(bg='#F7F2E8', ink='#1D1B16', muted='#7B7263', accent='#8A5A2B',
                      accent2='#3E5C4B', grid='#E0D6C3', soft='#FFFCF5',
                      ramp=['#F6EDDD', '#CFAE84', '#7A4A20']),
    'report': dict(bg='#FFFFFF', ink='#1E2A22', muted='#6E7A6C', accent='#1F5C43',
                   accent2='#C4622D', grid='#ECE6DB', soft='#F4F0E7',
                   ramp=['#EDF3EF', '#9BC4B2', '#14503A']),
    'industrial': dict(bg='#121010', ink='#F6F1E6', muted='#A79C8C', accent='#F0A02A',
                       accent2='#C8452B', grid='#2A2520', soft='#1C1917',
                       ramp=['#121010', '#8C3A1F', '#F0A02A']),
    'neon': dict(bg='#05070E', ink='#E8F1FF', muted='#7B8FAC', accent='#25E0C0',
                 accent2='#FF3D81', grid='#14203A', soft='#0B1120',
                 ramp=['#05070E', '#1D5E63', '#25E0C0']),
}


def cmap_of(pal, kind='err'):
    return LinearSegmentedColormap.from_list('c_' + kind, pal['ramp'])


def style(ax, pal, grid_axis='y'):
    ax.set_facecolor(pal['bg'])
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    for side in ('left', 'bottom'):
        ax.spines[side].set_color(pal['muted'])
        ax.spines[side].set_linewidth(0.6)
    ax.tick_params(colors=pal['muted'], labelsize=8, width=0.6, length=3)
    if grid_axis in ('x', 'y', 'both'):
        ax.grid(True, axis=grid_axis, color=pal['grid'], lw=0.6)
    ax.set_axisbelow(True)


def save(fig, theme, name):
    d = OUT / theme
    d.mkdir(parents=True, exist_ok=True)
    fig.savefig(d / f'{name}.png', dpi=200, facecolor=fig.get_facecolor(),
                bbox_inches='tight', pad_inches=0.12)
    plt.close(fig)


# ------------------------------------------------------------------ поля
def build_fields():
    cache = WORK / 'cache' / 'fields.npz'
    if cache.exists():
        z = np.load(cache)
        return {k: z[k] for k in z.files}
    arr = P.build_data()
    te = np.load(WORK / 'test_idx.npy')
    lr = np.linspace(-3.0, 4.0, 240)
    lt = np.linspace(-1.0, 7.0, 320)
    LR, LT = np.meshgrid(lr, lt)
    rho, T = 10 ** LR.ravel(), 10 ** LT.ravel()
    regs = P.build_baseline()
    h = 1e-3
    fP, fe = P.query(regs, LR.ravel(), LT.ravel())
    fPr, _ = P.query(regs, LR.ravel() + h, LT.ravel())
    fPrm, _ = P.query(regs, LR.ravel() - h, LT.ravel())
    fPT, _ = P.query(regs, LR.ravel(), LT.ravel() + h)
    fPTm, _ = P.query(regs, LR.ravel(), LT.ravel() - h)
    _, feT = P.query(regs, LR.ravel(), LT.ravel() + h)
    _, feTm = P.query(regs, LR.ravel(), LT.ravel() - h)
    dPdrho = (10 ** fPr - 10 ** fPrm) / (2 * rho * np.log(10) * h)
    dPdT = (10 ** fPT - 10 ** fPTm) / (2 * T * np.log(10) * h)
    dedT = (feT - feTm) / (2 * T * np.log(10) * h)
    cs2 = P.sound_speed(dPdrho, dPdT, dedT, rho, T)
    bad_tab = (~(dPdrho > 0)) | (~(dedT > 0)) | (~(cs2 > 0))
    out = dict(lr=lr, lt=lt, Ptab=(10 ** fP).reshape(LR.shape), etab=fe.reshape(LR.shape),
               bad_tab=bad_tab.reshape(LR.shape))

    import torch
    for tag, path in (('van', WORK / 'vanilla_final.pt'),
                      ('pinn', P.ROOT / 'pinn_best_physics.pt')):
        net = P.load_net(path)
        x = torch.tensor(P.encode(rho, T), dtype=torch.float32, requires_grad=True)
        net.zero_grad()
        o = net(x)
        gP = torch.autograd.grad(o[:, 0].sum(), x, retain_graph=True)[0].numpy()
        ge = torch.autograd.grad(o[:, 1].sum(), x, retain_graph=True)[0].numpy()
        Ph = 10 ** (o[:, 0].detach().numpy() * (P.LP1 - P.LP0) + P.LP0)
        dPdrho = Ph * gP[:, 0] * (P.LP1 - P.LP0) / (P.LR1 - P.LR0) / rho
        dPdT = Ph * gP[:, 1] * (P.LP1 - P.LP0) / (P.LT1 - P.LT0) / T
        dedT = ge[:, 1] * (P.E1 - P.E0) / (P.LT1 - P.LT0) / (T * np.log(10))
        v = P.violations(dPdrho, dPdT, dedT, rho, T)
        out[f'P_{tag}'] = Ph.reshape(LR.shape)
        out[f'err_{tag}'] = (np.abs(Ph - 10 ** fP) / np.abs(10 ** fP) * 100).reshape(LR.shape)
        out[f'bad_{tag}'] = v['any_']
        out[f'flags_{tag}'] = np.stack([
            ~(dPdrho > 0), ~(dedT > 0), ~(v['cs2'] > 0)]).reshape(3, *LR.shape)
        out[f'cs_{tag}'] = v['cs'].reshape(LR.shape)
        out[f'viol_{tag}'] = v['any_']
    out['cs_tab_grid'] = np.sqrt(np.clip(cs2, 0, None)).reshape(LR.shape)
    np.savez_compressed(cache, **out)
    return out


def main():
    f = build_fields()
    lr, lt = f['lr'], f['lt']
    ext = [lr[0], lr[-1], lt[0], lt[-1]]
    metrics = json.loads((WORK / 'final_metrics.json').read_text())
    comp = json.loads((WORK / 'compression.json').read_text())
    hist = json.loads((WORK / 'vanilla_final_hist.json').read_text())

    for theme, pal in PALETTES.items():
        plt.rcParams.update({'font.family': 'DejaVu Sans', 'text.color': pal['ink'],
                             'axes.labelcolor': pal['muted'], 'figure.facecolor': pal['bg']})

        # 1. карты P и e
        fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.2))
        for ax, key, ttl, unit in ((axes[0], 'Ptab', 'Давление log₁₀ P, ГПа', ''),
                                   (axes[1], 'etab', 'Энергия e, кДж/г (знак. лог)', '')):
            if key == 'Ptab':
                arr = np.log10(np.abs(f[key]))
            else:
                arr = np.sign(f[key]) * np.log10(1 + np.abs(f[key]))
            cm = cmap_of(pal, 'field')
            m = ax.pcolormesh(lr, lt, arr, cmap=cm, shading='auto')
            ax.set_title(ttl, fontsize=10.5, color=pal['ink'], pad=8)
            ax.set_xlabel('log₁₀ ρ, г/см³')
            ax.set_ylabel('log₁₀ T, К')
            style(ax, pal, 'none')
            cb = fig.colorbar(m, ax=ax, pad=0.02)
            cb.ax.tick_params(labelsize=7, colors=pal['muted'], length=2)
            cb.outline.set_visible(False)
        fig.tight_layout()
        save(fig, theme, 'eda_maps')

        # 2. кривые обучения vanilla
        ep = [h['epoch'] for h in hist]
        tr = [max(h['train'], 1e-9) for h in hist]
        te_ = [h['test'] for h in hist]
        fig, ax = plt.subplots(figsize=(6.4, 3.9))
        ax.semilogy(ep, tr, color=pal['muted'], lw=1.3, label='train')
        ax.semilogy(ep, te_, color=pal['accent'], lw=2.0, label='test (20 %)')
        style(ax, pal)
        ax.set_xlabel('эпоха')
        ax.set_ylabel('MSE в нормированных единицах')
        ax.legend(frameon=False, fontsize=8.5, labelcolor=pal['ink'])
        fig.tight_layout()
        save(fig, theme, 'val_curves')

        # 3. карты ошибок
        fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.3))
        from matplotlib.colors import LogNorm
        norm = LogNorm(vmin=0.3, vmax=100)
        for ax, key, ttl in ((axes[0], 'err_van', 'Vanilla MLP'),
                             (axes[1], 'err_pinn', 'PINN')):
            m = ax.pcolormesh(lr, lt, np.clip(np.abs(f[key]), 0.3, 100), cmap=cmap_of(pal),
                              shading='auto', norm=norm)
            ax.set_title(ttl, fontsize=11)
            ax.set_xlabel('log₁₀ ρ')
            ax.set_ylabel('log₁₀ T')
            style(ax, pal, 'none')
        cb = fig.colorbar(m, ax=axes, pad=0.02)
        cb.set_label('|ΔP| / P, % (лог. шкала, ≥ 100 обрезано)', fontsize=8, color=pal['muted'])
        cb.ax.tick_params(labelsize=7, colors=pal['muted'], length=2)
        cb.outline.set_visible(False)
        save(fig, theme, 'error_maps')

        # 4. карты нарушений
        fig, axes = plt.subplots(1, 2, figsize=(9.4, 4.4))
        cm_bad = LinearSegmentedColormap.from_list('b', [pal['bg'], pal['ramp'][1], pal['accent']])
        for ax, key, ttl in ((axes[0], 'van', 'Vanilla MLP'),
                             (axes[1], 'pinn', 'PINN')):
            mask = f[f'flags_{key}'].any(0).astype(float)
            ax.pcolormesh(lr, lt, mask, cmap=cm_bad, shading='auto', vmin=0, vmax=1)
            ax.set_title(f'{ttl} · {100 * mask.mean():.1f} % площади', fontsize=10.5)
            ax.set_xlabel('log₁₀ ρ')
            ax.set_ylabel('log₁₀ T')
            style(ax, pal, 'none')
        fig.tight_layout()
        save(fig, theme, 'violation_maps')

        # 5. бар-чарт нарушений по типам
        by = {m['tag']: m for m in metrics}
        tags = ['Baseline (билинейная интерполяция)', 'Vanilla MLP', 'PINN']
        labs = ['таблица', 'Vanilla', 'PINN']
        keys = ['stab_pct', 'cap_pct', 'cs2_neg_pct', 'any_']
        names = ['∂P/∂ρ ≤ 0', '∂e/∂T ≤ 0', 'c_s² ≤ 0', 'любое']
        fig, ax = plt.subplots(figsize=(6.8, 3.9))
        w = 0.2
        xs = np.arange(len(names))
        cols = [pal['muted'], pal['accent2'], pal['accent']]
        for i, (t, lab) in enumerate(zip(tags, labs)):
            vals = [by[t]['physics'][k] for k in keys]
            ax.bar(xs + (i - 1) * w, vals, w * 0.9, color=cols[i], label=lab)
            for xx, v in zip(xs + (i - 1) * w, vals):
                ax.text(xx, v + 0.8, f'{v:.1f}'.replace('.', ','), ha='center',
                        fontsize=7, color=pal['ink'])
        ax.set_xticks(xs)
        ax.set_xticklabels(names, fontsize=9)
        ax.set_ylabel('% точек теста')
        style(ax, pal)
        ax.legend(frameon=False, fontsize=8.5, labelcolor=pal['ink'], ncol=3)
        fig.tight_layout()
        save(fig, theme, 'violations_bar')

        # 6. c_s: PINN против таблицы
        cs_p, cs_t = f['cs_pinn'].ravel(), f['cs_tab_grid'].ravel()
        ok = np.isfinite(cs_t) & (cs_t > 0) & np.isfinite(cs_p) & (cs_p > 0)
        rng = np.random.default_rng(3)
        sel = rng.choice(np.flatnonzero(ok), size=min(6000, ok.sum()), replace=False)
        fig, ax = plt.subplots(figsize=(5.6, 4.6))
        ax.loglog(cs_t[sel] / 1e5, cs_p[sel] / 1e5, '.', ms=2.2, color=pal['accent'],
                  alpha=0.55, rasterized=True)
        lim = [cs_t[ok].min() / 1e5, cs_t[ok].max() / 1e5]
        ax.plot(lim, lim, '-', color=pal['ink'], lw=1.0)
        style(ax, pal, 'both')
        ax.set_xlabel('c_s по таблице, км/с')
        ax.set_ylabel('c_s по PINN, км/с')
        ax.text(0.03, 0.95, 'пунктир — идеальное совпадение'.replace('пунктир', 'линия'),
                transform=ax.transAxes, fontsize=8, color=pal['muted'], va='top')
        fig.tight_layout()
        save(fig, theme, 'cs_scatter')

        # 7. размер и скорость
        fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.6))
        sizes = [by[t]['size_mb'] for t in tags]
        axes[0].bar(labs, sizes, color=[pal['muted'], pal['accent2'], pal['accent']], width=0.55)
        for i, v in enumerate(sizes):
            axes[0].text(i, v * 1.05, f'{v:.3f}'.replace('.', ',') + ' МБ', ha='center',
                         fontsize=8.5, color=pal['ink'])
        axes[0].set_yscale('log')
        axes[0].set_ylabel('размер, МБ')
        axes[0].set_ylim(0.05, max(sizes) * 2.4)
        axes[0].axhline(10, color=pal['accent'], lw=0.9, ls='--')
        axes[0].text(2.4, 11, 'лимит 10 МБ', ha='right', fontsize=8, color=pal['accent'])
        style(axes[0], pal)
        sp = [by[t]['speed']['us_per_query'] for t in tags]
        axes[1].bar(labs, sp, color=[pal['muted'], pal['accent2'], pal['accent']], width=0.55)
        for i, v in enumerate(sp):
            axes[1].text(i, v * 1.04, f'{v:.2f}'.replace('.', ',') + ' мкс', ha='center',
                         fontsize=8.5, color=pal['ink'])
        axes[1].set_ylabel('мкс на запрос (batch 1)')
        style(axes[1], pal)
        fig.tight_layout()
        save(fig, theme, 'size_speed')

        # 8. c_s по таблице
        fig, ax = plt.subplots(figsize=(5.4, 4.3))
        csg = f['cs_tab_grid'] / 1e5
        m = ax.pcolormesh(lr, lt, np.log10(np.clip(csg, 1e-2, None)), cmap=cmap_of(pal),
                          shading='auto')
        ax.set_title('c_s по таблице, км/с (log₁₀)', fontsize=10.5)
        ax.set_xlabel('log₁₀ ρ')
        ax.set_ylabel('log₁₀ T')
        style(ax, pal, 'none')
        cb = fig.colorbar(m, ax=ax, pad=0.02)
        cb.ax.tick_params(labelsize=7, colors=pal['muted'], length=2)
        cb.outline.set_visible(False)
        fig.tight_layout()
        save(fig, theme, 'table_cs')

        # 9. ошибка по зонам
        zones = json.loads((WORK / 'zone_stats.json').read_text())
        keys = ['low', 'mid', 'high']
        names = ['T < 10³ К', '10³…10⁵ К', 'T > 10⁵ К']
        fig, ax = plt.subplots(figsize=(6.4, 3.4))
        xs = np.arange(3)
        ax.bar(xs - 0.19, [zones['zone_med_van'][k] for k in keys], 0.34,
               color=pal['accent2'], label='Vanilla')
        ax.bar(xs + 0.19, [zones['zone_med_pinn'][k] for k in keys], 0.34,
               color=pal['accent'], label='PINN')
        for i, k in enumerate(keys):
            ax.text(i - 0.19, zones['zone_med_van'][k] + 0.3,
                    f"{zones['zone_med_van'][k]:.1f}".replace('.', ','), ha='center', fontsize=7.5)
            ax.text(i + 0.19, zones['zone_med_pinn'][k] + 0.3,
                    f"{zones['zone_med_pinn'][k]:.1f}".replace('.', ','), ha='center', fontsize=7.5)
        ax.set_xticks(xs)
        ax.set_xticklabels(names, fontsize=8.5)
        ax.set_ylabel('медианная ошибка P, %')
        style(ax, pal)
        ax.legend(frameon=False, fontsize=8.5, labelcolor=pal['ink'])
        fig.tight_layout()
        save(fig, theme, 'error_by_zone')

    print('light figures ->', OUT)


if __name__ == '__main__':
    main()
