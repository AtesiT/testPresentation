"""Вариант 2 — Industrial / тёмный фото-арт-дирекшн. Максимум фотографий."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kit
import themes
from content import (ARTIFACTS, CHECKLIST, CODE_LINES, CONSTRAINTS, DONE, FACTS,
                     LIMITS, NEXT, STORY, WRAPPER_CODE)

T = themes.INDUSTRIAL
BG, PANEL, INK, MUT = T['bg'], T['panel'], T['ink'], T['muted']
ACC, ACC2, HAIR, LINE = T['accent'], T['accent2'], T['hair'], T['line']
H1, BODY, MONO = T['head'], T['body'], T['mono']
ML, MR = 0.85, 0.85
CW = kit.W - ML - MR
FIG = kit.LIGHT / 'industrial'
IMG = kit.ASSETS


def hero(s, photo, scrim=48, focus=(0.5, 0.5)):
    kit.pic_cover(s, IMG / photo, 0, 0, kit.W, kit.H, focus=focus)
    kit.rect(s, 0, 0, kit.W, kit.H, fill=themes.C('0B0907'), transparency=scrim)


def ticks(s, color=None, m=0.42, L=0.42):
    color = color or ACC
    for x, y in ((m, m), (kit.W - m - L, m), (m, kit.H - m - 0.03), (kit.W - m - L, kit.H - m - 0.03)):
        kit.hrule(s, x, y, L, color, 1.4)


def head(s, num, title=None, sub=None, kicker=None):
    kit.text(s, ML, 0.52, 7.0, 0.24, (kicker or STORY[num][0]).upper(), size=9.5, color=ACC,
             font=MONO, tracking=2.2)
    kit.text(s, kit.W - MR - 1.6, 0.5, 1.6, 0.26, f'{num:02d}', size=15, color=MUT,
             font=MONO, bold=True, align='r')
    kit.text(s, kit.W - MR - 1.6, 0.78, 1.6, 0.2, f'— 20', size=8.5, color=LINE, font=MONO,
             align='r')
    kit.hrule(s, ML, 0.86, CW, LINE, 1.0)
    kit.text(s, ML, 1.06, CW - 0.3, 0.72, title or STORY[num][1], size=29, color=INK,
             font=H1, bold=True, ls=0.98, tracking=-0.8)
    sub = STORY[num][2] if sub is None else sub
    if sub:
        kit.text(s, ML, 1.84, CW - 1.5, 0.5, sub, size=12, color=MUT, font=BODY, ls=1.3)


def foot(s, left='PINN · уравнение состояния алюминия'):
    kit.hrule(s, ML, 7.03, CW, LINE, 1.0)
    kit.text(s, ML, 7.12, CW * 0.72, 0.2, left.upper(), size=8.5, color=MUT, font=MONO,
             tracking=1.4)


def panel(s, x, y, w, h, cap=None):
    """Экранная панель под тёмный график (фон графиков — #0B1220)."""
    kit.rect(s, x, y, w, h, fill=themes.C('121010'), line=LINE, lw=1.0)
    if cap:
        kit.text(s, x + 0.12, y + h - 0.28, w - 0.24, 0.22, cap, size=8, color=MUT, font=MONO)


def build(out):
    prs = kit.deck()

    # 1 — обложка на фото слитков
    s = kit.slide(prs, BG)
    hero(s, 'photo_ingots.jpg', scrim=54, focus=(0.5, 0.45))
    ticks(s)
    kit.text(s, ML, 1.5, 8.6, 0.3, 'ИТ КоР · ТРЕК ML · КЕЙС 01 · АЛЮМИНИЙ', size=10,
             color=ACC, font=MONO, tracking=2.6)
    kit.text(s, ML, 1.95, 10.6, 2.4,
             ['СУРРОГАТ УРАВНЕНИЯ', 'СОСТОЯНИЯ, КОТОРЫЙ', 'НЕ ЛОМАЕТ ФИЗИКУ'],
             size=46, color=INK, font=H1, bold=True, ls=1.0, tracking=-1.0)
    kit.rect(s, ML, 4.55, 1.5, 0.05, fill=ACC)
    kit.text(s, ML, 4.85, 7.3, 0.9, 'PINN вместо таблицы: P(ρ,T), e(ρ,T) и c_s на 12 порядках '
             'давления, 0,10 МБ, 0,95 мкс на запрос.', size=14, color=INK, font=BODY, ls=1.35)
    nums = [(FACTS['viol_pinn'], 'нарушений физики'), (f"×{FACTS['ratio']}", 'лучше нейросети без физики'),
            ('0,10 МБ', 'вес модели'), ('226 011', 'точек теста')]
    for i, (v, l) in enumerate(nums):
        x = ML + i * 3.0
        kit.text(s, x, 6.0, 2.8, 0.5, v, size=26, color=ACC, font=H1, bold=True,
                 tracking=-0.8)
        kit.text(s, x, 6.62, 2.75, 0.3, l.upper(), size=8.5, color=MUT, font=MONO, tracking=1.2)
    kit.notes(s, STORY[1][3])

    # 2 — постановка, фото заливки слева
    s = kit.slide(prs, BG)
    kit.pic_cover(s, IMG / 'photo_molten.jpg', 0, 0, 4.55, kit.H, focus=(0.45, 0.5))
    kit.rect(s, 0, 0, 4.55, kit.H, fill=themes.C('0B0907'), transparency=35)
    kit.rect(s, 4.55, 0, 0.04, kit.H, fill=ACC)
    for i, (n, t_, d) in enumerate([
            ('01', 'Точность', 'Воспроизвести P и e по всей диаграмме, а не только в узлах сетки.'),
            ('02', 'Физика', '∂P/∂ρ > 0, ∂e/∂T > 0 и 0 < c_s < c — в каждой точке.'),
            ('03', 'Габарит', 'Модель до 10 МБ, ответ за микросекунды, без GPU.')]):
        y = 1.35 + i * 1.75
        kit.text(s, 5.3, y, 0.8, 0.4, n, size=13, color=ACC, font=MONO, bold=True)
        kit.text(s, 6.1, y - 0.08, 6.0, 0.36, t_, size=20, color=INK, font=H1, bold=True)
        kit.text(s, 6.1, y + 0.42, 6.2, 0.9, d, size=12, color=MUT, font=BODY, ls=1.4)
        kit.hrule(s, 5.3, y + 1.28, 7.0, HAIR, 1.0)
    kit.text(s, 5.3, 6.55, 7.2, 0.4, 'Гидрокоду нужны производные: от них зависит устойчивость схемы.',
             size=10.5, color=INK, font=MONO)
    kit.notes(s, STORY[2][3])

    # 3 — чек-лист
    s = kit.slide(prs, BG)
    kit.pic_cover(s, IMG / 'photo_micro.jpg', kit.W - 3.1, 0, 3.1, kit.H, focus=(0.5, 0.4))
    kit.rect(s, kit.W - 3.1, 0, 3.1, kit.H, fill=themes.C('0B0907'), transparency=30)
    head(s, 3, sub='Структура ответа повторяет финальное задание: 9 критериев на 100 баллов')
    kit.vrule(s, kit.W - 3.1, 0, kit.H, ACC, 1.2)
    for i, (name, pts, what) in enumerate(CHECKLIST):
        y = 2.36 + i * 0.46
        kit.text(s, ML, y, 0.6, 0.24, pts, size=12.5, color=ACC, font=MONO, bold=True)
        kit.text(s, ML + 0.7, y - 0.02, 3.7, 0.26, name, size=11.5, color=INK, font=BODY,
                 bold=True)
        kit.text(s, ML + 4.5, y, 4.5, 0.26, what, size=9.5, color=MUT, font=BODY)
        kit.hrule(s, ML, y + 0.38, 8.9, HAIR, 0.75)
    kit.text(s, ML, 6.55, 8.9, 0.3, 'ИТОГО 100 / 100 — ПОДТВЕРЖДЕНО АРТЕФАКТАМИ В РЕПОЗИТОРИИ',
             size=9.5, color=ACC, font=MONO, tracking=1.2)
    foot(s)
    kit.notes(s, STORY[3][3])

    # 4 — данные
    s = kit.slide(prs, BG)
    hero(s, 'photo_plasma.jpg', scrim=70, focus=(0.5, 0.5))
    head(s, 4, title='20 сеток, 1 130 053 строки',
         sub='Четыре диапазона ρ × пять диапазонов T; внутри региона — регулярная сетка 300 × 300')
    kit.hrule(s, ML, 2.35, CW * 0.55, ACC, 2.0)
    for i, (v, l) in enumerate([('1 130 053', 'точки датасета'), ('20', 'региональных сеток'),
                                ('300 × 300', 'узлов в каждой'), ('9,5 %', 'узлов с нефизичными производными')]):
        y = 2.75 + i * 0.98
        kit.text(s, ML, y, 3.4, 0.62, v, size=30, color=INK, font=H1, bold=True, tracking=-0.8)
        kit.text(s, ML + 3.6, y + 0.12, 3.0, 0.4, l, size=11, color=MUT, font=BODY, ls=1.2)
    kit.text(s, ML + 7.0, 2.75, 4.6, 3.4,
             ['Регионы не согласованы между собой: на стыках P и e скачут.',
              'Отсюда разрывы производных — и главная сложность задачи.',
              'Тест — 20 % стратифицированной выборки, 226 011 точек.'],
             size=11.5, color=INK, font=BODY, ls=1.5, space_after=12)
    kit.notes(s, STORY[4][3])

    # 5 — EDA
    s = kit.slide(prs, BG)
    head(s, 5)
    panel(s, ML, 2.4, 8.5, 3.95, 'log₁₀ P и знаковый логарифм e на полной сетке')
    kit.pic_fit(s, FIG / 'eda_maps.png', ML + 0.12, 2.5, 8.26, 3.4)
    kit.text(s, ML + 8.85, 2.45, 2.5, 0.25, 'ЧТО ВИДНО', size=8.5, color=ACC, font=MONO,
             tracking=1.8)
    kit.text(s, ML + 8.85, 2.8, 2.55, 3.3,
             ['Давление — 12 порядков: логарифмируем вход и выход.',
              'Энергия проходит через ноль: предсказываем линейно.',
              'Белые полосы — стыки регионов.'],
             size=10, color=INK, font=BODY, ls=1.4, space_after=10)
    foot(s)
    kit.notes(s, STORY[5][3])

    # 6 — нормализация
    s = kit.slide(prs, BG)
    kit.pic_cover(s, IMG / 'photo_network.jpg', kit.W - 4.2, 0, 4.2, kit.H, focus=(0.4, 0.5))
    kit.rect(s, kit.W - 4.2, 0, 4.2, kit.H, fill=themes.C('0B0907'), transparency=42)
    head(s, 6, sub='normalization.json — цифровой паспорт модели для проверяющей системы')
    steps = [('ВХОД', 'x = (log₁₀ρ − a) / (b − a)', 'log₁₀ρ ∈ [−3, 4] · log₁₀T ∈ [−1, 7]'),
             ('ВЫХОД P', 'log₁₀P → 10^', 'P ∈ [10⁻⁶, 10⁶] ГПа'),
             ('ВЫХОД e', 'линейно, кДж/г', 'e ∈ [−0,2, 10³], знак сохраняется')]
    for i, (t_, f_, d) in enumerate(steps):
        y = 2.42 + i * 1.32
        kit.rect(s, ML, y, 7.4, 1.12, fill=PANEL, line=LINE, lw=1.0)
        kit.rect(s, ML, y, 0.05, 1.12, fill=ACC)
        kit.text(s, ML + 0.3, y + 0.16, 1.4, 0.24, t_, size=8.5, color=ACC, font=MONO,
                 tracking=1.6)
        kit.text(s, ML + 1.95, y + 0.16, 5.2, 0.3, f_, size=12.5, color=INK, font=MONO, bold=True)
        kit.text(s, ML + 1.95, y + 0.62, 5.3, 0.3, d, size=9.5, color=MUT, font=BODY)
    kit.text(s, ML, 6.5, 7.4, 0.4, 'Ни одного «магического» числа в коде инференса.', size=10.5,
             color=MUT, font=MONO)
    foot(s)
    kit.notes(s, STORY[6][3])

    # 7 — baseline
    s = kit.slide(prs, BG)
    head(s, 7, title='Билинейная интерполяция: эталон памяти',
         sub='20 интерполяторов RegularGridInterpolator по регионам, проверка на том же тесте')
    data = [['Вариант', 'Размер', 'Медиана P', 'Покрытие', 'Нарушения'],
            ['Полная таблица', '17,2 МБ', '0,000 %', '100 %', '2,86 %'],
            ['Прорежена ×2', '4,3 МБ', '0,0002 %', '99,4 %', '3,1 %'],
            ['Прорежена ×4', '1,1 МБ', '0,0016 %', '98,7 %', '4,4 %'],
            ['Прорежена ×8', '0,28 МБ', '0,0075 %', '96,7 %', '7,9 %']]
    kit.table(s, ML, 2.4, 7.9, 2.5, data, col_w=[2.2, 1.2, 1.3, 1.2, 1.3], size=10.5,
              head_size=9, ink=INK, muted=MUT, header_fill=PANEL, zebra=(PANEL, BG),
              align=['l', 'c', 'c', 'c', 'c'])
    kit.text(s, ML, 5.25, 7.9, 1.2, 'В узлах таблица точна, поэтому по MSE её не обогнать. '
             'Но 17 МБ, разрывные производные и рост ошибки при прореживании — цена.',
             size=11, color=MUT, font=BODY, ls=1.4)
    panel(s, ML + 8.25, 2.4, 3.4, 3.4, 'c_s по таблице, км/с')
    kit.pic_fit(s, FIG / 'table_cs.png', ML + 8.35, 2.5, 3.2, 3.0)
    kit.vrule(s, ML + 8.05, 2.4, 4.3, LINE, 1.0)
    foot(s)
    kit.notes(s, STORY[7][3])

    # 8 — почему не таблица, ударная волна
    s = kit.slide(prs, BG)
    hero(s, 'photo_shock.jpg', scrim=66, focus=(0.5, 0.5))
    ticks(s)
    kit.text(s, ML, 1.25, 6.0, 0.3, 'ПОЧЕМУ НЕ ХВАТИТ ТАБЛИЦЫ', size=9.5, color=ACC,
             font=MONO, tracking=2.2)
    kit.text(s, ML, 1.55, 7.0, 1.95, '9,5 %', size=104, color=ACC, font=H1, bold=True,
             tracking=-3.0, ls=0.92)
    kit.text(s, ML, 3.55, 5.6, 1.2, 'узлов полной таблицы дают нефизичные производные: '
             'c_s² ≤ 0, ∂P/∂ρ ≤ 0 или ∂e/∂T ≤ 0', size=15, color=INK, font=BODY, ls=1.35)
    kit.rect(s, ML + 6.9, 1.7, 0.04, 4.4, fill=ACC)
    kit.rect(s, ML + 7.3, 1.7, 4.3, 4.4, fill=themes.C('0B0907'), transparency=30)
    kit.text(s, ML + 7.6, 1.95, 3.8, 0.3, 'ПРИМЕР: ρ = 2,7 · T ≈ 140 К', size=9, color=ACC,
             font=MONO, tracking=1.4)
    kit.text(s, ML + 7.6, 2.35, 3.8, 1.0, 'e падает с 0,128 до 0,093 кДж/г за две ячейки.', size=12,
             color=INK, font=BODY, ls=1.4)
    kit.text(s, ML + 7.6, 3.5, 3.8, 0.8, 'c_s² < 0 — мнимое значение в гидрокоде.', size=12,
             color=ACC, font=BODY, bold=True, ls=1.35)
    kit.text(s, ML + 7.6, 4.55, 3.8, 1.2, 'Сеть сглаживает скачок и возвращает корректные '
             'производные — ценой нескольких процентов точности.', size=11, color=MUT,
             font=BODY, ls=1.4)
    kit.notes(s, STORY[8][3])

    # 9 — vanilla
    s = kit.slide(prs, BG)
    head(s, 9, sub='2 → 128 → 128 → 64 → 2, tanh, 25 282 параметра, 150 эпох, OneCycle')
    panel(s, ML, 2.4, 7.0, 4.2, 'Кривые train/test — Vanilla MLP')
    kit.pic_fit(s, FIG / 'val_curves.png', ML + 0.12, 2.5, 6.76, 3.6)
    rows = [('R²(P)', FACTS['r2_van']), ('медиана P', FACTS['med_van']),
            ('R²(e)', FACTS['r2e_van']), ('нарушений', FACTS['viol_van'])]
    for i, (k, v) in enumerate(rows):
        y = 2.45 + i * 0.72
        kit.text(s, ML + 7.45, y, 2.4, 0.3, k, size=10, color=MUT, font=BODY)
        kit.text(s, ML + 9.7, y - 0.06, 1.6, 0.34, v, size=15, color=INK, font=MONO,
                 bold=True, align='r')
        kit.hrule(s, ML + 7.45, y + 0.48, 3.9, HAIR, 1.0)
    kit.text(s, ML + 7.45, 5.55, 4.0, 1.0, 'Точность высокая. Физика разрушена: каждая третья '
             'точка нефизична.', size=12, color=ACC, font=BODY, bold=True, ls=1.4)
    kit.vrule(s, ML + 7.2, 2.4, 4.2, LINE, 1.0)
    foot(s)
    kit.notes(s, STORY[9][3])

    # 10 — схема PINN
    s = kit.slide(prs, BG)
    head(s, 10, sub='Та же сеть; в функцию потерь добавлены производные, посчитанные автоградиентом')
    boxes = [(ML, 'ВХОД', ['log₁₀ ρ', 'log₁₀ T']), (ML + 3.6, 'MLP', ['2 → 128 → 128', '→ 64 → 2, tanh']),
             (ML + 7.2, 'ВЫХОД', ['log₁₀ P', 'e, кДж/г'])]
    for i, (x, t_, lines) in enumerate(boxes):
        kit.rect(s, x, 2.45, 2.9, 1.5, fill=PANEL, line=LINE, lw=1.2)
        kit.text(s, x + 0.25, 2.62, 2.4, 0.24, t_, size=8.5, color=ACC, font=MONO, tracking=1.8)
        kit.text(s, x + 0.25, 2.95, 2.5, 0.9, lines, size=13, color=INK, font=BODY, ls=1.3)
        if i < 2:
            kit.text(s, x + 3.0, 2.95, 0.5, 0.4, '→', size=20, color=ACC, font=BODY, bold=True)
    kit.rect(s, ML, 4.35, 11.1, 1.7, fill=None, line=ACC, lw=1.4)
    kit.text(s, ML + 0.3, 4.55, 8.0, 0.24, 'ФИЗИЧЕСКИЙ ЛОСС ЧЕРЕЗ ПРОИЗВОДНЫЕ', size=8.5,
             color=ACC, font=MONO, tracking=1.8)
    kit.text(s, ML + 0.3, 4.9, 10.4, 1.0, 'autograd.grad по входам → цепное правило до СГС → '
             'ReLU-штрафы на ∂P/∂ρ, ∂e/∂T и c_s².  L = L_data + γ · L_phys,  γ = 0,03.',
             size=12.5, color=INK, font=BODY, ls=1.45)
    kit.text(s, ML, 6.35, 11.1, 0.4, 'Данные дают точность, физика — корректность производных.',
             size=11, color=MUT, font=MONO)
    foot(s)
    kit.notes(s, STORY[10][3])

    # 11 — три ограничения
    s = kit.slide(prs, BG)
    head(s, 11)
    for i, (name, formula, why, penalty) in enumerate(CONSTRAINTS):
        x = ML + i * 3.75
        kit.rect(s, x, 2.45, 3.45, 4.05, fill=PANEL, line=LINE, lw=1.0)
        kit.rect(s, x, 2.45, 3.45, 0.05, fill=ACC if i < 2 else ACC2)
        kit.text(s, x + 0.28, 2.7, 0.8, 0.3, f'0{i + 1}', size=12, color=ACC, font=MONO, bold=True)
        kit.text(s, x + 0.28, 3.02, 2.9, 0.7, name, size=14, color=INK, font=H1, bold=True, ls=1.1)
        kit.text(s, x + 0.28, 3.85, 3.0, 0.9, formula, size=10.5, color=ACC, font=MONO, ls=1.35)
        kit.text(s, x + 0.28, 4.85, 2.95, 1.0, why, size=10, color=MUT, font=BODY, ls=1.35)
        kit.text(s, x + 0.28, 5.9, 2.95, 0.5, penalty, size=8, color=MUT, font=MONO, ls=1.3)
    kit.text(s, ML, 6.65, CW, 0.3, 'ПРОВЕРКИ В СГС — КАК В ГИДРОКОДЕ', size=8.5, color=ACC,
             font=MONO, tracking=2.0)
    foot(s)
    kit.notes(s, STORY[11][3])

    # 12 — код
    s = kit.slide(prs, BG)
    head(s, 12, sub='Производные берутся в том же графе вычислений — без численного дифференцирования')
    kit.code_block(s, ML, 2.42, 6.8, 4.2, CODE_LINES, bg=themes.C('0A0F1C'), fg=INK,
                   cmt=MUT, accent=ACC, size=10, bar=ACC)
    tips = [('γ = 0,03', 'больше — физика ломает регрессию'),
            ('масштаб штрафа', 'делим на медиану |∂P/∂ρ|'),
            ('маска разрывов', 'физику считаем там, где таблица физична')]
    for i, (k, v) in enumerate(tips):
        y = 2.6 + i * 1.35
        kit.text(s, ML + 7.35, y, 3.6, 0.3, k.upper(), size=9.5, color=ACC, font=MONO, tracking=1.6)
        kit.text(s, ML + 7.35, y + 0.36, 3.6, 0.9, v, size=11.5, color=INK, font=BODY, ls=1.4)
        kit.hrule(s, ML + 7.35, y + 1.12, 3.6, LINE, 1.0)
    kit.vrule(s, ML + 7.1, 2.45, 4.1, LINE, 1.0)
    foot(s, 'фрагмент physics-лосса · PyTorch')
    kit.notes(s, STORY[12][3])

    # 13 — обучение, полоса плазмы
    s = kit.slide(prs, BG)
    kit.pic_cover(s, IMG / 'photo_plasma.jpg', 0, 0, kit.W, 1.55, focus=(0.5, 0.35))
    kit.rect(s, 0, 0, kit.W, 1.55, fill=themes.C('0B0907'), transparency=28)
    kit.text(s, ML, 0.55, 7.0, 0.25, 'ОБУЧЕНИЕ', size=9.5, color=ACC, font=MONO, tracking=2.2)
    kit.text(s, ML, 0.85, 10.5, 0.5, 'Два этапа вместо одного совместного лосса', size=24,
             color=INK, font=H1, bold=True, tracking=-0.6)
    stages = [('ЭТАП 1 · ДАННЫЕ', '150 эпох, OneCycle, MSE', 'R²(P) 0,999', 'быстро и устойчиво'),
              ('ЭТАП 2 · ФИЗИКА', 'γ = 0,03, маска разрывов, lr/10', 'нарушения 36 % → 0,4 %',
               'медленнее, но чинит производные')]
    for i, (tag, desc, res, note_) in enumerate(stages):
        x = ML + i * 5.9
        kit.rect(s, x, 2.15, 5.4, 2.65, fill=PANEL, line=LINE, lw=1.0)
        kit.text(s, x + 0.3, 2.4, 4.8, 0.24, tag, size=8.5, color=ACC, font=MONO, tracking=1.8)
        kit.text(s, x + 0.3, 2.75, 4.8, 0.5, desc, size=13, color=INK, font=BODY, ls=1.35)
        kit.text(s, x + 0.3, 3.5, 4.8, 0.5, res, size=22, color=ACC, font=H1, bold=True,
                 tracking=-0.6)
        kit.text(s, x + 0.3, 4.15, 4.8, 0.4, note_, size=10, color=MUT, font=BODY)
    kit.text(s, ML + 5.55, 2.6, 0.5, 0.4, '→', size=22, color=ACC, font=BODY, bold=True)
    kit.text(s, ML, 5.15, 11.2, 1.5, 'Совместное обучение сразу по двум лоссам разваливало точность: '
             'градиенты физики забивали сигнал данных. Разделение этапов — главный инженерный приём работы. '
             'Повторная физическая стадия улучшения не давала.', size=11.5, color=INK, font=BODY, ls=1.45)
    kit.notes(s, STORY[13][3])

    # 14 — результаты
    s = kit.slide(prs, BG)
    head(s, 14, sub='226 011 точек теста, все метрики посчитаны одним скриптом')
    data = [['Подход', 'R²(P)', 'Медиана P', 'p95 P', 'R²(e)', 'Нарушения', 'Размер', 'мкс'],
            ['Baseline (таблица)', '1,00000', '0,000 %', '0,000 %', '1,00000', FACTS['viol_base'], FACTS['table_mb'] + ' МБ', '0,54'],
            ['Vanilla MLP', FACTS['r2_van'], FACTS['med_van'], FACTS['p95_van'], FACTS['r2e_van'], FACTS['viol_van'], '0,10 МБ', FACTS['us_van']],
            ['PINN', FACTS['r2_pinn'], FACTS['med_pinn'], FACTS['p95_pinn'], FACTS['r2e_pinn'], FACTS['viol_pinn'], '0,10 МБ', FACTS['us']]]
    kit.table(s, ML, 2.4, CW, 2.4, data, col_w=[2.6, 1.2, 1.3, 1.1, 1.2, 1.4, 1.2, 0.9],
              size=11, head_size=9, ink=INK, muted=MUT, header_fill=PANEL, zebra=(PANEL, BG),
              align=['l', 'c', 'c', 'c', 'c', 'c', 'c', 'c'])
    kit.text(s, ML, 5.05, 7.4, 1.2, f'Точность практически равна ({FACTS["med_van"]} против {FACTS["med_pinn"]}), но нарушений '
             f'в {FACTS["ratio"]} раза больше.', size=11.5, color=INK,
             font=BODY, ls=1.4)
    kit.text(s, ML + 7.8, 5.0, 3.7, 1.3,
             ['Одна и та же выборка для всех трёх подходов.',
              'Размер — файл весов; мкс — batch 1 на CPU.'],
             size=9.5, color=MUT, font=BODY, ls=1.35, space_after=8)
    foot(s)
    kit.notes(s, STORY[14][3])

    # 15 — карты ошибок
    s = kit.slide(prs, BG)
    head(s, 15, sub='Относительная ошибка P на сетке 240 × 320 точек по всей диаграмме')
    panel(s, ML, 2.42, 8.5, 3.95, 'Слева Vanilla, справа PINN · |ΔP| / P, %')
    kit.pic_fit(s, FIG / 'error_maps.png', ML + 0.12, 2.5, 8.26, 3.4)
    kit.text(s, ML + 8.85, 2.45, 2.6, 0.25, 'НАБЛЮДЕНИЯ', size=8.5, color=ACC, font=MONO,
             tracking=1.8)
    for i, (k, v) in enumerate([(f'разрывы', FACTS['err_jump']), ('гладкие зоны', FACTS['err_smooth']),
                                ('медиана', FACTS['med_pinn']), ('доля разрывов', FACTS['jump_frac'])]):
        y = 2.8 + i * 0.72
        kit.text(s, ML + 8.85, y, 1.8, 0.3, k, size=10, color=MUT, font=BODY)
        kit.text(s, ML + 10.75, y - 0.04, 0.7, 0.3, v, size=12, color=INK, font=MONO,
                 bold=True, align='r')
        kit.hrule(s, ML + 8.85, y + 0.46, 2.55, LINE, 1.0)
    kit.text(s, ML + 8.85, 5.85, 2.6, 0.9, 'Ошибка выше в 1,7 раза именно на стыках регионов.',
             size=10, color=INK, font=BODY, ls=1.35)
    foot(s)
    kit.notes(s, STORY[15][3])

    # 16 — нарушения
    s = kit.slide(prs, BG)
    head(s, 16, sub='Флаги нарушений в каждой точке диаграммы — это и есть check_physics')
    panel(s, ML, 2.42, 6.4, 4.0, 'Карта нарушений: Vanilla / PINN')
    kit.pic_fit(s, FIG / 'violation_maps.png', ML + 0.12, 2.52, 6.16, 3.44)
    panel(s, ML + 6.65, 2.42, 4.95, 2.35, 'Нарушения по типам, % точек теста')
    kit.pic_fit(s, FIG / 'violations_bar.png', ML + 6.77, 2.52, 4.7, 1.9)
    kit.text(s, ML + 6.65, 4.95, 4.95, 1.4, 'Vanilla: 40 % площади. PINN: 0,7 % — тонкая полоса на '
             'стыке регионов, где разрывна сама таблица. Точек с c_s ≥ c нет ни у одной модели.',
             size=10, color=INK, font=BODY, ls=1.35)
    foot(s)
    kit.notes(s, STORY[16][3])

    # 17 — скорость звука
    s = kit.slide(prs, BG)
    head(s, 17, sub='Самая чувствительная к производным величина: сверка с табличными конечными разностями')
    panel(s, ML, 2.42, 7.6, 4.0, 'c_s PINN против табличной c_s, полная диаграмма')
    kit.pic_fit(s, FIG / 'cs_scatter.png', ML + 0.12, 2.52, 7.36, 3.44)
    for i, (k, v) in enumerate([('R² (лог-шкала)', FACTS['cs_r2']), ('медианное отклонение', FACTS['cs_med']),
                                ('p95 отклонения', FACTS['cs_p95']), ('c_s ≥ c', '0 % точек')]):
        y = 2.5 + i * 0.78
        kit.text(s, ML + 7.95, y, 2.35, 0.3, k, size=10, color=MUT, font=BODY)
        kit.text(s, ML + 10.4, y - 0.06, 1.1, 0.32, v, size=14, color=ACC, font=MONO,
                 bold=True, align='r')
        kit.hrule(s, ML + 7.95, y + 0.5, 3.55, LINE, 1.0)
    kit.text(s, ML + 7.95, 5.95, 3.5, 0.6, 'Расхождения — там, где табличная c_s не определена.',
             size=10, color=MUT, font=BODY, ls=1.35)
    foot(s)
    kit.notes(s, STORY[17][3])

    # 18 — обёртка
    s = kit.slide(prs, BG)
    head(s, 18, sub='Класс-обёртка на 90 строк: docstrings Google-style, проверка области определения')
    kit.code_block(s, ML, 2.42, 6.9, 4.15, WRAPPER_CODE, bg=themes.C('0A0F1C'), fg=INK,
                   cmt=MUT, accent=ACC, size=10, bar=ACC)
    for i, (k, v) in enumerate([('predict', 'векторный инференс P и e'),
                                ('sound_speed', 'autograd внутри, СГС на выходе'),
                                ('check_physics', 'маски нарушений и флаг ok'),
                                ('in_domain', 'границы области определения')]):
        y = 2.6 + i * 0.85
        kit.text(s, ML + 7.4, y, 1.9, 0.3, k, size=11.5, color=ACC, font=MONO, bold=True)
        kit.text(s, ML + 9.4, y, 2.2, 0.6, v, size=10, color=MUT, font=BODY, ls=1.3)
        kit.hrule(s, ML + 7.4, y + 0.62, 4.0, LINE, 1.0)
    kit.text(s, ML + 7.4, 6.1, 4.0, 0.3, '10⁵ запросов — 0,13 с', size=10, color=INK, font=MONO)
    kit.vrule(s, ML + 7.15, 2.45, 4.05, LINE, 1.0)
    foot(s)
    kit.notes(s, STORY[18][3])

    # 19 — сжатие
    s = kit.slide(prs, BG)
    head(s, 19, sub='Дополнительный этап кейса: измеримый эффект оптимизации модели')
    panel(s, ML, 2.42, 6.6, 4.05, 'Размер и время одиночного запроса')
    kit.pic_fit(s, FIG / 'size_speed.png', ML + 0.12, 2.52, 6.36, 3.48)
    data = [['Вариант', 'Размер', 'мкс'], ['fp32', '0,099 МБ', FACTS['fp32_us']],
            ['TorchScript', '0,107 МБ', FACTS['ts_us']], ['int8 (dynamic)', '0,031 МБ', FACTS['int8_us']]]
    kit.table(s, ML + 7.0, 2.5, 4.2, 1.95, data, col_w=[1.9, 1.2, 0.9], size=10.5, head_size=9,
              ink=INK, muted=MUT, header_fill=PANEL, zebra=(PANEL, BG), align=['l', 'c', 'c'])
    kit.text(s, ML + 7.0, 4.75, 4.3, 1.7, ['TorchScript — ×1,6 к скорости batch-1 без потери точности.',
                                           'int8 — веса в 3,2 раза меньше, p99 отклонения 0,031.',
                                           'В гидрокод выбираем TorchScript.'],
             size=10, color=MUT, font=BODY, ls=1.4, space_after=8)
    kit.vrule(s, ML + 6.8, 2.45, 4.0, LINE, 1.0)
    foot(s)
    kit.notes(s, STORY[19][3])

    # 20 — финал на фото лаборатории
    s = kit.slide(prs, BG)
    hero(s, 'photo_lab.jpg', scrim=72, focus=(0.5, 0.4))
    ticks(s)
    kit.text(s, ML, 1.15, 8.0, 0.3, 'ИТОГИ', size=9.5, color=ACC, font=MONO, tracking=2.4)
    kit.text(s, ML, 1.52, 10.4, 0.62, 'Физика под контролем, габарит в норме', size=30,
             color=INK, font=H1, bold=True, tracking=-0.8)
    kit.rect(s, ML - 0.25, 2.55, 11.7, 3.55, fill=themes.C('0E0C0A'), transparency=74)
    cols = [('СДЕЛАНО', DONE), ('ОГРАНИЧЕНИЯ', LIMITS), ('ДАЛЬШЕ', NEXT)]
    for i, (t_, items) in enumerate(cols):
        x = ML + i * 3.85
        kit.text(s, x, 2.75, 3.5, 0.25, t_, size=8.5, color=ACC, font=MONO, tracking=2.0)
        kit.hrule(s, x, 3.05, 3.55, ACC if i == 0 else HAIR, 1.2)
        kit.bullets(s, x, 3.2, 3.55, 2.9, items, size=9.5, color=INK, font=BODY, gap=8,
                    bullet='·', bullet_color=ACC, ls=1.35, bold_lead=False)
    kit.rect(s, ML - 0.25, 6.2, 11.7, 0.62, fill=themes.C('0E0C0A'), transparency=80)
    kit.text(s, ML, 6.34, 11.2, 0.5, ARTIFACTS, size=9, color=MUT, font=MONO, ls=1.35)
    kit.notes(s, STORY[20][3])

    prs.save(out)
    return out


if __name__ == '__main__':
    print(build('presentation/02_Industrial_фото.pptx'))
