"""Пять дизайн-систем для пяти вариантов презентации."""
from __future__ import annotations

from pptx.dml.color import RGBColor


def C(h):
    return RGBColor.from_string(h.upper().lstrip('#'))


SWISS = dict(
    key='swiss', name='Swiss · чистая типографика', photos=0,
    bg=C('FFFFFF'), panel=C('F2F2F2'), ink=C('111111'), muted=C('6B6B6B'),
    accent=C('E2231A'), accent2=C('111111'), line=C('111111'), hair=C('D0D0D0'),
    on_accent=C('FFFFFF'), fig_bg=None, soft=C('F2F2F2'),
    head='Arial', body='Arial', mono='Consolas',
)

INDUSTRIAL = dict(
    key='industrial', name='Industrial · фото-арт-дирекшн', photos=8,
    bg=C('121010'), panel=C('1C1917'), ink=C('F6F1E6'), muted=C('A79C8C'),
    accent=C('F0A02A'), accent2=C('C8452B'), line=C('3A342B'), hair=C('2E2A25'),
    on_accent=C('141110'), fig_bg=C('1C1917'),
    head='Arial', body='Arial', mono='Consolas',
)

EDITORIAL = dict(
    key='editorial', name='Editorial · научный журнал', photos=2,
    bg=C('F7F2E8'), panel=C('FFFCF5'), ink=C('1D1B16'), muted=C('7B7263'),
    accent=C('8A5A2B'), accent2=C('3E5C4B'), line=C('2A2620'), hair=C('D6CCB9'),
    on_accent=C('F7F2E8'), fig_bg=C('FFFCF5'),
    head='Georgia', body='Georgia', mono='Consolas',
)

NEON = dict(
    key='neon', name='Neon · data-tech', photos=5,
    bg=C('05070E'), panel=C('0B1120'), ink=C('E8F1FF'), muted=C('7B8FAC'),
    accent=C('25E0C0'), accent2=C('FF3D81'), line=C('1B2B47'), hair=C('14203A'),
    on_accent=C('04120F'), fig_bg=C('0B1120'),
    head='Arial', body='Arial', mono='Consolas',
)

REPORT = dict(
    key='report', name='Report · годовой отчёт', photos=7,
    bg=C('FBF8F2'), panel=C('FFFFFF'), ink=C('1E2A22'), muted=C('6E7A6C'),
    accent=C('1F5C43'), accent2=C('C4622D'), line=C('DCD3C3'), hair=C('E7E0D2'),
    on_accent=C('FFFFFF'), fig_bg=C('FFFFFF'), soft=C('F4F0E7'),
    head='Georgia', body='Arial', mono='Consolas',
)

ALL = [SWISS, INDUSTRIAL, EDITORIAL, NEON, REPORT]
