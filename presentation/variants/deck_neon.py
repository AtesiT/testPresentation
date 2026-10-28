"""Вариант 4 — Neon / data-tech: тёмный интерфейс, монолейблы, сетка и неоновые акценты."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kit
import themes
from content import (ARTIFACTS, CHECKLIST, CODE_LINES, CONSTRAINTS, DONE, FACTS,
                     LIMITS, NEXT, STORY, WRAPPER_CODE)

T = themes.NEON
BG, PANEL, INK, MUT = T['bg'], T['panel'], T['ink'], T['muted']
ACC, ACC2, HAIR, LINE = T['accent'], T['accent2'], T['hair'], T['line']
H1, BODY, MONO = T['head'], T['body'], T['mono']
ML, MR = 0.8, 0.8
CW = kit.W - ML - MR
FIG = kit.LIGHT / 'neon'
IMG = kit.ASSETS


def grid_bg(s, step=0.833):
    x = 0.0
    while x < kit.W:
        kit.vrule(s, x, 0, kit.H, HAIR, 0.5)
        x += step
    y = 0.0
    while y < kit.H:
        kit.hrule(s, 0, y, kit.W, HAIR, 0.5)
        y += step


def progress(s, num):
    w = 2.2
    kit.rect(s, kit.W - MR - w, 0.44, w, 0.035, fill=LINE)
    kit.rect(s, kit.W - MR - w, 0.44, w * num / 20, 0.035, fill=ACC)


def head(s, num, title=None, sub=None, kicker=None):
    kicker = (kicker or STORY[num][0]).upper()
    title = title or STORY[num][1]
    sub = STORY[num][2] if sub is None else sub
    kit.text(s, ML, 0.38, 0.45, 0.22, f'{num:02d}', size=10, color=ACC, font=MONO, bold=True)
    kit.text(s, ML + 0.55, 0.4, 6.0, 0.2, kicker, size=8.5, color=MUT, font=MONO,
             tracking=1.8)
    progress(s, num)
    kit.hrule(s, ML, 0.62, CW, LINE, 0.75)
    kit.text(s, ML, 0.8, CW - 0.3, 0.62, title, size=30, color=INK, font=H1, bold=True,
             ls=1.0, tracking=-0.6)
    if sub:
        kit.text(s, ML, 1.56, CW - 1.2, 0.5, sub, size=11.5, color=MUT, font=BODY, ls=1.3)


def foot(s, left='pinn / eos al / ρt-grid'):
    kit.hrule(s, ML, 7.04, CW, LINE, 0.75)
    kit.text(s, ML, 7.12, 6.0, 0.2, left, size=8, color=MUT, font=MONO, tracking=1.0)
    kit.text(s, kit.W - MR - 2.0, 7.12, 2.0, 0.2, 'ИТ КоР · ML · КЕЙС 01', size=8, color=MUT,
             font=MONO, align='r', tracking=1.0)


def bracket(s, x, y, w, h, color=None, L=0.22):
    color = color or ACC
    for cx, cy, dx, dy in ((x, y, 1, 1), (x + w, y, -1, 1), (x, y + h, 1, -1),
                           (x + w, y + h, -1, -1)):
        kit.hrule(s, min(cx, cx + dx * L), cy, L, color, 1.6)
        kit.vrule(s, cx, min(cy, cy + dy * L), L, color, 1.6)


def panel(s, x, y, w, h, path=None, cap=None, label=None):
    kit.rect(s, x, y, w, h, fill=PANEL, line=LINE, lw=0.75)
    if path:
        kit.pic_fit(s, path, x + 0.1, y + 0.1, w - 0.2, h - 0.2 - (0.24 if cap else 0))
    if label:
        kit.text(s, x + 0.14, y + 0.1, w - 0.28, 0.2, label.upper(), size=7.5, color=MUT,
                 font=MONO, tracking=1.2)
    if cap:
        kit.text(s, x + 0.14, y + h - 0.26, w - 0.28, 0.2, cap, size=7.5, color=MUT, font=MONO)


def chip(s, x, y, w, value, label, color=None):
    color = color or ACC
    kit.rrect(s, x, y, w, 0.95, radius=0.12, fill=PANEL, line=LINE, lw=0.75)
    kit.text(s, x + 0.2, y + 0.14, w - 0.4, 0.4, value, size=20, color=color, font=MONO,
             bold=True)
    kit.text(s, x + 0.2, y + 0.58, w - 0.35, 0.3, label.upper(), size=7.5, color=MUT,
             font=MONO, tracking=1.0)


def tint_photo(s, path, x, y, w, h, focus=(0.5, 0.5), alpha=55):
    kit.pic_cover(s, IMG / path, x, y, w, h, focus=focus)
    kit.rect(s, x, y, w, h, fill=ACC, transparency=alpha)


def build(out):
    prs = kit.deck()

    # 1 — обложка
    s = kit.slide(prs, BG)
    grid_bg(s)
    tint_photo(s, 'photo_network.jpg', 8.3, 0, 5.03, kit.H, focus=(0.55, 0.5), alpha=40)
    kit.rect(s, 8.3, 0, 5.03, kit.H, fill=BG, transparency=25)
    bracket(s, ML - 0.16, 0.55, 11.9, 6.3, ACC, 0.25)
    kit.text(s, ML, 0.95, 7.4, 0.22, 'fizika v losse · al · 12 poryadkov', size=9, color=ACC,
             font=MONO, tracking=2.0)
    kit.text(s, ML, 1.35, 8.6, 2.6,
             ['Суррогат уравнения', 'состояния алюминия', 'на физическом лоссе'],
             size=38, color=INK, font=H1, bold=True, ls=1.05, tracking=-0.6)
    kit.text(s, ML, 4.35, 7.0, 0.9, 'P(ρ,T), e(ρ,T) и c_s. Ошибка по медиане 8,9 %, нарушений '
             'физики 0,43 %, вес модели 0,10 МБ.', size=12, color=MUT, font=BODY, ls=1.4)
    for i, (v, l) in enumerate([(FACTS['viol_pinn'], 'violations'), (f"×{FACTS['ratio']}", 'vs vanilla'),
                                ('0,10 МБ', 'weights'), ('0,95 мкс', 'per query')]):
        x = ML + i * 2.85
        kit.text(s, x, 5.7, 2.7, 0.4, v, size=22, color=ACC, font=MONO, bold=True)
        kit.text(s, x, 6.2, 2.7, 0.2, l.upper(), size=8, color=MUT, font=MONO, tracking=1.2)
        kit.vrule(s, x - 0.2, 5.7, 0.72, LINE, 0.75)
    kit.text(s, ML, 6.9, 7.0, 0.2, 'ИТ КоР · ТРЕК MACHINE LEARNING · КЕЙС 01 · 2026', size=8,
             color=MUT, font=MONO, tracking=1.4)
    kit.notes(s, STORY[1][3])

    # 2 — постановка
    s = kit.slide(prs, BG)
    head(s, 2)
    for i, (n, t_, d) in enumerate([('01', 'ТОЧНОСТЬ', 'P и e по всей диаграмме, не только в узлах сетки'),
                                    ('02', 'ФИЗИКА', '∂P/∂ρ > 0, ∂e/∂T > 0, 0 < c_s < c'),
                                    ('03', 'ГАБАРИТ', 'до 10 МБ, микросекунды, без GPU')]):
        x = ML + i * 3.85
        kit.rrect(s, x, 2.35, 3.55, 2.1, radius=0.08, fill=PANEL, line=LINE, lw=0.75)
        kit.rect(s, x, 2.35, 3.55, 0.04, fill=ACC if i < 2 else ACC2)
        kit.text(s, x + 0.25, 2.55, 1.0, 0.24, n, size=10, color=ACC, font=MONO, bold=True)
        kit.text(s, x + 0.25, 2.85, 3.0, 0.26, t_, size=10, color=INK, font=BODY, bold=True,
                 tracking=1.2)
        kit.text(s, x + 0.25, 3.25, 3.05, 0.9, d, size=10, color=MUT, font=BODY, ls=1.4)
    kit.text(s, ML, 4.75, 7.3, 1.3, 'Гидрокоду нужны не только P и e, но и производные: от них '
             'зависит устойчивость численной схемы. Поэтому физика проверяется в лоссе, а не '
             'только на защите.', size=12, color=INK, font=BODY, ls=1.45)
    kit.pic_cover(s, IMG / 'photo_compute.jpg', ML + 7.7, 4.7, 4.05, 1.95, focus=(0.5, 0.5))
    kit.rect(s, ML + 7.7, 4.7, 4.05, 1.95, fill=ACC, transparency=74)
    kit.text(s, ML + 7.7, 6.55, 4.05, 0.2, 'inference target: CPU, batch 1', size=7.5,
             color=ACC, font=MONO)
    foot(s)
    kit.notes(s, STORY[2][3])

    # 3 — чек-лист с весами
    s = kit.slide(prs, BG)
    head(s, 3, sub='Структура ответа повторяет финальное задание: 9 критериев, 100 баллов')
    for i, (name, pts, what) in enumerate(CHECKLIST):
        y = 2.42 + i * 0.47
        kit.text(s, ML, y, 0.4, 0.24, f'{i + 1:02d}', size=9, color=MUT, font=MONO)
        kit.text(s, ML + 0.5, y - 0.02, 3.9, 0.26, name, size=11, color=INK, font=BODY)
        w = max(float(pts) / 25 * 1.8, 0.12)
        kit.rect(s, ML + 4.55, y + 0.05, 1.8, 0.14, fill=LINE)
        kit.rect(s, ML + 4.55, y + 0.05, w, 0.14, fill=ACC)
        kit.text(s, ML + 6.55, y - 0.02, 0.6, 0.24, pts, size=9.5, color=ACC, font=MONO,
                 align='r')
        kit.text(s, ML + 7.4, y, 3.9, 0.26, what, size=9, color=MUT, font=BODY)
        kit.hrule(s, ML, y + 0.38, CW, HAIR, 0.5)
    kit.text(s, ML, 6.6, CW, 0.24, '// total 100 / 100 · все артефакты в репозитории', size=9,
             color=ACC, font=MONO)
    foot(s)
    kit.notes(s, STORY[3][3])

    # 4 — данные
    s = kit.slide(prs, BG)
    head(s, 4, title='20 сеток · 1 130 053 строки',
         sub='4 диапазона ρ × 5 диапазонов T; внутри региона — регулярная сетка 300 × 300')
    for i, (v, l) in enumerate([('1 130 053', 'rows'), ('20', 'regions'),
                                ('300 × 300', 'grid'), ('226 011', 'test rows')]):
        x = ML + i * 2.95
        kit.rrect(s, x, 2.4, 2.7, 1.35, radius=0.1, fill=PANEL, line=LINE, lw=0.75)
        kit.text(s, x + 0.2, 2.58, 2.35, 0.45, v, size=21, color=INK, font=MONO, bold=True)
        kit.text(s, x + 0.2, 3.16, 2.3, 0.2, l.upper(), size=7.5, color=ACC, font=MONO,
                 tracking=1.2)
    kit.text(s, ML, 4.05, 5.6, 2.3,
             ['20 независимых таблиц: внутри региона гладко, на стыках несогласованно.',
              '9,5 % узлов полной сетки дают нефизичные производные — до всякой модели.',
              'Тест — 20 % стратифицированной выборки.'],
             size=11, color=MUT, font=BODY, ls=1.45, space_after=10)
    panel(s, ML + 6.35, 4.0, 5.35, 2.5, FIG / 'table_cs.png', 'c_s по таблице, км/с')
    foot(s)
    kit.notes(s, STORY[4][3])

    # 5 — EDA
    s = kit.slide(prs, BG)
    head(s, 5)
    panel(s, ML, 2.35, 5.8, 3.95, FIG / 'eda_maps.png', 'P и e на полной сетке')
    kit.text(s, ML + 6.15, 2.4, 5.5, 3.9,
             ['P меняется на 12 порядков → log на входе и на выходе.',
              'e проходит через ноль → линейный выход, без логарифма.',
              'Скачки на картах — стыки регионов, а не шум.'],
             size=11, color=INK, font=BODY, ls=1.5, space_after=12)
    for i in range(2):
        kit.hrule(s, ML + 6.15, 3.55 + i * 1.1, 5.0, HAIR, 0.5)
    foot(s)
    kit.notes(s, STORY[5][3])

    # 6 — нормализация
    s = kit.slide(prs, BG)
    head(s, 6)
    steps = [('IN', 'x = (log₁₀ρ − a) / (b − a)', 'log₁₀ρ ∈ [−3, 4] · log₁₀T ∈ [−1, 7]'),
             ('P', 'log₁₀P → 10^', 'P ∈ [10⁻⁶, 10⁶] ГПа'),
             ('E', 'линейно, кДж/г', 'e ∈ [−0,2, 10³], знак сохраняется')]
    for i, (tag, f_, d) in enumerate(steps):
        y = 2.35 + i * 1.2
        kit.rrect(s, ML, y, 7.6, 1.0, radius=0.08, fill=PANEL, line=LINE, lw=0.75)
        kit.rect(s, ML, y, 0.05, 1.0, fill=ACC)
        kit.text(s, ML + 0.28, y + 0.15, 0.7, 0.24, tag, size=9, color=ACC, font=MONO, bold=True)
        kit.text(s, ML + 1.1, y + 0.13, 4.6, 0.3, f_, size=12, color=INK, font=MONO)
        kit.text(s, ML + 1.1, y + 0.55, 6.2, 0.3, d, size=9, color=MUT, font=BODY)
    kit.text(s, ML + 8.05, 2.35, 3.6, 3.6,
             ['normalization.json — единственный источник констант.', 'Инференс воспроизводим '
              'без нашего кода.', 'Границы области определения описаны явно.'],
             size=10.5, color=MUT, font=BODY, ls=1.45, space_after=12)
    kit.vrule(s, ML + 7.85, 2.35, 4.5, LINE, 0.75)
    foot(s)
    kit.notes(s, STORY[6][3])

    # 7 — baseline
    s = kit.slide(prs, BG)
    head(s, 7, sub='20 интерполяторов RegularGridInterpolator по регионам, та же тестовая выборка')
    data = [['Вариант', 'Размер', 'Медиана P', 'Покрытие', 'Нарушения'],
            ['Полная', '17,2 МБ', '0,000 %', '100 %', '2,86 %'],
            ['×2', '4,3 МБ', '0,0002 %', '99,4 %', '3,1 %'],
            ['×4', '1,1 МБ', '0,0016 %', '98,7 %', '4,4 %'],
            ['×8', '0,28 МБ', '0,0075 %', '96,7 %', '7,9 %']]
    kit.table(s, ML, 2.35, 7.6, 2.3, data, col_w=[1.8, 1.2, 1.3, 1.1, 1.2], size=10,
              head_size=8.5, ink=INK, muted=MUT, header_fill=PANEL, zebra=(PANEL, BG),
              align=['l', 'c', 'c', 'c', 'c'], font=BODY)
    kit.text(s, ML, 5.2, 7.5, 1.3, 'В узлах точна → по MSE не обогнать. Но 17 МБ, разрывные '
             'производные и 2,86 % нарушений уже в самой таблице.', size=11, color=INK,
             font=BODY, ls=1.45)
    panel(s, ML + 8.05, 2.35, 3.65, 3.15, FIG / 'size_speed.png', 'размер и время')
    kit.text(s, ML + 8.05, 5.65, 3.65, 0.6, 'Таблица проигрывает по памяти в 170 раз.', size=9,
             color=ACC, font=MONO)
    foot(s)
    kit.notes(s, STORY[7][3])

    # 8 — почему не таблица
    s = kit.slide(prs, BG)
    head(s, 8, title='Разрывы ломают производные', sub='')
    kit.text(s, ML, 2.25, 5.2, 1.6, '9,5 %', size=86, color=ACC, font=MONO, bold=True,
             tracking=-2.0)
    kit.text(s, ML, 4.05, 5.0, 1.1, 'узлов полной таблицы дают нефизичные производные: '
             'c_s² ≤ 0, ∂P/∂ρ ≤ 0 или ∂e/∂T ≤ 0', size=11.5, color=INK, font=BODY, ls=1.45)
    tint_photo(s, 'photo_micro.jpg', ML + 5.6, 2.3, 3.35, 2.9, focus=(0.5, 0.4), alpha=30)
    kit.text(s, ML + 5.6, 5.28, 3.35, 0.2, 'AL · MICROSTRUCTURE', size=7.5, color=MUT, font=MONO)
    kit.text(s, ML + 9.3, 2.3, 2.45, 3.6,
             ['ρ = 2,7 · T ≈ 140 К', 'e: 0,128 → 0,093', 'перепад 27 % за две ячейки',
              'c_s² < 0 — мнимое значение'],
             size=9.5, color=INK, font=MONO, ls=1.5, space_after=8)
    for i in range(4):
        kit.hrule(s, ML + 9.3, 3.05 + i * 0.72, 2.4, LINE, 0.75)
    foot(s)
    kit.notes(s, STORY[8][3])

    # 9 — vanilla
    s = kit.slide(prs, BG)
    head(s, 9, sub='2 → 128 → 128 → 64 → 2, tanh, 25 282 параметра, 150 эпох, OneCycle')
    panel(s, ML, 2.35, 7.3, 3.95, FIG / 'val_curves.png', 'train / test, MSE в нормированных единицах')
    for i, (k, v) in enumerate([('R²(P)', FACTS['r2_van']), ('MEDIAN P', FACTS['med_van']),
                                ('R²(E)', FACTS['r2e_van']), ('VIOLATIONS', FACTS['viol_van'])]):
        chip(s, ML + 7.55, 2.35 + i * 1.0, 3.85, v, k,
             ACC2 if i == 3 else ACC)
    foot(s)
    kit.notes(s, STORY[9][3])

    # 10 — PINN
    s = kit.slide(prs, BG)
    head(s, 10)
    xs = [(ML, 'INPUT', ['log₁₀ ρ', 'log₁₀ T']), (ML + 3.55, 'MLP', ['2→128→128', '→64→2']),
          (ML + 7.1, 'OUTPUT', ['log₁₀ P', 'e'])]
    for i, (x, tag, lines) in enumerate(xs):
        kit.rrect(s, x, 2.35, 3.0, 1.35, radius=0.1, fill=PANEL, line=ACC if i == 1 else LINE,
                  lw=1.0)
        kit.text(s, x + 0.22, 2.5, 2.4, 0.2, tag, size=7.5, color=ACC if i == 1 else MUT,
                 font=MONO, tracking=1.6)
        kit.text(s, x + 0.22, 2.8, 2.5, 0.8, lines, size=12, color=INK, font=MONO, ls=1.4)
        if i < 2:
            kit.text(s, x + 3.1, 2.85, 0.4, 0.3, '→', size=14, color=MUT, font=MONO)
    kit.rrect(s, ML, 4.0, 11.1, 1.55, radius=0.06, fill=None, line=ACC, lw=1.2)
    bracket(s, ML - 0.05, 3.95, 11.2, 1.65, ACC, 0.18)
    kit.text(s, ML + 0.3, 4.2, 9.6, 0.2, 'LOSS = L_DATA + γ · (L_STAB + L_CAP + L_CS)', size=9,
             color=ACC, font=MONO, tracking=1.2)
    kit.text(s, ML + 0.3, 4.52, 10.5, 0.9, 'autograd.grad по входам → цепное правило до СГС → '
             'ReLU-штрафы на ∂P/∂ρ, ∂e/∂T и c_s². γ = 0,03.', size=11, color=INK, font=BODY,
             ls=1.4)
    kit.text(s, ML, 5.8, 11.1, 0.7, 'Данные отвечают за точность, физика — за корректность '
             'производных.', size=10.5, color=MUT, font=BODY)
    foot(s)
    kit.notes(s, STORY[10][3])

    # 11 — физика
    s = kit.slide(prs, BG)
    head(s, 11)
    for i, (name, formula, why, penalty) in enumerate(CONSTRAINTS):
        y = 2.35 + i * 1.42
        kit.text(s, ML, y - 0.04, 0.5, 0.24, f'{i + 1:02d}', size=9, color=ACC, font=MONO)
        kit.text(s, ML + 0.5, y - 0.06, 3.6, 0.3, name, size=12.5, color=INK, font=BODY,
                 bold=True)
        kit.text(s, ML + 4.3, y - 0.04, 6.6, 0.34, formula, size=11, color=ACC, font=MONO)
        kit.text(s, ML + 0.5, y + 0.36, 10.5, 0.4, why, size=10, color=MUT, font=BODY, ls=1.35)
        kit.text(s, ML + 0.5, y + 0.84, 10.5, 0.24, penalty, size=8, color=MUT, font=MONO)
        kit.hrule(s, ML, y + 1.2, CW, LINE, 0.75)
    foot(s, 'system: cgs · checks run per point')
    kit.notes(s, STORY[11][3])

    # 12 — код
    s = kit.slide(prs, BG)
    head(s, 12)
    kit.code_block(s, ML, 2.35, 7.0, 4.15, CODE_LINES, bg=themes.C('070C18'), fg=INK,
                   cmt=MUT, accent=ACC, size=10, bar=ACC)
    for i, (k, v) in enumerate([('γ', '0,03 — больше ломает регрессию'),
                                ('scale', 'штраф делится на медиану |∂P/∂ρ|'),
                                ('mask', 'физика там, где таблица физична')]):
        y = 2.5 + i * 1.25
        kit.text(s, ML + 7.3, y, 3.9, 0.2, k.upper(), size=8, color=ACC, font=MONO, tracking=1.4)
        kit.text(s, ML + 7.3, y + 0.28, 3.9, 0.8, v, size=10.5, color=INK, font=BODY, ls=1.4)
        kit.hrule(s, ML + 7.3, y + 1.0, 3.6, LINE, 0.75)
    foot(s, 'physics loss · pytorch autograd')
    kit.notes(s, STORY[12][3])

    # 13 — обучение
    s = kit.slide(prs, BG)
    head(s, 13)
    for i, (tag, desc, res, note_) in enumerate([
            ('STAGE 1 · DATA', '150 эпох, OneCycle, MSE', 'R²(P) ≈ 0,999', 'быстро и устойчиво'),
            ('STAGE 2 · PHYSICS', 'γ = 0,03, маска, lr/10', f"{FACTS['viol_van']} → {FACTS['viol_pinn']}", 'чинит производные')]):
        x = ML + i * 5.85
        kit.rrect(s, x, 2.35, 5.35, 2.35, radius=0.06, fill=PANEL, line=LINE, lw=0.75)
        kit.rect(s, x, 2.35, 5.35, 0.04, fill=ACC if i == 0 else ACC2)
        kit.text(s, x + 0.28, 2.55, 4.8, 0.2, tag, size=8, color=ACC if i == 0 else ACC2,
                 font=MONO, tracking=1.6)
        kit.text(s, x + 0.28, 2.85, 4.8, 0.4, desc, size=11.5, color=INK, font=BODY)
        kit.text(s, x + 0.28, 3.35, 4.8, 0.45, res, size=20, color=INK, font=MONO, bold=True)
        kit.text(s, x + 0.28, 3.95, 4.8, 0.3, note_, size=9, color=MUT, font=BODY)
    kit.text(s, ML + 5.4, 2.9, 0.4, 0.3, '→', size=14, color=ACC, font=MONO)
    kit.text(s, ML, 5.05, 11.3, 1.4, 'Совместное обучение по двум лоссам сразу разваливало '
             'точность: градиенты физики забивали сигнал данных. Разделение этапов — главный '
             'инженерный приём работы. Повторная физическая стадия не улучшала результат.',
             size=11, color=INK, font=BODY, ls=1.45)
    foot(s)
    kit.notes(s, STORY[13][3])

    # 14 — результаты
    s = kit.slide(prs, BG)
    head(s, 14, sub='226 011 точек, все метрики посчитаны одним скриптом')
    data = [['ПОДХОД', 'R²(P)', 'МЕДИАНА P', 'P95 P', 'R²(E)', 'НАРУШЕНИЯ', 'РАЗМЕР', 'МКС'],
            ['Baseline', '1,00000', '0,000 %', '0,000 %', '1,00000', FACTS['viol_base'], FACTS['table_mb'] + ' МБ', '0,54'],
            ['Vanilla MLP', FACTS['r2_van'], FACTS['med_van'], FACTS['p95_van'], FACTS['r2e_van'], FACTS['viol_van'], '0,10 МБ', FACTS['us_van']],
            ['PINN', FACTS['r2_pinn'], FACTS['med_pinn'], FACTS['p95_pinn'], FACTS['r2e_pinn'], FACTS['viol_pinn'], '0,10 МБ', FACTS['us']]]
    kit.table(s, ML, 2.35, CW, 2.3, data, col_w=[2.5, 1.2, 1.3, 1.1, 1.2, 1.4, 1.2, 0.9],
              size=10, head_size=8, ink=INK, muted=MUT, header_fill=PANEL, zebra=(PANEL, BG),
              align=['l', 'c', 'c', 'c', 'c', 'c', 'c', 'c'], head_font=MONO, font=BODY)
    kit.text(s, ML, 5.15, 6.9, 1.2,
             f'Точность практически равна ({FACTS["med_van"]} против {FACTS["med_pinn"]}), '
             f'но нарушений в {FACTS["ratio"]} раза больше.', size=11, color=INK,
             font=BODY, ls=1.45)
    chip(s, ML + 7.3, 5.1, 1.75, FACTS['viol_pinn'], 'PINN')
    chip(s, ML + 9.25, 5.1, 1.9, FACTS['viol_van'], 'VANILLA', ACC2)
    foot(s)
    kit.notes(s, STORY[14][3])

    # 15 — ошибки
    s = kit.slide(prs, BG)
    head(s, 15)
    panel(s, ML, 2.35, 8.4, 3.95, FIG / 'error_maps.png', 'Vanilla слева, PINN справа · |ΔP| / P, %')
    for i, (k, v) in enumerate([('РАЗРЫВЫ', FACTS['err_jump']), ('ГЛАДКИЕ', FACTS['err_smooth']),
                                ('МЕДИАНА', FACTS['med_pinn']), ('ДОЛЯ РАЗРЫВОВ', FACTS['jump_frac'])]):
        y = 2.45 + i * 0.9
        kit.text(s, ML + 8.75, y, 2.4, 0.2, k, size=8, color=MUT, font=MONO, tracking=1.2)
        kit.text(s, ML + 8.75, y + 0.22, 2.4, 0.35, v, size=17, color=ACC, font=MONO, bold=True)
        kit.hrule(s, ML + 8.75, y + 0.72, 3.0, LINE, 0.75)
    foot(s)
    kit.notes(s, STORY[15][3])

    # 16 — нарушения
    s = kit.slide(prs, BG)
    head(s, 16)
    panel(s, ML, 2.35, 6.5, 3.95, FIG / 'violation_maps.png', 'карта нарушений по площади')
    panel(s, ML + 6.75, 2.35, 4.95, 2.2, FIG / 'violations_bar.png', 'нарушения по типам, %')
    tint_photo(s, 'photo_shock.jpg', ML + 6.75, 4.75, 4.95, 1.5, focus=(0.5, 0.5), alpha=35)
    kit.text(s, ML + 6.75, 6.35, 4.95, 0.2, 'SHOCK / INTERFERENCE — ILLUSTRATION', size=7,
             color=INK, font=MONO)
    foot(s)
    kit.notes(s, STORY[16][3])

    # 17 — скорость звука
    s = kit.slide(prs, BG)
    head(s, 17)
    panel(s, ML, 2.35, 7.4, 3.95, FIG / 'cs_scatter.png', 'c_s PINN против табличной, км/с')
    for i, (k, v) in enumerate([('R² LOG', FACTS['cs_r2']), ('МЕДИАНА', FACTS['cs_med']), ('P95', FACTS['cs_p95']),
                                ('c_s ≥ c', '0 %')]):
        y = 2.45 + i * 0.9
        kit.text(s, ML + 7.75, y, 2.2, 0.2, k, size=8, color=MUT, font=MONO, tracking=1.2)
        kit.text(s, ML + 7.75, y + 0.22, 2.6, 0.35, v, size=17, color=ACC, font=MONO, bold=True)
        kit.hrule(s, ML + 7.75, y + 0.72, 2.9, LINE, 0.75)
    foot(s)
    kit.notes(s, STORY[17][3])

    # 18 — обёртка
    s = kit.slide(prs, BG)
    head(s, 18, sub='Класс-обёртка, docstrings Google-style, проверка области определения')
    kit.code_block(s, ML, 2.35, 7.0, 4.15, WRAPPER_CODE, bg=themes.C('070C18'), fg=INK,
                   cmt=MUT, accent=ACC, size=10, bar=ACC)
    for i, (k, v) in enumerate([('predict', 'P и e батчем'), ('sound_speed', 'autograd, СГС'),
                                ('check_physics', 'маски и флаг ok'), ('in_domain', 'границы')]):
        y = 2.45 + i * 0.85
        kit.text(s, ML + 7.3, y, 2.0, 0.22, k, size=10, color=ACC, font=MONO, bold=True)
        kit.text(s, ML + 9.35, y, 2.1, 0.4, v, size=9, color=MUT, font=BODY, ls=1.3)
        kit.hrule(s, ML + 7.3, y + 0.62, 3.7, LINE, 0.75)
    kit.text(s, ML + 7.3, 6.0, 3.7, 0.3, '10⁵ запросов · 0,13 с', size=9, color=INK, font=MONO)
    foot(s)
    kit.notes(s, STORY[18][3])

    # 19 — сжатие
    s = kit.slide(prs, BG)
    head(s, 19)
    panel(s, ML, 2.35, 6.6, 3.95, FIG / 'size_speed.png', 'размер, МБ · мкс на запрос')
    data = [['ВАРИАНТ', 'РАЗМЕР', 'МКС'], ['fp32', '0,099 МБ', FACTS['fp32_us']],
            ['TorchScript', '0,107 МБ', FACTS['ts_us']], ['int8', '0,031 МБ', FACTS['int8_us']]]
    kit.table(s, ML + 6.9, 2.35, 3.9, 1.9, data, col_w=[1.6, 1.2, 0.8], size=9.5, head_size=8,
              ink=INK, muted=MUT, header_fill=PANEL, zebra=(PANEL, BG), align=['l', 'c', 'c'],
              font=BODY, head_font=MONO)
    kit.text(s, ML + 6.9, 4.45, 4.0, 1.9,
             ['TorchScript — ×1,6 к скорости batch-1.', 'int8 — веса в 3,2 раза меньше, '
              'p99 отклонения 0,031.', 'Для гидрокода выбираем TorchScript.'],
             size=9.5, color=MUT, font=BODY, ls=1.4, space_after=8)
    foot(s)
    kit.notes(s, STORY[19][3])

    # 20 — итоги
    s = kit.slide(prs, BG)
    grid_bg(s)
    kit.rect(s, 0, 0, kit.W, kit.H, fill=BG, transparency=35)
    kit.text(s, ML, 0.55, 2.0, 0.2, '20 / 20', size=9, color=ACC, font=MONO, tracking=1.6)
    kit.text(s, ML, 0.9, 10.5, 0.7, 'Физика под контролем', size=34, color=INK, font=H1,
             bold=True, tracking=-0.6)
    kit.hrule(s, ML, 1.7, CW, LINE, 0.75)
    cols = [('ВЫПОЛНЕНО', DONE), ('ОГРАНИЧЕНИЯ', LIMITS), ('ДАЛЬШЕ', NEXT)]
    for i, (t_, items) in enumerate(cols):
        x = ML + i * 3.9
        kit.text(s, x, 2.0, 3.5, 0.2, t_, size=8, color=ACC if i == 0 else MUT, font=MONO,
                 tracking=1.6)
        kit.hrule(s, x, 2.25, 3.55, LINE, 0.75)
        kit.bullets(s, x, 2.4, 3.5, 2.9, items, size=9.5, color=INK, font=BODY, gap=8,
                    bullet='▸', bullet_color=ACC, ls=1.4, bold_lead=False)
    tint_photo(s, 'photo_plasma.jpg', 0, 5.55, kit.W, 1.15, focus=(0.5, 0.45), alpha=40)
    kit.text(s, ML, 5.95, 11.0, 0.3, 'P(ρ,T) · e(ρ,T) · c_s · check_physics · 0,10 МБ',
             size=12, color=INK, font=MONO, bold=True)
    kit.text(s, ML, 6.35, 11.3, 0.3, ARTIFACTS, size=8, color=INK, font=MONO, ls=1.3)
    kit.notes(s, STORY[20][3])

    prs.save(out)
    return out


if __name__ == '__main__':
    print(build('presentation/04_Neon_data.pptx'))
