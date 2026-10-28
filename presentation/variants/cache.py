"""Один раз считает тяжёлые поля для всех пяти презентаций и кэширует их в .npz.

Запуск: python3 presentation/variants/cache.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'work'))

from baseline_lib import build, query          # noqa: E402
from physics_eval_lib import violations        # noqa: E402
from train2 import EOSNet                      # noqa: E402

torch.set_num_threads(2)
CACHE = ROOT / 'work' / 'cache'
CACHE.mkdir(parents=True, exist_ok=True)

NORM = json.loads((ROOT / 'normalization.json').read_text())
lr0, lr1 = NORM['inputs']['log_rho']['min'], NORM['inputs']['log_rho']['max']
lt0, lt1 = NORM['inputs']['log_T']['min'], NORM['inputs']['log_T']['max']
LP0, LP1 = np.log10(NORM['outputs']['P']['min']), np.log10(NORM['outputs']['P']['max'])
e0, e1 = NORM['outputs']['e']['min'], NORM['outputs']['e']['max']


def encode(rho, T):
    return np.stack([(np.log10(rho) - lr0) / (lr1 - lr0),
                     (np.log10(T) - lt0) / (lt1 - lt0)], -1)


def load_net(ckpt, width=128):
    net = EOSNet(width)
    net.load_state_dict(torch.load(ckpt, map_location='cpu'))
    net.eval()
    return net


def main():
    regs = build(1)
    lr = np.linspace(-3, 4, 200)
    lt = np.linspace(-1, 7, 280)
    LR, LT = np.meshgrid(lr, lt)
    rho, T = 10 ** LR.ravel(), 10 ** LT.ravel()

    fP, fe = query(regs, LR.ravel(), LT.ravel())
    P_true = 10 ** fP
    inside = ~np.isnan(fP)

    h = 1e-3
    fPr, _ = query(regs, LR.ravel() + h, LT.ravel())
    fPrm, _ = query(regs, LR.ravel() - h, LT.ravel())
    fPT, _ = query(regs, LR.ravel(), LT.ravel() + h)
    fPTm, _ = query(regs, LR.ravel(), LT.ravel() - h)
    _, feT = query(regs, LR.ravel(), LT.ravel() + h)
    _, feTm = query(regs, LR.ravel(), LT.ravel() - h)
    dPdrho_t = (10 ** fPr - 10 ** fPrm) / (2 * rho * np.log(10) * h)
    dPdT_t = (10 ** fPT - 10 ** fPTm) / (2 * T * np.log(10) * h)
    dedT_t = (feT - feTm) / (2 * T * np.log(10) * h)
    v_t = violations(dPdrho_t, dPdT_t, dedT_t, rho, T)
    cs_tab = v_t['cs'] / 1e5
    bad_tab = (~(dPdrho_t > 0)) | (~(dedT_t > 0)) | (~(v_t['cs2'] > 0))

    out = dict(lr=lr, lt=lt, logP=fP, e=fe, inside=inside,
               P_true=P_true, cs_tab=cs_tab, bad_tab=bad_tab)

    for tag, path in (('vanilla', 'work/vanilla_final.pt'), ('pinn', 'work/pinn_final.pt')):
        net = load_net(ROOT / path)
        net.zero_grad()
        x = torch.tensor(encode(rho, T), dtype=torch.float32, requires_grad=True)
        o = net(x)
        gP = torch.autograd.grad(o[:, 0].sum(), x, retain_graph=True)[0].numpy()
        ge = torch.autograd.grad(o[:, 1].sum(), x, retain_graph=True)[0].numpy()
        P_hat = 10 ** (o[:, 0].detach().numpy() * (LP1 - LP0) + LP0)
        dPdrho = P_hat * gP[:, 0] * (LP1 - LP0) / (lr1 - lr0) * np.log(10) / (rho * np.log(10))
        dPdT = P_hat * gP[:, 1] * (LP1 - LP0) / (lt1 - lt0) * np.log(10) / (T * np.log(10))
        dedT = ge[:, 1] * (e1 - e0) / (lt1 - lt0) / (T * np.log(10))
        v = violations(dPdrho, dPdT, dedT, rho, T)
        err = np.abs(P_hat - P_true) / np.maximum(P_true, 1e-300)
        out[f'err_{tag}'] = np.where(inside, err, np.nan).reshape(LR.shape)
        out[f'bad_{tag}'] = ((~(dPdrho > 0)) | (~(dedT > 0)) | (~(v['cs2'] > 0))).reshape(LR.shape)
        out[f'cs_{tag}'] = (v['cs'] / 1e5).reshape(LR.shape)

    np.savez_compressed(CACHE / 'fields.npz', **out)
    print('cached fields:', {k: getattr(v, 'shape', None) for k, v in out.items() if hasattr(v, 'shape')})


if __name__ == '__main__':
    main()
