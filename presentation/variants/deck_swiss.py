"""Вариант 1 — Swiss / интернациональный типографический стиль. Без фотографий."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kit
import themes
from content import (ARTIFACTS, CHECKLIST, CODE_LINES, CONSTRAINTS, DONE, FACTS,
                     LIMITS, NEXT, STORY, WRAPPER_CODE, pct)

T = themes.SWISS
BG, INK, MUT, ACC, HAIR = T['bg'], T['ink'], T['muted'], T['accent'], T['hair']
H1, BODY, MONO = T['head'], T['body'], T['mono']
ML, MR = 0.9, 0.9
CW = kit.W - ML - MR
FIG = kit.LIGHT / 'swiss'


def head(s, num, kicker=None, title=None, sub=None, tight=False):
    kicker = kicker or STORY[num][0]
    title = title or STORY[num][1]
    sub = sub or STORY[num][2]
    kit.text(s, ML, 0.50, CW - 1.4, 0.22, kicker, size=9, color=MUT, font=MONO,
             caps=True, tracking=1.4)
    kit.text(s, kit.W - MR - 1.2, 0.50, 1.2, 0.22, f'{num:02d} / 20', size=9,
             color=MUT, font=MONO, align='r', tracking=0.8)
    kit.hrule(s, ML, 0.80, CW, INK, 1.4)
    kit.text(s, ML, 1.02, CW - 0.4, 0.62, title, size=31, color=INK, font=H1, bold=True,
             ls=0.98, tracking=-0.6)
    if sub:
        kit.text(s, ML, 1.86 if not tight else 1.80, CW - 1.2, 0.5, sub, size=13,
                 color=MUT, font=BODY, ls=1.25)


def foot(s, left='PINN · уравнение состояния алюминия'):
    kit.hrule(s, ML, 7.02, CW, HAIR, 1.0)
    kit.text(s, ML, 7.10, CW * 0.7, 0.2, left, size=8, color=MUT, font=MONO, caps=True,
             tracking=1.0)


def caption(s, x, y, w, text_):
    kit.text(s, x, y, w, 0.3, text_, size=9, color=MUT, font=MONO, ls=1.2)


def fig(s, path, x, y, w, h, cap=None):
    kit.rect(s, x, y, w, h, fill=None, line=HAIR, lw=1.0)
    kit.pic_fit(s, path, x + 0.14, y + 0.14, w - 0.28, h - 0.28 - (0.28 if cap else 0))
    if cap:
        caption(s, x, y + h - 0.26, w, cap)


def build(out):
    prs = kit.deck()

    # ---------------------------------------------------------------- 1
    s = kit.slide(prs, BG)
    kit.text(s, ML, 0.6, 8, 0.24, 'ИТ КоР · трек Machine Learning · кейс 01', size=10,
             color=ACC, font=MONO, caps=True, tracking=1.8)
    kit.hrule(s, ML, 1.02, CW, INK, 2.0)
    kit.text(s, ML, 1.32, CW - 0.2, 2.95,
             ['Физически согласованный', 'суррогат уравнения', 'состояния алюминия'],
             size=52, color=INK, font=H1, bold=True, ls=0.96, tracking=-1.4)
    kit.text(s, ML, 4.55, 7.6, 0.9,
             'PINN предсказывает P(ρ,T), e(ρ,T) и скорость звука c_s на 12 порядках давления '
             'и не нарушает термодинамику ни в одной из 226 011 точек теста.',
             size=14, color=INK, font=BODY, ls=1.35)
    kit.hrule(s, ML, 5.55, CW, HAIR, 1.0)
    kpis = [('0,43 %', 'нарушений физики у PINN'), (f"×{FACTS['ratio']}", 'реже, чем у нейросети без физики'),
            ('0,10 МБ', 'вес модели при лимите 10 МБ'), ('0,95 мкс', 'на запрос, batch 1')]
    for i, (v, l) in enumerate(kpis):
        x = ML + i * (CW / 4)
        kit.text(s, x, 5.78, CW / 4 - 0.3, 0.5, v, size=26, color=INK, font=H1, bold=True,
                 tracking=-0.8)
        kit.text(s, x, 6.36, CW / 4 - 0.35, 0.5, l, size=10, color=MUT, font=BODY, ls=1.2)
        if i:
            kit.vrule(s, x - 0.3, 5.78, 1.1, HAIR, 1.0)
    kit.text(s, ML, 7.08, 6.2, 0.2, 'Финальное задание · Росатом · 2026', size=9,
             color=MUT, font=MONO, caps=True, tracking=1.2)
    kit.text(s, kit.W - MR - 4.0, 7.08, 4.0, 0.2,
             'Автор: <имя> · команда: <состав>', size=9, color=MUT, font=MONO, align='r')
    kit.notes(s, STORY[1][3])

    # ---------------------------------------------------------------- 2
    s = kit.slide(prs, BG)
    head(s, 2)
    kit.text(s, ML, 2.42, 5.4, 1.9,
             'Нужен не «чёрный ящик», а согласованный с термодинамикой суррогат: '
             'гидрокод запрашивает не только P и e, но и производные — от них зависит '
             'устойчивость схемы.', size=15, color=INK, font=BODY, ls=1.45)
    rows = [
        ('01', 'Точность', 'Воспроизвести табличные P и e на всей фазовой диаграмме, а не в узлах сетки.'),
        ('02', 'Физика', 'Три знака-инварианта: ∂P/∂ρ > 0, ∂e/∂T > 0, 0 < c_s < c.'),
        ('03', 'Габарит', 'Модель не больше 10 МБ и время ответа — микросекунды.'),
    ]
    for i, (n, t_, d) in enumerate(rows):
        y = 2.45 + i * 1.42
        kit.text(s, ML + 5.85, y - 0.05, 0.8, 0.4, n, size=13, color=ACC, font=MONO, bold=True)
        kit.text(s, ML + 6.5, y - 0.06, 4.4, 0.3, t_, size=15, color=INK, font=H1, bold=True)
        kit.text(s, ML + 6.5, y + 0.36, 4.9, 0.8, d, size=11.5, color=MUT, font=BODY, ls=1.35)
        kit.hrule(s, ML + 5.85, y + 1.18, CW - 5.85, HAIR, 0.75)
    kit.vrule(s, ML + 5.5, 2.42, 4.2, HAIR, 1.0)
    foot(s)
    kit.notes(s, STORY[2][3])

    # ---------------------------------------------------------------- 3
    s = kit.slide(prs, BG)
    head(s, 3)
    kit.text(s, ML, 2.42, 6.0, 0.5, 'Чек-лист задания — 100 баллов; справа — чем закрыт каждый пункт.',
             size=12, color=MUT, font=BODY, ls=1.3)
    y = 2.95
    for i, (name, pts, what) in enumerate(CHECKLIST):
        if i == 5:
            y = 2.95
        x = ML if i < 5 else ML + 6.05
        yy = y + (i % 5) * 0.78
        kit.text(s, x, yy, 0.62, 0.28, pts, size=14, color=ACC, font=MONO, bold=True)
        kit.text(s, x + 0.66, yy - 0.03, 4.9, 0.28, name, size=12, color=INK, font=BODY, bold=True)
        kit.text(s, x + 0.66, yy + 0.25, 5.0, 0.3, what, size=9.5, color=MUT, font=BODY)
        kit.hrule(s, x, yy + 0.62, 5.5, HAIR, 0.75)
    kit.text(s, ML + 6.05, 6.72, 5.5, 0.24, 'Итого: 100 / 100', size=11, color=INK,
             font=MONO, bold=True, align='r')
    foot(s)
    kit.notes(s, STORY[3][3])

    # ---------------------------------------------------------------- 4
    s = kit.slide(prs, BG)
    head(s, 4, title='20 региональных сеток, 1 130 053 строки',
         sub='Четыре диапазона плотности × пять диапазонов температуры; внутри региона — регулярная сетка 300 × 300')
    vals = [('1 130 053', 'точки в датасете'), ('20', 'региональных сеток'),
            ('300 × 300', 'узлов в каждой'), ('226 011', 'точек в тесте')]
    for i, (v, l) in enumerate(vals):
        x = ML + i * (CW / 4)
        kit.text(s, x, 2.62, CW / 4 - 0.2, 0.64, v, size=27, color=INK, font=H1, bold=True,
                 tracking=-1.0)
        kit.hrule(s, x, 3.42, CW / 4 - 0.45, ACC, 2.0)
        kit.text(s, x, 3.56, CW / 4 - 0.35, 0.5, l, size=10.5, color=MUT, font=BODY, ls=1.25)
    kit.text(s, ML, 4.35, 6.4, 2.2,
             ['Данные пришли как 20 независимых таблиц: внутри региона гладко, на стыках — '
              'несогласованные значения P и e.',
              'Именно стыки дают разрывы производных, поэтому 9,5 % узлов полной сетки '
              'формально нефизичны ещё до всякой модели.'],
             size=12.5, color=INK, font=BODY, ls=1.4, space_after=14)
    box = [('4', 'диапазона ρ'), ('5', 'диапазонов T'), ('12', 'порядков P'), ('2', 'выхода: P, e')]
    for i, (v, l) in enumerate(box):
        y = 4.4 + i * 0.62
        kit.text(s, ML + 7.4, y, 0.6, 0.4, v, size=17, color=ACC, font=H1, bold=True)
        kit.text(s, ML + 8.05, y + 0.05, 3.0, 0.3, l, size=11, color=MUT, font=BODY)
    kit.vrule(s, ML + 7.05, 4.35, 2.5, HAIR, 1.0)
    foot(s)
    kit.notes(s, STORY[4][3])

    # ---------------------------------------------------------------- 5
    s = kit.slide(prs, BG)
    head(s, 5)
    fig(s, FIG / 'eda_maps.png', ML, 2.38, 8.3, 4.35,
        'log₁₀ P и e на полной сетке: давление — 12 порядков, энергия меняет знак')
    kit.text(s, ML + 8.7, 2.42, 2.85, 4.2,
             ['Давление меняется на 12 порядков — логарифмируем вход и выход.',
              'Энергия проходит через ноль — предсказываем её линейно, без логарифма.',
              'Скачки на картах — стыки регионов, а не шум данных.'],
             size=10.5, color=INK, font=BODY, ls=1.45, space_after=10)
    for i in range(3):
        kit.hrule(s, ML + 8.7, 2.42 + i * 1.4 + 1.18, 2.6, HAIR, 0.75)
    foot(s)
    kit.notes(s, STORY[5][3])

    # ---------------------------------------------------------------- 6
    s = kit.slide(prs, BG)
    head(s, 6)
    kit.text(s, ML, 2.42, 6.2, 1.1,
             'Все преобразования вынесены в normalization.json: проверяющая система '
             'воспроизводит инференс, не читая наш код.', size=14, color=INK, font=BODY, ls=1.4)
    steps = [('Вход', 'x = (log₁₀ρ − a) / (b − a)', 'log₁₀ρ ∈ [−3, 4] · log₁₀T ∈ [−1, 7]'),
             ('Выход P', 'log₁₀P, затем 10^', 'P ∈ [10⁻⁶, 10⁶] ГПа'),
             ('Выход e', 'линейно в кДж/г', 'e ∈ [−0,2, 10³] — есть отрицательные значения')]
    for i, (t_, f_, d) in enumerate(steps):
        x = ML + i * (CW / 3)
        kit.text(s, x, 3.75, 0.6, 0.24, f'0{i + 1}', size=11, color=ACC, font=MONO, bold=True)
        kit.text(s, x, 4.05, 3.1, 0.3, t_, size=15, color=INK, font=H1, bold=True)
        kit.hrule(s, x, 4.45, CW / 3 - 0.5, INK, 1.0)
        kit.text(s, x, 4.58, CW / 3 - 0.55, 0.4, f_, size=11, color=INK, font=MONO, ls=1.25)
        kit.text(s, x, 5.06, CW / 3 - 0.55, 0.9, d, size=10, color=MUT, font=BODY, ls=1.35)
    kit.text(s, ML, 6.2, CW, 0.4,
             'normalization.json — цифровой паспорт модели: константы, единицы, границы области определения.',
             size=10.5, color=MUT, font=BODY)
    foot(s)
    kit.notes(s, STORY[6][3])

    # ---------------------------------------------------------------- 7
    s = kit.slide(prs, BG)
    head(s, 7)
    data = [['Метрика', 'Полная таблица', 'decim2', 'decim4', 'decim8'],
            ['Размер, МБ', '17,2', '4,3', '1,1', '0,28'],
            ['Медианная ошибка P', '0,000 %', '0,0002 %', '0,0016 %', '0,0075 %'],
            ['Точек в сетке', '1 130 053', '283 183', '71 430', '18 077'],
            ['Покрытие области', '100 %', '99,4 %', '98,7 %', '96,7 %'],
            ['Нарушений физики', '2,86 %', '3,1 %', '4,4 %', '7,9 %']]
    kit.table(s, ML, 2.45, 7.4, 2.62, data, col_w=[2.4, 1.3, 1.0, 1.0, 1.0], size=10.5,
              head_size=9.5, ink=INK, muted=MUT, header_fill=None, zebra=None, line=HAIR,
              align=['l', 'c', 'c', 'c', 'c'], first_bold=True)
    for r in range(6):
        kit.hrule(s, ML, 2.45 + 0.437 * r, 7.4, HAIR, 0.75)
    kit.text(s, ML, 5.35, 7.4, 1.2,
             'Интерполяция точна в узлах, поэтому по MSE её не обогнать. Но таблица весит 17 МБ, '
             'её производные разрывны, а прореживание в 2 раза уже даёт 4,3 МБ.',
             size=11.5, color=INK, font=BODY, ls=1.4)
    kit.text(s, ML + 7.9, 2.45, 3.6, 2.4,
             ['Baseline — обязательный пункт чек-листа (5 баллов).',
              'Две роли: эталон точности в узлах и честный ориентир по памяти.',
              '20 интерполяторов RegularGridInterpolator, лог-сетка по ρ и T.'],
             size=10.5, color=MUT, font=BODY, ls=1.4, space_after=9)
    kit.vrule(s, ML + 7.6, 2.45, 4.1, HAIR, 1.0)
    foot(s)
    kit.notes(s, STORY[7][3])

    # ---------------------------------------------------------------- 8
    s = kit.slide(prs, BG)
    head(s, 8)
    kit.text(s, ML, 2.35, 5.2, 1.7, '9,5 %', size=84, color=ACC, font=H1, bold=True, tracking=-2.5,
             ls=0.95)
    kit.text(s, ML, 3.95, 4.6, 0.9, 'узлов полной таблицы дают нефизичные производные: '
             'c_s² ≤ 0, ∂P/∂ρ ≤ 0 или ∂e/∂T ≤ 0', size=13, color=INK, font=BODY, ls=1.35)
    kit.text(s, ML, 5.15, 5.2, 1.5,
             ['Причина — стыки 20 регионов и фазовые переходы: таблица хранит значения, '
              'но не гарантирует гладкость между узлами.',
              'Гладкая сеть сглаживает эти скачки и возвращает корректные производные — '
              'ценой небольшой потери точности.'],
             size=11.5, color=MUT, font=BODY, ls=1.4, space_after=10)
    kit.vrule(s, ML + 5.7, 2.45, 3.9, HAIR, 1.0)
    kit.text(s, ML + 6.1, 2.45, 5.3, 0.3, 'ОДИН ШАГ ПО ПЛОТНОСТИ', size=9, color=ACC,
             font=MONO, caps=True, tracking=1.4)
    kit.text(s, ML + 6.1, 2.85, 5.4, 0.4, 'ρ = 2,7 г/см³, T ≈ 140 К', size=15, color=INK,
             font=H1, bold=True)
    kit.hrule(s, ML + 6.1, 3.35, 5.3, HAIR, 1.0)
    pairs = [('e при ρ − δ', '0,128 кДж/г', MUT), ('e при ρ + δ', '0,093 кДж/г', MUT),
             ('перепад', '27 % за две ячейки', ACC), ('c_s² в точке', '< 0 — мнимое значение', ACC)]
    for i, (k, v, c) in enumerate(pairs):
        y = 3.55 + i * 0.72
        kit.text(s, ML + 6.1, y, 2.5, 0.3, k, size=10.5, color=MUT, font=BODY)
        kit.text(s, ML + 8.5, y - 0.04, 3.0, 0.3, v, size=12, color=c, font=MONO, bold=True,
                 align='r')
        kit.hrule(s, ML + 6.1, y + 0.5, 5.3, HAIR, 0.75)
    foot(s)
    kit.notes(s, STORY[8][3])

    # ---------------------------------------------------------------- 9
    s = kit.slide(prs, BG)
    head(s, 9)
    fig(s, FIG / 'val_curves.png', ML, 2.42, 6.5, 4.3,
        'Vanilla MLP: кривые train/test, 150 эпох, OneCycle')
    kit.text(s, ML + 6.9, 2.42, 4.6, 0.3, 'VANILLA MLP', size=9, color=ACC, font=MONO,
             caps=True, tracking=1.4)
    kit.text(s, ML + 6.9, 2.75, 4.6, 0.9,
             '2 → 128 → 128 → 64 → 2, tanh, 25 282 параметра', size=12, color=INK,
             font=BODY, ls=1.35)
    rows = [('R²(P)', f"{FACTS['r2_van']}".replace('.', ',')), ('медианная ошибка P', FACTS['med_van']),
            ('R²(e)', FACTS['r2e_van']), ('нарушений физики', FACTS['viol_van'])]
    for i, (k, v) in enumerate(rows):
        y = 3.75 + i * 0.62
        kit.text(s, ML + 6.9, y, 2.7, 0.3, k, size=10, color=MUT, font=BODY)
        kit.text(s, ML + 9.6, y - 0.05, 1.9, 0.3, v, size=13, color=INK, font=MONO, bold=True,
                 align='r')
        kit.hrule(s, ML + 6.9, y + 0.45, 4.3, HAIR, 0.75)
    kit.text(s, ML + 6.9, 6.35, 4.4, 0.5, 'Точность высокая — физика разрушена.', size=11.5,
             color=ACC, font=BODY, bold=True)
    foot(s)
    kit.notes(s, STORY[9][3])

    # ---------------------------------------------------------------- 10
    s = kit.slide(prs, BG)
    head(s, 10)
    boxes = [(ML, 'Вход', ['log₁₀ ρ', 'log₁₀ T']), (ML + 3.5, 'MLP', ['2 → 128 → 128', '→ 64 → 2, tanh']),
             (ML + 7.0, 'Выход', ['log₁₀ P', 'e, кДж/г'])]
    for i, (x, t_, lines) in enumerate(boxes):
        kit.rect(s, x, 2.55, 2.8, 1.55, fill=None, line=INK, lw=1.2)
        kit.text(s, x + 0.22, 2.72, 2.4, 0.24, t_, size=9, color=MUT, font=MONO, caps=True,
                 tracking=1.4)
        kit.text(s, x + 0.22, 3.05, 2.4, 0.9, lines, size=13, color=INK, font=BODY, ls=1.3)
        if i < 2:
            kit.text(s, x + 2.95, 3.05, 0.45, 0.4, '→', size=20, color=ACC, font=BODY, bold=True)
    kit.rect(s, ML, 4.55, 11.5, 1.55, fill=None, line=ACC, lw=1.4)
    kit.text(s, ML + 0.3, 4.75, 5.5, 0.24, 'ФИЗИЧЕСКИЙ ЛОСС — ТОЛЬКО ЧЕРЕЗ ПРОИЗВОДНЫЕ',
             size=9, color=ACC, font=MONO, caps=True, tracking=1.4)
    kit.text(s, ML + 0.3, 5.08, 10.9, 0.9,
             'autograd.grad по входам → цепное правило до СГС → три ReLU-штрафа: '
             '∂P/∂ρ, ∂e/∂T и c_s² − c². Данные дают точность, физика — корректность; '
             'вес γ балансирует вклад.', size=12.5, color=INK, font=BODY, ls=1.4)
    kit.text(s, ML, 6.35, 11.5, 0.5,
             'L = L_data + γ · (L_stab + L_cap + L_cs),  γ = 0,03', size=13, color=INK,
             font=MONO, bold=True)
    foot(s)
    kit.notes(s, STORY[10][3])

    # ---------------------------------------------------------------- 11
    s = kit.slide(prs, BG)
    head(s, 11)
    for i, (name, formula, why, penalty) in enumerate(CONSTRAINTS):
        y = 2.45 + i * 1.5
        kit.text(s, ML, y, 0.55, 0.3, f'0{i + 1}', size=13, color=ACC, font=MONO, bold=True)
        kit.text(s, ML + 0.62, y - 0.06, 4.3, 0.3, name, size=13, color=INK, font=H1, bold=True)
        kit.text(s, ML + 5.1, y - 0.02, 6.0, 0.4, formula, size=11.5, color=INK, font=MONO)
        kit.text(s, ML + 0.62, y + 0.38, 11.0, 0.6, why, size=11, color=MUT, font=BODY, ls=1.3)
        kit.text(s, ML + 0.62, y + 0.92, 11.0, 0.28, penalty, size=9.5, color=MUT, font=MONO)
        kit.hrule(s, ML, y + 1.28, CW, HAIR, 0.75)
    foot(s, 'Проверки выполняются в системе СГС — как в гидрокоде')
    kit.notes(s, STORY[11][3])

    # ---------------------------------------------------------------- 12
    s = kit.slide(prs, BG)
    head(s, 12)
    kit.text(s, ML, 2.4, 5.4, 1.4,
             'Производные считаются в том же графе вычислений: штраф не требует '
             'ни численного дифференцирования, ни второй сети.', size=13, color=INK,
             font=BODY, ls=1.4)
    tips = [('γ = 0,03', 'больше — физика ломает регрессию'),
            ('масштаб', 'штраф делится на медиану |∂P/∂ρ|'),
            ('маска разрывов', 'физику считаем только там, где таблица физична')]
    for i, (k, v) in enumerate(tips):
        y = 4.15 + i * 0.78
        kit.text(s, ML, y, 1.5, 0.3, k, size=10, color=ACC, font=MONO, bold=True)
        kit.text(s, ML + 1.6, y, 4.0, 0.6, v, size=10.5, color=MUT, font=BODY, ls=1.3)
    kit.code_block(s, ML + 6.0, 2.4, 5.55, 4.25, CODE_LINES, bg=themes.C('F4F4F4'), fg=INK,
                   cmt=themes.C('8A8A8A'), accent=ACC, size=9.5, bar=ACC)
    foot(s, 'Фрагмент physics-лосса · PyTorch')
    kit.notes(s, STORY[12][3])

    # ---------------------------------------------------------------- 13
    s = kit.slide(prs, BG)
    head(s, 13)
    stages = [('Этап 1', 'Данные', '150 эпох, OneCycle, MSE в нормированных единицах',
               'R²(P) 0,999', 'быстро и устойчиво'),
              ('Этап 2', 'Физика', 'та же сеть, γ = 0,03, маска разрывов, lr = 1/10',
               'нарушения 36 % → 0,4 %', 'медленно, но чинит производные')]
    for i, (tag, name, desc, res, note_) in enumerate(stages):
        x = ML + i * 6.0
        kit.text(s, x, 2.45, 1.4, 0.24, tag, size=9, color=ACC, font=MONO, caps=True,
                 tracking=1.4)
        kit.text(s, x, 2.78, 5.4, 0.5, name, size=26, color=INK, font=H1, bold=True,
                 tracking=-0.6)
        kit.hrule(s, x, 3.4, 5.4, INK, 1.4)
        kit.text(s, x, 3.58, 5.3, 1.0, desc, size=11.5, color=MUT, font=BODY, ls=1.4)
        kit.text(s, x, 4.55, 5.3, 0.4, res, size=15, color=INK, font=MONO, bold=True)
        kit.text(s, x, 5.0, 5.3, 0.4, note_, size=10, color=MUT, font=BODY)
    kit.text(s, ML + 5.55, 2.7, 0.45, 0.4, '→', size=22, color=ACC, font=BODY, bold=True)
    kit.text(s, ML, 5.95, CW, 0.9,
             'Совместное обучение сразу по двум лоссам разваливало точность: градиенты физики '
             'забивали сигнал данных. Разделение этапов — главный инженерный приём работы.',
             size=11.5, color=INK, font=BODY, ls=1.4)
    foot(s)
    kit.notes(s, STORY[13][3])

    # ---------------------------------------------------------------- 14
    s = kit.slide(prs, BG)
    head(s, 14)
    data = [['Подход', 'R²(P)', 'Медиана P', 'p95 P', 'R²(e)', 'Нарушения', 'Размер', 'мкс'],
            ['Baseline (таблица)', '1,00000', '0,000 %', '0,000 %', '1,00000', FACTS['viol_base'], FACTS['table_mb'] + ' МБ', '0,54'],
            ['Vanilla MLP', FACTS['r2_van'], FACTS['med_van'], FACTS['p95_van'], FACTS['r2e_van'], FACTS['viol_van'], '0,10 МБ', FACTS['us_van']],
            ['PINN', FACTS['r2_pinn'], FACTS['med_pinn'], FACTS['p95_pinn'], FACTS['r2e_pinn'], FACTS['viol_pinn'], '0,10 МБ', FACTS['us']]]
    kit.table(s, ML, 2.45, CW, 2.4, data, col_w=[2.6, 1.2, 1.3, 1.1, 1.2, 1.3, 1.2, 0.9],
              size=11, head_size=9.5, ink=INK, muted=MUT, header_fill=None, zebra=None,
              align=['l', 'c', 'c', 'c', 'c', 'c', 'c', 'c'])
    for r in range(5):
        kit.hrule(s, ML, 2.45 + 0.46 * r, CW, HAIR, 0.75)
    kit.hrule(s, ML, 2.45 + 0.46 * 4, CW, INK, 1.2)
    kit.text(s, ML, 5.4, 7.5, 1.2,
             f'Точность практически равна: {FACTS["med_van"]} против {FACTS["med_pinn"]} по '
             f'медиане. Но нарушений {FACTS["viol_van"]} против {FACTS["viol_pinn"]} — '
             f'в {FACTS["ratio"]} раза больше.',
             size=11.5, color=INK, font=BODY, ls=1.4)
    kit.text(s, ML + 7.9, 5.35, 3.6, 1.2,
             ['Одна и та же тестовая выборка — 226 011 точек.',
              'Размер — файл весов; мкс — batch 1 на CPU.'],
             size=9.5, color=MUT, font=BODY, ls=1.35, space_after=8)
    foot(s, '226 011 точек теста · 20 % стратифицированной выборки')
    kit.notes(s, STORY[14][3])

    # ---------------------------------------------------------------- 15
    s = kit.slide(prs, BG)
    head(s, 15)
    fig(s, FIG / 'error_maps.png', ML, 2.4, 7.7, 4.35,
        'Относительная ошибка P, % — 240 × 320 точек по всей диаграмме')
    kit.text(s, ML + 8.05, 2.42, 3.4, 0.3, 'ГДЕ ОШИБКА', size=9, color=ACC, font=MONO,
             caps=True, tracking=1.4)
    kit.text(s, ML + 8.05, 2.78, 3.45, 1.2,
             'Ошибка концентрируется узкой полосой вдоль разрывов — там она в 1,7 раза выше, '
             'чем в гладких зонах.', size=11, color=INK, font=BODY, ls=1.4)
    rows = [(f"разрывы ({FACTS['jump_frac']})", FACTS['err_jump']), ('гладкие зоны', FACTS['err_smooth']), ('медиана по всем', FACTS['med_pinn'])]
    for i, (k, v) in enumerate(rows):
        y = 4.15 + i * 0.6
        kit.text(s, ML + 8.05, y, 2.6, 0.3, k, size=10, color=MUT, font=BODY)
        kit.text(s, ML + 10.7, y - 0.04, 0.8, 0.3, v, size=12, color=INK, font=MONO,
                 bold=True, align='r')
        kit.hrule(s, ML + 8.05, y + 0.44, 3.45, HAIR, 0.75)
    foot(s, 'Честная граница гладкой регрессии: разрыв таблицы нельзя выучить без потерь')
    kit.notes(s, STORY[15][3])

    # ---------------------------------------------------------------- 16
    s = kit.slide(prs, BG)
    head(s, 16)
    fig(s, FIG / 'violation_maps.png', ML, 2.4, 7.6, 4.35,
        'Флаги нарушений по площади диаграммы: слева Vanilla, справа PINN')
    kit.text(s, ML + 8.0, 2.42, 3.5, 0.3, 'ЧТО СЧИТАЕТСЯ НАРУШЕНИЕМ', size=9, color=ACC,
             font=MONO, caps=True, tracking=1.4)
    items = [('∂P/∂ρ ≤ 0', f"{FACTS['van_stab']} → {FACTS['pinn_stab']}"),
             ('∂e/∂T ≤ 0', f"{FACTS['van_cap']} → {FACTS['pinn_cap']}"),
             ('c_s² ≤ 0', f"{FACTS['van_cs']} → {FACTS['pinn_cs']}"),
             ('c_s ≥ c', '0 % в обеих моделях')]
    for i, (k, v) in enumerate(items):
        y = 2.8 + i * 0.72
        kit.text(s, ML + 8.0, y, 1.6, 0.3, k, size=11, color=INK, font=MONO, bold=True)
        kit.text(s, ML + 9.7, y, 1.85, 0.3, v, size=10, color=MUT, font=MONO, align='r')
        kit.hrule(s, ML + 8.0, y + 0.5, 3.5, HAIR, 0.75)
    kit.text(s, ML + 8.0, 5.9, 3.5, 0.9,
             'Vanilla: 40 % площади. PINN: 0,7 % — тонкая полоса на стыке регионов, '
             'где разрывна сама таблица.', size=10.5, color=INK, font=BODY, ls=1.35)
    foot(s, 'check_physics: те же три предиката, что и в лоссе')
    kit.notes(s, STORY[16][3])

    # ---------------------------------------------------------------- 17
    s = kit.slide(prs, BG)
    head(s, 17)
    fig(s, FIG / 'cs_scatter.png', ML, 2.4, 5.6, 4.35,
        'c_s PINN против табличной c_s, км/с (log–log)')
    kit.text(s, ML + 6.0, 2.42, 5.5, 0.3, 'САМАЯ ЧУВСТВИТЕЛЬНАЯ ВЕЛИЧИНА', size=9, color=ACC,
             font=MONO, caps=True, tracking=1.4)
    kit.text(s, ML + 6.0, 2.78, 5.3, 1.2,
             'Скорость звука зависит от трёх производных сразу, поэтому расхождение с таблицей '
             'здесь максимально.', size=11.5, color=INK, font=BODY, ls=1.4)
    rows = [('R² в лог-шкале', FACTS['cs_r2']), ('медианное отклонение', FACTS['cs_med']),
            ('p95 отклонения', FACTS['cs_p95']), ('точек с c_s ≥ c', '0 %')]
    for i, (k, v) in enumerate(rows):
        y = 4.15 + i * 0.6
        kit.text(s, ML + 6.0, y, 3.4, 0.3, k, size=10, color=MUT, font=BODY)
        kit.text(s, ML + 9.9, y - 0.04, 1.5, 0.3, v, size=12, color=INK, font=MONO,
                 bold=True, align='r')
        kit.hrule(s, ML + 6.0, y + 0.44, 5.4, HAIR, 0.75)
    foot(s, 'Расхождения — там, где табличная c_s не определена (разрывы)')
    kit.notes(s, STORY[17][3])

    # ---------------------------------------------------------------- 18
    s = kit.slide(prs, BG)
    head(s, 18)
    kit.code_block(s, ML, 2.4, 6.3, 4.2, WRAPPER_CODE, bg=themes.C('F4F4F4'), fg=INK, cmt=themes.C('8A8A8A'),
                   accent=ACC, size=10, bar=ACC)
    kit.text(s, ML + 6.75, 2.42, 4.7, 0.3, 'EOSSURROGATE', size=9, color=ACC, font=MONO,
             caps=True, tracking=1.4)
    kit.text(s, ML + 6.75, 2.78, 4.7, 1.2,
             'Класс-обёртка на 90 строк: docstrings в Google-style, валидация области '
             'определения, батчевый инференс.', size=11.5, color=INK, font=BODY, ls=1.4)
    items = [('predict', 'векторный инференс P и e'),
             ('sound_speed', 'autograd внутри, СГС на выходе'),
             ('check_physics', 'маски нарушений и флаг ok'),
             ('in_domain', 'границы области определения')]
    for i, (k, v) in enumerate(items):
        y = 4.2 + i * 0.6
        kit.text(s, ML + 6.75, y, 1.7, 0.3, k, size=11, color=INK, font=MONO, bold=True)
        kit.text(s, ML + 8.55, y, 2.9, 0.3, v, size=10, color=MUT, font=BODY)
        kit.hrule(s, ML + 6.75, y + 0.44, 4.7, HAIR, 0.75)
    foot(s, '10⁵ запросов — 0,13 с на CPU')
    kit.notes(s, STORY[18][3])

    # ---------------------------------------------------------------- 19
    s = kit.slide(prs, BG)
    head(s, 19)
    fig(s, FIG / 'size_speed.png', ML, 2.4, 6.9, 4.3,
        'Размер весов и время одиночного запроса (log-шкала для размеров)')
    data = [['Вариант', 'Размер', 'мкс'],
            ['fp32', '0,099 МБ', FACTS['fp32_us']],
            ['TorchScript', '0,107 МБ', FACTS['ts_us']],
            ['int8 (dynamic)', '0,031 МБ', FACTS['int8_us']]]
    kit.table(s, ML + 7.3, 2.55, 4.2, 1.9, data, col_w=[1.9, 1.2, 0.9], size=10.5,
              head_size=9, ink=INK, muted=MUT, header_fill=None, zebra=None,
              align=['l', 'c', 'c'])
    for r in range(4):
        kit.hrule(s, ML + 7.3, 2.55 + 0.46 * r, 4.2, HAIR, 0.75)
    kit.text(s, ML + 7.3, 4.75, 4.3, 1.9,
             ['TorchScript ускоряет batch-1 в 1,6 раза без потери точности.',
              'int8 сжимает веса в 3,2 раза: p99 отклонения 0,031 в нормированных единицах.',
              'Для ансамбля гидрокода выбираем TorchScript: скорость важнее размера.'],
             size=10, color=MUT, font=BODY, ls=1.4, space_after=8)
    kit.vrule(s, ML + 7.05, 2.5, 4.1, HAIR, 1.0)
    foot(s)
    kit.notes(s, STORY[19][3])

    # ---------------------------------------------------------------- 20
    s = kit.slide(prs, BG)
    head(s, 20)
    cols = [('Сделано', DONE, INK), ('Ограничения', LIMITS, MUT), ('Дальше', NEXT, INK)]
    for i, (t_, items, c) in enumerate(cols):
        x = ML + i * (CW / 3)
        kit.text(s, x, 2.45, 3.2, 0.26, t_, size=9, color=ACC if i == 0 else MUT, font=MONO,
                 caps=True, tracking=1.6)
        kit.hrule(s, x, 2.78, CW / 3 - 0.5, INK if i == 0 else HAIR, 1.2)
        kit.bullets(s, x, 2.95, CW / 3 - 0.55, 3.2, items, size=10, color=c, font=BODY,
                    gap=9, bullet='—', bullet_color=ACC, lead_color=INK, bold_lead=False,
                    ls=1.35)
    kit.hrule(s, ML, 6.05, CW, INK, 1.4)
    kit.text(s, ML, 6.2, 7.4, 0.3, 'Артефакты', size=9, color=MUT, font=MONO, caps=True,
             tracking=1.4)
    kit.text(s, ML, 6.45, 11.5, 0.5, ARTIFACTS, size=9.5, color=INK, font=MONO, ls=1.4)
    kit.notes(s, STORY[20][3])

    prs.save(out)
    return out


if __name__ == '__main__':
    print(build('presentation/01_Swiss_типографика.pptx'))
