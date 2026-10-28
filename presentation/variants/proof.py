"""Рендер дек в PNG и контактные листы для визуальной проверки."""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import proof_render as PR

ROOT = Path(__file__).resolve().parents[1]


def render(pptx, sub, bg):
    out = ROOT / 'proof' / sub
    paths = PR.render(str(pptx), out_dir=str(out), bg=bg)
    return paths


def sheet(paths, out, cols=2, width=760):
    ims = [Image.open(p) for p in paths]
    th = int(width * ims[0].height / ims[0].width)
    rows = (len(ims) + cols - 1) // cols
    pad = 10
    canvas = Image.new('RGB', (cols * width + pad * (cols + 1),
                               rows * th + pad * (rows + 1)), (245, 245, 245))
    for i, im in enumerate(ims):
        r, c = divmod(i, cols)
        canvas.paste(im.resize((width, th)), (pad + c * (width + pad), pad + r * (th + pad)))
    canvas.save(out)
    return out


if __name__ == '__main__':
    pptx, sub, bg = sys.argv[1], sys.argv[2], sys.argv[3]
    b = tuple(int(x) for x in bg.split(','))
    ps = render(pptx, sub, b)
    print(len(ps), sheet(ps, ROOT / 'proof' / sub / 'sheet.png'))
