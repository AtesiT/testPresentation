"""Вариант 3 — Editorial / научный журнал: бумага, антиква, тонкие линейки."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kit
import themes
from content import (ARTIFACTS, CHECKLIST, CODE_LINES, CONSTRAINTS, DONE, FACTS,
                     LIMITS, NEXT, STORY, WRAPPER_CODE)

T = themes.EDITORIAL
BG, PANEL, INK, MUT = T['bg'], T['panel'], T['ink'], T['muted']
ACC, ACC2, HAIR = T['accent'], T['accent2'], T['hair']
H1, BODY, MONO = T['head'], T['body'], T['mono']
ML, MR = 1.0, 1.0
CW = kit.W - ML - MR
FIG = kit.LIGHT / 'editorial'
IMG = kit.ASSETS
RUBRIC = 'ИТ КоР · трек ML · кейс 01'


def head(s, num, kicker=None, title=None, sub=None, fig_no=None):
    kicker = kicker or STORY[num][0]
    title = title or STORY[num][1]
    sub = STORY[num][2] if sub is None else sub
    kit.text(s, ML, 0.46, 6.0, 0.22, RUBRIC, size=8.5, color=MUT, font=BODY, caps=True,
             tracking=1.6)
    kit.text(s, kit.W - MR - 4.0, 0.46, 4.0, 0.22, kicker, size=8.5, color=ACC, font=BODY,
             caps=True, tracking=1.6, align='r')
    kit.hrule(s, ML, 0.72, CW, INK, 1.0)
    kit.hrule(s, ML, 0.78, CW, HAIR, 0.5)
    kit.text(s, ML, 0.95, CW - 0.6, 0.9, title, size=28, color=INK, font=H1, ls=1.08)
    if sub:
        kit.text(s, ML, 1.72, CW - 1.4, 0.45, sub, size=11.5, color=MUT, font=H1, italic=True,
                 ls=1.35)


def folio(s, num):
    kit.hrule(s, ML, 6.98, CW, HAIR, 0.5)
    kit.text(s, ML, 7.06, 6.0, 0.2, 'Физически согласованный суррогат УРС алюминия', size=8,
             color=MUT, font=BODY, caps=True, tracking=1.2)
    kit.text(s, kit.W - MR - 1.2, 7.02, 1.2, 0.26, f'{num}', size=12, color=INK, font=H1,
             align='r')


def figure(s, path, x, y, w, h, no, cap):
    kit.rect(s, x, y, w, h, fill=PANEL, line=HAIR, lw=0.75)
    kit.pic_fit(s, path, x + 0.1, y + 0.1, w - 0.2, h - 0.2)
    kit.text(s, x, y + h + 0.08, w, 0.3, f'Рис. {no}. {cap}', size=8.5, color=MUT,
             font=BODY, italic=True, ls=1.25)


def body(s, x, y, w, h, txt, size=11.5, ls=1.55):
    kit.text(s, x, y, w, h, txt, size=size, color=INK, font=BODY, ls=ls)


def drop(s, x, y, ch):
    kit.text(s, x, y, 0.7, 0.7, ch, size=46, color=ACC, font=H1, bold=False, ls=0.9)


def build(out):
    prs = kit.deck()

    # 1 — титул
    s = kit.slide(prs, BG)
    kit.hrule(s, ML, 0.72, CW, INK, 1.2)
    kit.text(s, ML, 0.86, 7.4, 0.24, 'Финальное задание · Росатом · трек Machine Learning',
             size=9, color=MUT, font=BODY, caps=True, tracking=1.8)
    kit.text(s, ML, 1.22, 7.7, 2.55,
             ['Физически согласованный', 'суррогат уравнения', 'состояния алюминия'],
             size=36, color=INK, font=H1, ls=1.12)
    kit.text(s, ML, 3.75, 7.2, 0.9,
             'PINN для P(ρ,T), e(ρ,T) и скорости звука: 12 порядков давления, '
             '226 011 точек теста, 0,10 МБ весов.',
             size=13, color=MUT, font=H1, italic=True, ls=1.45)
    kit.hrule(s, ML, 4.9, 4.0, ACC, 1.0)
    kit.text(s, ML, 5.05, 4.2, 0.2, 'КЛЮЧЕВЫЕ ВЕЛИЧИНЫ', size=8.5, color=ACC, font=BODY,
             caps=True, tracking=1.8)
    for i, (v, l) in enumerate([('0,43 %', 'точек с нарушением физики'),
                                (f"×{FACTS['ratio']}", 'реже, чем без физики в лоссе'),
                                ('0,95 мкс', 'на запрос, batch 1')]):
        y = 5.35 + i * 0.52
        kit.text(s, ML, y, 1.5, 0.3, v, size=15, color=INK, font=H1)
        kit.text(s, ML + 1.7, y + 0.06, 3.4, 0.3, l, size=9.5, color=MUT, font=BODY)
    kit.rect(s, ML + 8.6, 1.35, 3.75, 4.15, fill=PANEL, line=HAIR, lw=0.75)
    kit.pic_cover(s, IMG / 'photo_micro.jpg', ML + 8.72, 1.47, 3.51, 3.35, focus=(0.5, 0.45))
    kit.text(s, ML + 8.72, 4.9, 3.5, 0.5, 'Микроструктура алюминиевого сплава — '
             'иллюстрация, не данные.', size=8, color=MUT, font=BODY, italic=True, ls=1.25)
    kit.hrule(s, ML, 6.98, CW, HAIR, 0.5)
    kit.text(s, ML, 7.06, 7.0, 0.2, 'Автор: <имя> · команда: <состав> · 2026', size=8.5,
             color=MUT, font=BODY, caps=True, tracking=1.4)
    kit.notes(s, STORY[1][3])

    # 2 — постановка
    s = kit.slide(prs, BG)
    head(s, 2)
    drop(s, ML, 2.35, 'Г')
    body(s, ML + 0.72, 2.4, 5.4, 2.0,
         'идрокоду нужен не «чёрный ящик», а согласованный с термодинамикой суррогат: '
         'запрашиваются не только P и e, но и производные — от них зависит устойчивость схемы.')
    body(s, ML, 4.55, 5.9, 2.2,
         'Кейс требует воспроизвести таблицу на всей фазовой диаграмме, сохранить три '
         'инварианта и уложиться в 10 МБ. Поэтому оцениваем не только MSE, но и долю '
         'точек, где физика нарушена.')
    kit.vrule(s, ML + 6.35, 2.35, 4.3, HAIR, 0.75)
    items = [('Точность', 'P и e по всей диаграмме, а не только в узлах сетки.'),
             ('Физика', '∂P/∂ρ > 0, ∂e/∂T > 0, 0 < c_s < c.'),
             ('Габарит', 'до 10 МБ, микросекунды на запрос, без GPU.')]
    for i, (t_, d) in enumerate(items):
        y = 2.4 + i * 1.45
        kit.text(s, ML + 6.9, y, 0.5, 0.3, f'{(i + 1) * 1:02d}', size=10, color=ACC,
                 font=MONO)
        kit.text(s, ML + 7.5, y - 0.06, 3.6, 0.3, t_, size=14, color=INK, font=H1, bold=False)
        kit.text(s, ML + 7.5, y + 0.38, 3.9, 0.8, d, size=10.5, color=MUT, font=BODY, ls=1.45)
        kit.hrule(s, ML + 6.9, y + 1.18, 4.4, HAIR, 0.5)
    folio(s, 2)
    kit.notes(s, STORY[2][3])

    # 3 — чек-лист
    s = kit.slide(prs, BG)
    head(s, 3, sub='Девять критериев финального задания — и чем закрыт каждый')
    kit.text(s, ML, 2.3, 5.2, 0.24, 'КРИТЕРИЙ', size=8, color=MUT, font=BODY, caps=True,
             tracking=1.6)
    kit.text(s, ML + 5.3, 2.3, 0.8, 0.24, 'БАЛЛ', size=8, color=MUT, font=BODY, caps=True,
             tracking=1.6, align='r')
    kit.text(s, ML + 6.0, 2.3, 5.0, 0.24, 'ЧЕМ ЗАКРЫТ', size=8, color=MUT, font=BODY,
             caps=True, tracking=1.6)
    kit.hrule(s, ML, 2.56, CW, INK, 0.75)
    for i, (name, pts, what) in enumerate(CHECKLIST):
        y = 2.66 + i * 0.47
        kit.text(s, ML, y, 5.1, 0.26, name, size=11, color=INK, font=BODY)
        kit.text(s, ML + 5.3, y, 0.8, 0.26, pts, size=11, color=ACC, font=BODY, align='r')
        kit.text(s, ML + 6.0, y, 5.3, 0.26, what, size=9, color=MUT, font=BODY)
        kit.hrule(s, ML, y + 0.38, CW, HAIR, 0.5)
    kit.text(s, ML, 6.95 - 0.28, 3.0, 0.24, 'Итого', size=10, color=MUT, font=BODY,
             caps=True, tracking=1.4)
    kit.text(s, ML + 5.3, 6.95 - 0.28, 0.8, 0.26, '100', size=11, color=INK, font=BODY,
             bold=True, align='r')
    folio(s, 3)
    kit.notes(s, STORY[3][3])

    # 4 — данные
    s = kit.slide(prs, BG)
    head(s, 4, title='Датасет: 20 региональных сеток',
         sub='1 130 053 строки, четыре диапазона плотности × пять диапазонов температуры')
    body(s, ML, 2.35, 5.6, 1.5,
         'Регионы независимы: внутри каждого сетка регулярная 300 × 300, но на стыках '
         'значения P и e не согласованы. Именно эта особенность определяет сложность задачи.')
    body(s, ML, 4.05, 5.6, 1.5,
         '9,5 % узлов полной сетки формально нефизичны ещё до появления модели — следствие '
         'разрывов, а не ошибки организаторов.')
    rows = [('Точек в датасете', '1 130 053'), ('Региональных сеток', '20'),
            ('Узлов в сетке', '300 × 300'), ('Тестовая выборка', '226 011 точек'),
            ('Выхода модели', 'P, e и производные')]
    kit.vrule(s, ML + 6.1, 2.35, 4.1, HAIR, 0.75)
    for i, (k, v) in enumerate(rows):
        y = 2.4 + i * 0.78
        kit.text(s, ML + 6.6, y, 3.9, 0.26, k, size=10, color=MUT, font=BODY)
        kit.text(s, ML + 6.6, y + 0.26, 3.9, 0.3, v, size=13.5, color=INK, font=H1)
        kit.hrule(s, ML + 6.6, y + 0.66, 4.6, HAIR, 0.5)
    folio(s, 4)
    kit.notes(s, STORY[4][3])

    # 5 — EDA
    s = kit.slide(prs, BG)
    head(s, 5, title='Поля давления и энергии', sub='')
    figure(s, FIG / 'eda_maps.png', ML, 2.3, 8.4, 3.85, 1,
           'log₁₀ P и e на полной сетке. Давление охватывает 12 порядков, энергия меняет знак')
    kit.text(s, ML + 8.75, 2.35, 2.5, 3.9,
             ['Давление логарифмируем и на входе, и на выходе.',
              'Энергию предсказываем линейно: она проходит через ноль.',
              'Скачки на картах — стыки регионов.'],
             size=10, color=INK, font=BODY, ls=1.5, space_after=8)
    folio(s, 5)
    kit.notes(s, STORY[5][3])

    # 6 — нормализация
    s = kit.slide(prs, BG)
    head(s, 6, sub='normalization.json фиксирует все преобразования: инференс воспроизводим без нашего кода')
    steps = [('Вход', 'x = (log₁₀ρ − a) / (b − a)', 'log₁₀ρ ∈ [−3, 4]; log₁₀T ∈ [−1, 7]'),
             ('Выход P', 'log₁₀P, затем 10^', 'P ∈ [10⁻⁶, 10⁶] ГПа'),
             ('Выход e', 'линейно, кДж/г', 'e ∈ [−0,2, 10³], знак сохраняется')]
    for i, (t_, f_, d) in enumerate(steps):
        y = 2.4 + i * 1.35
        kit.text(s, ML, y, 1.6, 0.24, t_.upper(), size=8.5, color=ACC, font=BODY, caps=True,
                 tracking=1.6)
        kit.text(s, ML + 1.9, y - 0.04, 5.0, 0.3, f_, size=13, color=INK, font=MONO)
        kit.text(s, ML + 1.9, y + 0.36, 8.6, 0.3, d, size=10, color=MUT, font=BODY)
        kit.hrule(s, ML, y + 0.95, CW, HAIR, 0.5)
    body(s, ML, 6.35, 10.6, 0.5,
         'Проверяющая система читает только этот файл: константы, единицы и границы области '
         'определения описаны явно.', size=10.5, ls=1.4)
    folio(s, 6)
    kit.notes(s, STORY[6][3])

    # 7 — baseline
    s = kit.slide(prs, BG)
    head(s, 7, sub='20 интерполяторов RegularGridInterpolator, проверка на той же тестовой выборке')
    data = [['Вариант таблицы', 'Размер', 'Медиана P', 'Покрытие', 'Нарушения'],
            ['Полная', '17,2 МБ', '0,000 %', '100 %', '2,86 %'],
            ['Прорежена ×2', '4,3 МБ', '0,0002 %', '99,4 %', '3,1 %'],
            ['Прорежена ×4', '1,1 МБ', '0,0016 %', '98,7 %', '4,4 %'],
            ['Прорежена ×8', '0,28 МБ', '0,0075 %', '96,7 %', '7,9 %']]
    kit.table(s, ML, 2.35, 7.6, 2.3, data, col_w=[2.1, 1.1, 1.2, 1.1, 1.2], size=10,
              head_size=8.5, ink=INK, muted=MUT, header_fill=None, zebra=None,
              align=['l', 'c', 'c', 'c', 'c'], font=BODY, head_font=BODY)
    for r in range(5):
        kit.hrule(s, ML, 2.35 + 0.5 * r, 7.6, HAIR if r else INK, 0.5 if r else 0.75)
    body(s, ML, 5.1, 7.4, 1.3,
         'В узлах сетки интерполяция точна, поэтому по MSE её не обогнать. Цена — 17 МБ, '
         'разрывные производные и быстрый рост ошибки при прореживании.')
    kit.vrule(s, ML + 7.85, 2.35, 3.95, HAIR, 0.75)
    kit.text(s, ML + 8.3, 2.35, 3.9, 2.5,
             ['Baseline — обязательный пункт чек-листа на 5 баллов.',
              'Две роли: эталон точности и ориентир по памяти.',
              'Табличный звук: 2,86 % точек уже нефизичны.'],
             size=10, color=MUT, font=BODY, ls=1.5, space_after=10)
    folio(s, 7)
    kit.notes(s, STORY[7][3])

    # 8 — почему не таблица, пластина
    s = kit.slide(prs, BG)
    head(s, 8, title='Почему таблицы недостаточно', sub='')
    kit.rect(s, ML, 2.3, 4.6, 3.55, fill=PANEL, line=HAIR, lw=0.75)
    kit.pic_cover(s, IMG / 'photo_shock.jpg', ML + 0.1, 2.4, 4.4, 3.35, focus=(0.5, 0.5))
    kit.text(s, ML, 5.95, 4.6, 0.55, 'Ударная волна и интерференционные полосы. '
             'Иллюстрация, не данные.', size=8, color=MUT, font=BODY, italic=True, ls=1.3)
    kit.text(s, ML + 5.3, 2.3, 6.0, 0.9, '9,5 %', size=54, color=ACC, font=H1, ls=1.0)
    body(s, ML + 5.3, 3.15, 5.9, 1.0,
         'узлов полной таблицы дают нефизичные производные: c_s² ≤ 0, ∂P/∂ρ ≤ 0 или ∂e/∂T ≤ 0.',
         size=12)
    body(s, ML + 5.3, 4.3, 5.9, 1.6,
         'Пример: при ρ = 2,7 г/см³ и T ≈ 140 К энергия падает с 0,128 до 0,093 кДж/г за две '
         'ячейки. Конечная разность даёт c_s² < 0 — мнимое значение в гидрокоде. Гладкая сеть '
         'сглаживает скачок и возвращает корректные производные.')
    folio(s, 8)
    kit.notes(s, STORY[8][3])

    # 9 — vanilla
    s = kit.slide(prs, BG)
    head(s, 9, title='Vanilla MLP: точность без физики',
         sub='2 → 128 → 128 → 64 → 2, tanh, 25 282 параметра, 150 эпох')
    figure(s, FIG / 'val_curves.png', ML, 2.3, 6.4, 3.95, 2,
           'Кривые обучения: train и test (20 % выборки)')
    kit.vrule(s, ML + 6.7, 2.3, 4.0, HAIR, 0.75)
    for i, (k, v) in enumerate([('R²(P)', FACTS['r2_van']), ('Медиана P', FACTS['med_van']),
                                ('R²(e)', FACTS['r2e_van']), ('Нарушений', FACTS['viol_van'])]):
        y = 2.35 + i * 0.72
        kit.text(s, ML + 7.1, y, 2.6, 0.26, k, size=10, color=MUT, font=BODY)
        kit.text(s, ML + 7.1, y + 0.24, 2.6, 0.32, v, size=15, color=INK, font=H1)
        kit.hrule(s, ML + 7.1, y + 0.62, 3.2, HAIR, 0.5)
    body(s, ML + 7.1, 5.45, 3.2, 0.9, 'Точность хорошая. Физика разрушена.',
         size=10.5, ls=1.4)
    folio(s, 9)
    kit.notes(s, STORY[9][3])

    # 10 — PINN схема
    s = kit.slide(prs, BG)
    head(s, 10, sub='Та же сеть; в функцию потерь добавлены производные, посчитанные автоградиентом')
    boxes = [(ML, 'Вход', ['log₁₀ ρ', 'log₁₀ T']), (ML + 3.75, 'MLP', ['2 → 128 → 128', '→ 64 → 2']),
             (ML + 7.5, 'Выход', ['log₁₀ P', 'e'])]
    for i, (x, t_, lines) in enumerate(boxes):
        kit.rect(s, x, 2.35, 3.1, 1.35, fill=PANEL, line=INK, lw=0.75)
        kit.text(s, x + 0.25, 2.5, 2.6, 0.22, t_.upper(), size=8, color=MUT, font=BODY,
                 caps=True, tracking=1.6)
        kit.text(s, x + 0.25, 2.8, 2.7, 0.8, lines, size=12, color=INK, font=BODY, ls=1.35)
        if i < 2:
            kit.text(s, x + 3.2, 2.8, 0.5, 0.4, '→', size=16, color=MUT, font=BODY)
    kit.rect(s, ML, 4.1, 11.3, 1.45, fill=None, line=ACC, lw=0.75)
    kit.text(s, ML + 0.3, 4.28, 8.0, 0.22, 'ФИЗИЧЕСКИЙ ЛОСС', size=8, color=ACC, font=BODY,
             caps=True, tracking=1.8)
    body(s, ML + 0.3, 4.55, 10.6, 0.9,
         'autograd.grad по входам → цепное правило до СГС → ReLU-штрафы на ∂P/∂ρ, ∂e/∂T и c_s². '
         'L = L_data + γ · L_phys, γ = 0,03.')
    body(s, ML, 5.85, 11.3, 0.9,
         'Данные отвечают за точность, физика — за корректность производных. Вес γ управляет '
         'балансом и подбирался по доле нарушений, а не по MSE.', size=10.5)
    folio(s, 10)
    kit.notes(s, STORY[10][3])

    # 11 — ограничения
    s = kit.slide(prs, BG)
    head(s, 11)
    for i, (name, formula, why, penalty) in enumerate(CONSTRAINTS):
        y = 2.35 + i * 1.5
        kit.text(s, ML, y - 0.02, 0.6, 0.3, f'{(i + 1) * 1:02d}', size=10, color=ACC,
                 font=MONO)
        kit.text(s, ML + 0.6, y - 0.08, 4.2, 0.32, name, size=14, color=INK, font=H1)
        kit.text(s, ML + 5.2, y - 0.04, 6.0, 0.36, formula, size=12, color=INK, font=MONO)
        kit.text(s, ML + 0.6, y + 0.36, 10.5, 0.4, why, size=10.5, color=MUT, font=BODY, ls=1.4)
        kit.text(s, ML + 0.6, y + 0.86, 10.5, 0.26, penalty, size=8.5, color=MUT, font=MONO)
        kit.hrule(s, ML, y + 1.28, CW, HAIR, 0.5)
    folio(s, 11)
    kit.notes(s, STORY[11][3])

    # 12 — код
    s = kit.slide(prs, BG)
    head(s, 12)
    body(s, ML, 2.35, 4.6, 1.8,
         'Производные считаются в том же графе вычислений: штраф не требует ни численного '
         'дифференцирования, ни второй сети.')
    for i, (k, v) in enumerate([('γ = 0,03', 'иначе физика ломает регрессию'),
                                ('масштаб', 'штраф делим на медиану |∂P/∂ρ|'),
                                ('маска', 'физика только там, где таблица физична')]):
        y = 4.35 + i * 0.72
        kit.text(s, ML, y, 1.5, 0.26, k, size=9.5, color=ACC, font=BODY, caps=True,
                 tracking=1.4)
        kit.text(s, ML + 1.55, y - 0.02, 3.3, 0.6, v, size=10, color=MUT, font=BODY, ls=1.35)
    kit.code_block(s, ML + 5.0, 2.35, 6.3, 4.2, CODE_LINES, bg=PANEL, fg=INK, cmt=MUT,
                   accent=ACC, size=9.5, bar=ACC)
    folio(s, 12)
    kit.notes(s, STORY[12][3])

    # 13 — обучение
    s = kit.slide(prs, BG)
    head(s, 13)
    stages = [('Этап первый', 'Данные', '150 эпох, OneCycle, MSE в нормированных единицах',
               'R²(P) ≈ 0,999', 'быстро и устойчиво'),
              ('Этап второй', 'Физика', 'та же сеть, γ = 0,03, маска разрывов, lr в 10 раз меньше',
               'нарушения 36 % → 0,4 %', 'медленно, но чинит производные')]
    for i, (tag, name, desc, res, note_) in enumerate(stages):
        x = ML + i * 5.9
        kit.text(s, x, 2.35, 3.6, 0.22, tag.upper(), size=8.5, color=ACC, font=BODY,
                 caps=True, tracking=1.6)
        kit.text(s, x, 2.62, 4.6, 0.5, name, size=24, color=INK, font=H1)
        kit.hrule(s, x, 3.22, 4.9, INK, 0.75)
        kit.text(s, x, 3.35, 4.7, 0.9, desc, size=10.5, color=MUT, font=BODY, ls=1.45)
        kit.text(s, x, 4.35, 4.7, 0.35, res, size=14, color=INK, font=H1)
        kit.text(s, x, 4.78, 4.7, 0.3, note_, size=9, color=MUT, font=BODY, italic=True)
    kit.text(s, ML + 5.35, 2.7, 0.5, 0.4, '→', size=17, color=ACC, font=BODY)
    body(s, ML, 5.6, 11.0, 1.1,
         'Совместное обучение по двум лоссам сразу разваливало точность: градиенты физики '
         'забивали сигнал данных. Разделение этапов — главный инженерный приём работы; '
         'повторная физическая стадия улучшения не давала.')
    folio(s, 13)
    kit.notes(s, STORY[13][3])

    # 14 — результаты
    s = kit.slide(prs, BG)
    head(s, 14, sub='Одна и та же тестовая выборка — 226 011 точек по всей фазовой диаграмме')
    data = [['Подход', 'R²(P)', 'Медиана P', 'p95 P', 'R²(e)', 'Нарушения', 'Размер', 'мкс'],
            ['Baseline', '1,00000', '0,000 %', '0,000 %', '1,00000', FACTS['viol_base'], FACTS['table_mb'] + ' МБ', '0,54'],
            ['Vanilla MLP', FACTS['r2_van'], FACTS['med_van'], FACTS['p95_van'], FACTS['r2e_van'], FACTS['viol_van'], '0,10 МБ', FACTS['us_van']],
            ['PINN', FACTS['r2_pinn'], FACTS['med_pinn'], FACTS['p95_pinn'], FACTS['r2e_pinn'], FACTS['viol_pinn'], '0,10 МБ', FACTS['us']]]
    kit.table(s, ML, 2.35, CW, 2.2, data, col_w=[2.4, 1.2, 1.3, 1.1, 1.2, 1.4, 1.2, 0.9],
              size=10, head_size=8.5, ink=INK, muted=MUT, header_fill=None, zebra=None,
              align=['l', 'c', 'c', 'c', 'c', 'c', 'c', 'c'], font=BODY, head_font=BODY)
    for r in range(5):
        kit.hrule(s, ML, 2.35 + 0.5 * r, CW, HAIR if r else INK, 0.5 if r else 0.75)
    body(s, ML, 5.1, 6.6, 1.2,
         f'Точность практически равна ({FACTS["med_van"]} против {FACTS["med_pinn"]} по медиане), но нарушений '
         f'в {FACTS["ratio"]} раза больше.')
    kit.text(s, ML + 7.2, 5.05, 4.2, 1.2,
             ['Размер — файл весов, мкс — batch 1 на CPU.',
              'Все числа получены одним скриптом и лежат в сравнении.'],
             size=9, color=MUT, font=BODY, ls=1.45, space_after=6)
    folio(s, 14)
    kit.notes(s, STORY[14][3])

    # 15 — карты ошибок
    s = kit.slide(prs, BG)
    head(s, 15, sub='Относительная ошибка P на сетке 240 × 320 точек по всей диаграмме')
    figure(s, FIG / 'error_maps.png', ML, 2.3, 8.1, 3.8, 3,
           'Слева Vanilla, справа PINN. Шкала общая, обрезка на 99-м проценте')
    kit.vrule(s, ML + 8.45, 2.3, 4.0, HAIR, 0.75)
    for i, (k, v) in enumerate([(f"Разрывы ({FACTS['jump_frac']})", FACTS['err_jump']), ('Гладкие зоны', FACTS['err_smooth']),
                                ('Медиана', FACTS['med_pinn'])]):
        y = 2.35 + i * 0.7
        kit.text(s, ML + 8.85, y, 2.4, 0.26, k, size=9.5, color=MUT, font=BODY)
        kit.text(s, ML + 11.3, y - 0.04, 0.6, 0.3, v, size=12, color=INK, font=H1, align='r')
        kit.hrule(s, ML + 8.85, y + 0.5, 3.05, HAIR, 0.5)
    body(s, ML + 8.85, 4.6, 3.1, 1.7,
         'Ошибка концентрируется узкой полосой вдоль разрывов: там она в 1,7 раза выше, '
         'чем в гладких зонах.', size=9.5, ls=1.45)
    folio(s, 15)
    kit.notes(s, STORY[15][3])

    # 16 — нарушения
    s = kit.slide(prs, BG)
    head(s, 16, sub='Флаги нарушений в каждой точке — это и есть метод check_physics')
    figure(s, FIG / 'violation_maps.png', ML, 2.3, 6.6, 3.85, 4,
           'Площадь нарушений: Vanilla слева, PINN справа')
    kit.vrule(s, ML + 6.95, 2.3, 3.9, HAIR, 0.75)
    for i, (k, v) in enumerate([('Vanilla', FACTS['viol_van'] + ' точек'), ('PINN', FACTS['viol_pinn'] + ' точек'),
                                ('Площадь, Vanilla', '40 %'), ('Площадь, PINN', '0,7 %')]):
        y = 2.35 + i * 0.68
        kit.text(s, ML + 7.35, y, 2.2, 0.26, k, size=9.5, color=MUT, font=BODY)
        kit.text(s, ML + 7.35, y + 0.24, 2.6, 0.3, v, size=12.5, color=INK, font=H1)
        kit.hrule(s, ML + 7.35, y + 0.6, 2.6, HAIR, 0.5)
    body(s, ML + 7.35, 5.15, 2.7, 1.1,
         'У PINN остаётся тонкая полоса на стыке регионов, где разрывна сама таблица.',
         size=9, ls=1.4)
    folio(s, 16)
    kit.notes(s, STORY[16][3])

    # 17 — скорость звука
    s = kit.slide(prs, BG)
    head(s, 17, sub='Самая чувствительная к производным величина: сверка с табличными конечными разностями')
    figure(s, FIG / 'cs_scatter.png', ML, 2.3, 5.6, 4.0, 5,
           'c_s по PINN против табличной c_s, км/с; линия — идеальное совпадение')
    kit.vrule(s, ML + 5.95, 2.3, 4.1, HAIR, 0.75)
    for i, (k, v) in enumerate([('R² в лог-шкале', FACTS['cs_r2']), ('Медианное отклонение', FACTS['cs_med']),
                                ('p95 отклонения', FACTS['cs_p95']), ('Точек с c_s ≥ c', '0 %')]):
        y = 2.35 + i * 0.72
        kit.text(s, ML + 6.35, y, 2.6, 0.26, k, size=9.5, color=MUT, font=BODY)
        kit.text(s, ML + 6.35, y + 0.24, 2.6, 0.32, v, size=14, color=INK, font=H1)
        kit.hrule(s, ML + 6.35, y + 0.62, 3.3, HAIR, 0.5)
    body(s, ML + 6.35, 5.5, 3.4, 0.8,
         'Расхождения — там, где табличная c_s не определена.', size=9, ls=1.4)
    folio(s, 17)
    kit.notes(s, STORY[17][3])

    # 18 — обёртка
    s = kit.slide(prs, BG)
    head(s, 18, sub='Класс-обёртка на 90 строк: docstrings Google-style, проверка области определения')
    kit.code_block(s, ML, 2.35, 6.4, 4.15, WRAPPER_CODE, bg=PANEL, fg=INK, cmt=MUT,
                   accent=ACC, size=9.5, bar=ACC)
    kit.vrule(s, ML + 6.75, 2.35, 4.0, HAIR, 0.75)
    for i, (k, v) in enumerate([('predict', 'векторный инференс P и e'),
                                ('sound_speed', 'autograd внутри, СГС на выходе'),
                                ('check_physics', 'маски нарушений и флаг ok'),
                                ('in_domain', 'границы области определения')]):
        y = 2.4 + i * 0.85
        kit.text(s, ML + 7.15, y, 3.9, 0.26, k, size=10.5, color=INK, font=MONO)
        kit.text(s, ML + 7.15, y + 0.24, 3.9, 0.26, v, size=9.5, color=MUT, font=BODY)
        kit.hrule(s, ML + 7.15, y + 0.6, 3.9, HAIR, 0.5)
    kit.text(s, ML + 7.15, 5.95, 3.9, 0.3, '10⁵ запросов — 0,13 с на CPU', size=9,
             color=ACC, font=BODY, italic=True)
    folio(s, 18)
    kit.notes(s, STORY[18][3])

    # 19 — сжатие
    s = kit.slide(prs, BG)
    head(s, 19, sub='Дополнительный этап кейса: измеримый эффект оптимизации модели')
    figure(s, FIG / 'size_speed.png', ML, 2.3, 6.5, 3.9, 6,
           'Размер весов и время одиночного запроса')
    data = [['Вариант', 'Размер', 'мкс'], ['fp32', '0,099 МБ', FACTS['fp32_us']],
            ['TorchScript', '0,107 МБ', FACTS['ts_us']], ['int8', '0,031 МБ', FACTS['int8_us']]]
    kit.table(s, ML + 6.9, 2.35, 3.9, 1.8, data, col_w=[1.5, 1.2, 0.8], size=9.5,
              head_size=8.5, ink=INK, muted=MUT, header_fill=None, zebra=None,
              align=['l', 'c', 'c'], font=BODY, head_font=BODY)
    for r in range(4):
        kit.hrule(s, ML + 6.9, 2.35 + 0.45 * r, 4.3, HAIR if r else INK, 0.5 if r else 0.75)
    kit.vrule(s, ML + 6.65, 2.3, 4.0, HAIR, 0.75)
    body(s, ML + 6.9, 4.45, 4.3, 1.9,
         'TorchScript ускоряет batch-1 в 1,6 раза без потери точности. int8 сжимает веса в '
         '3,2 раза при p99 отклонения 0,031 в нормированных единицах. Для гидрокода выбираем '
         'TorchScript.', size=9.5, ls=1.45)
    folio(s, 19)
    kit.notes(s, STORY[19][3])

    # 20 — итоги
    s = kit.slide(prs, BG)
    head(s, 20, sub='Решение закрывает чек-лист; ниже — ограничения и план развития')
    cols = [('Сделано', DONE), ('Ограничения', LIMITS), ('Дальше', NEXT)]
    for i, (t_, items) in enumerate(cols):
        x = ML + i * 3.85
        kit.text(s, x, 2.32, 3.5, 0.22, t_.upper(), size=8.5, color=ACC if i == 0 else MUT,
                 font=BODY, caps=True, tracking=1.6)
        kit.hrule(s, x, 2.58, 3.5, INK if i == 0 else HAIR, 0.75)
        kit.bullets(s, x, 2.7, 3.5, 2.9, items, size=9.5, color=INK, font=BODY, gap=8,
                    bullet='—', bullet_color=ACC, ls=1.5, bold_lead=False)
    kit.hrule(s, ML, 5.95, CW, INK, 0.75)
    kit.text(s, ML, 6.08, 3.0, 0.22, 'АРТЕФАКТЫ', size=8.5, color=MUT, font=BODY, caps=True,
             tracking=1.6)
    kit.text(s, ML, 6.32, CW, 0.5, ARTIFACTS, size=9, color=INK, font=MONO, ls=1.5)
    folio(s, 20)
    kit.notes(s, STORY[20][3])

    prs.save(out)
    return out


if __name__ == '__main__':
    print(build('presentation/03_Editorial_журнал.pptx'))
