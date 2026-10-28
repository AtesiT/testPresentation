"""Вариант 5 — Report / годовой отчёт: тёплая бумага, карточки, глубокий зелёный."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kit
import themes
from content import (ARTIFACTS, CHECKLIST, CODE_LINES, CONSTRAINTS, DONE, FACTS,
                     LIMITS, NEXT, STORY, WRAPPER_CODE)

T = themes.REPORT
BG, CARD, INK, MUT = T['bg'], T['panel'], T['ink'], T['muted']
ACC, ACC2, LINE, HAIR = T['accent'], T['accent2'], T['line'], T['hair']
H1, BODY, MONO = T['head'], T['body'], T['mono']
ML, MR = 0.85, 0.85
CW = kit.W - ML - MR
FIG = kit.LIGHT / 'report'
IMG = kit.ASSETS


def card(s, x, y, w, h, fill=None, radius=0.05, line=None):
    return kit.rrect(s, x, y, w, h, radius=radius, fill=fill or CARD,
                     line=line if line is not None else HAIR, lw=0.75)


def head(s, num, title=None, sub=None, kicker=None):
    kicker = (kicker or STORY[num][0]).upper()
    title = title or STORY[num][1]
    sub = STORY[num][2] if sub is None else sub
    kit.text(s, ML, 0.5, 7.4, 0.22, kicker, size=9, color=ACC, font=BODY, bold=True,
             tracking=1.6)
    kit.text(s, kit.W - MR - 1.6, 0.46, 1.6, 0.3, f'{num:02d}', size=16, color=LINE,
             font=H1, align='r')
    kit.text(s, ML, 0.86, CW - 0.4, 0.7, title, size=28, color=INK, font=H1, ls=1.08)
    if sub:
        kit.text(s, ML, 1.6, CW - 1.8, 0.5, sub, size=11.5, color=MUT, font=BODY, ls=1.3)
    kit.hrule(s, ML, 2.12, CW, LINE, 1.0)


def foot(s, left='Физически согласованный суррогат УРС алюминия · 2026'):
    kit.hrule(s, ML, 7.06, CW, HAIR, 0.75)
    kit.text(s, ML, 7.14, 7.5, 0.2, left, size=8, color=MUT, font=BODY)
    kit.text(s, kit.W - MR - 3.0, 7.14, 3.0, 0.2, 'ИТ КоР · трек ML · кейс 01', size=8,
             color=MUT, font=BODY, align='r')


def badge(s, x, y, d, txt, color=None):
    kit.oval(s, x, y, d, d, fill=color or ACC)
    kit.text(s, x, y + d / 2 - 0.16, d, 0.3, txt, size=12, color=T['on_accent'],
             font=BODY, bold=True, align='c')


def photo(s, name, x, y, w, h, focus=(0.5, 0.5), frame=True, cap=None):
    if frame:
        kit.rect(s, x - 0.09, y - 0.09, w + 0.18, h + 0.18, fill=CARD, line=HAIR, lw=0.75)
    kit.pic_cover(s, IMG / name, x, y, w, h, focus=focus)
    if cap:
        kit.text(s, x - 0.09, y + h + 0.14, w + 0.18, 0.24, cap, size=8, color=MUT,
                 font=BODY, italic=True)


def build(out):
    prs = kit.deck()

    # 1 — обложка
    s = kit.slide(prs, BG)
    kit.pic_cover(s, IMG / 'photo_ingots.jpg', 0, 0, kit.W, 4.35, focus=(0.5, 0.4))
    kit.rect(s, 0, 4.35, kit.W, 3.15, fill=BG)
    kit.rect(s, 0, 4.28, kit.W, 0.07, fill=ACC)
    kit.text(s, ML, 4.65, 8.0, 0.24, 'ИТ КоР · трек Machine Learning · кейс 01 · алюминий',
             size=9.5, color=ACC, font=BODY, bold=True, tracking=1.8)
    kit.text(s, ML, 4.95, 6.9, 1.5,
             ['Физически согласованный', 'суррогат уравнения', 'состояния'],
             size=28, color=INK, font=H1, ls=1.12)
    kit.text(s, ML, 6.28, 6.4, 0.7, 'PINN вместо таблицы: P(ρ,T), e(ρ,T) и c_s. '
             '0,10 МБ, 0,43 % нарушений физики.', size=11, color=MUT, font=BODY, ls=1.35)
    for i, (v, l) in enumerate([(FACTS['viol_pinn'], 'нарушений'), (f"×{FACTS['ratio']}", 'к vanilla'),
                                ('0,10 МБ', 'вес'), (FACTS['us'] + ' мкс', 'запрос')]):
        x = ML + 6.45 + i * 1.33
        kit.text(s, x, 6.3, 1.35, 0.3, v, size=11.5, color=ACC, font=BODY, bold=True)
        kit.text(s, x, 6.62, 1.35, 0.2, l, size=7.5, color=MUT, font=BODY)
    kit.text(s, ML, 7.05, 6.0, 0.2, 'Автор: <имя> · команда: <состав>', size=8.5,
             color=MUT, font=BODY)
    kit.notes(s, STORY[1][3])

    # 2 — постановка
    s = kit.slide(prs, BG)
    head(s, 2, sub='Три требования кейса: точность по таблице, знаки производных, габарит модели')
    for i, (t_, d) in enumerate([('Точность', 'P и e по всей фазовой диаграмме, а не только в узлах сетки'),
                                 ('Физика', '∂P/∂ρ > 0, ∂e/∂T > 0, 0 < c_s < c в каждой точке'),
                                 ('Габарит', 'модель до 10 МБ, ответ за микросекунды, без GPU')]):
        y = 2.45 + i * 1.25
        card(s, ML, y, 7.0, 1.05)
        badge(s, ML + 0.25, y + 0.24, 0.56, str(i + 1), ACC if i < 2 else ACC2)
        kit.text(s, ML + 1.05, y + 0.2, 5.7, 0.3, t_, size=13, color=INK, font=H1)
        kit.text(s, ML + 1.05, y + 0.58, 5.7, 0.4, d, size=10, color=MUT, font=BODY, ls=1.3)
    photo(s, 'photo_lab.jpg', ML + 7.6, 2.45, 3.7, 3.55, focus=(0.5, 0.45),
          cap='Гидрокод и его уравнения — заказчик суррогата')
    kit.text(s, ML, 6.45, 7.2, 0.5, 'Оцениваем не только MSE, но и долю точек, где нарушена физика.',
             size=10.5, color=ACC, font=BODY, bold=True)
    foot(s)
    kit.notes(s, STORY[2][3])

    # 3 — чек-лист
    s = kit.slide(prs, BG)
    head(s, 3, sub='Девять критериев финального задания — по 100 баллов в сумме')
    for i, (name, pts, what) in enumerate(CHECKLIST):
        r, c = divmod(i, 3)
        x = ML + c * 3.95
        y = 2.4 + r * 1.5
        card(s, x, y, 3.72, 1.32)
        badge(s, x + 0.22, y + 0.22, 0.42, pts, ACC)
        kit.text(s, x + 0.78, y + 0.2, 2.8, 0.3, name, size=9.5, color=INK, font=BODY, bold=True)
        kit.text(s, x + 0.78, y + 0.58, 2.8, 0.65, what, size=8, color=MUT, font=BODY, ls=1.25)
    foot(s, 'Итого 100 / 100 — каждый пункт подтверждается артефактом в репозитории')
    kit.notes(s, STORY[3][3])

    # 4 — данные
    s = kit.slide(prs, BG)
    kit.pic_cover(s, IMG / 'photo_molten.jpg', 0, 0, kit.W, 2.15, focus=(0.5, 0.45))
    kit.rect(s, 0, 0, kit.W, 2.15, fill=themes.C('14251C'), transparency=42)
    kit.text(s, ML, 0.5, 8.0, 0.24, 'ДАННЫЕ', size=9, color=T['on_accent'], font=BODY,
             bold=True, tracking=1.8)
    kit.text(s, ML, 0.82, 10.6, 0.55, '20 региональных сеток, 1 130 053 строки', size=27,
             color=T['on_accent'], font=H1)
    kit.text(s, ML, 1.5, 10.0, 0.4, 'Четыре диапазона плотности × пять диапазонов температуры; '
             'внутри региона — сетка 300 × 300', size=10.5, color=T['on_accent'], font=BODY)
    for i, (v, l) in enumerate([('1 130 053', 'точки в датасете'), ('20', 'региональных сеток'),
                                ('300 × 300', 'узлов в сетке'), ('226 011', 'точек в тесте')]):
        x = ML + i * 2.95
        card(s, x, 2.6, 2.72, 1.25)
        kit.text(s, x + 0.22, 2.78, 2.4, 0.4, v, size=18, color=ACC, font=H1)
        kit.text(s, x + 0.22, 3.28, 2.4, 0.4, l, size=8.5, color=MUT, font=BODY, ls=1.25)
    kit.text(s, ML, 4.2, 5.6, 2.3,
             ['Внутри региона таблица гладкая, на стыках значения не согласованы.',
              '9,5 % узлов полной сетки дают нефизичные производные ещё до модели.',
              'Тест — 20 % стратифицированной выборки.'],
             size=11, color=INK, font=BODY, ls=1.45, space_after=12)
    card(s, ML + 6.1, 4.2, 5.4, 2.3, fill=CARD)
    kit.text(s, ML + 6.4, 4.4, 4.8, 0.24, 'ЧТО ЭТО ЗНАЧИТ', size=8.5, color=ACC, font=BODY,
             bold=True, tracking=1.5)
    kit.text(s, ML + 6.4, 4.75, 4.8, 1.6, 'Разрывы производных — главная сложность задачи. '
             'Гладкая модель сглаживает стыки и возвращает корректные производные, но платит '
             'точностью в узлах.', size=10, color=MUT, font=BODY, ls=1.4)
    foot(s)
    kit.notes(s, STORY[4][3])

    # 5 — EDA
    s = kit.slide(prs, BG)
    head(s, 5, title='Что видно в данных')
    card(s, ML, 2.35, 8.3, 4.2, fill=CARD)
    kit.pic_fit(s, FIG / 'eda_maps.png', ML + 0.15, 2.5, 8.0, 3.6)
    kit.text(s, ML + 0.15, 6.15, 8.0, 0.25, 'log₁₀ P и знаковый логарифм e; белые полосы — '
             'стыки регионов', size=8, color=MUT, font=BODY, italic=True)
    for i, (t_, d) in enumerate([('Давление', '12 порядков → логарифм на входе и выходе'),
                                 ('Энергия', 'проходит через ноль → линейный выход'),
                                 ('Разрывы', 'видны как полосы на картах')]):
        y = 2.45 + i * 1.32
        kit.text(s, ML + 8.7, y, 3.3, 0.24, t_.upper(), size=8, color=ACC, font=BODY,
                 bold=True, tracking=1.4)
        kit.text(s, ML + 8.7, y + 0.3, 3.4, 0.8, d, size=10, color=INK, font=BODY, ls=1.35)
        kit.hrule(s, ML + 8.7, y + 1.05, 3.3, HAIR, 1.0)
    foot(s)
    kit.notes(s, STORY[5][3])

    # 6 — нормализация
    s = kit.slide(prs, BG)
    head(s, 6, sub='normalization.json — цифровой паспорт модели: проверяющий воспроизводит инференс без нашего кода')
    for i, (t_, f_, d) in enumerate([('Вход', 'x = (log₁₀ρ − a) / (b − a)', 'log₁₀ρ ∈ [−3, 4] · log₁₀T ∈ [−1, 7]'),
                                     ('Выход P', 'log₁₀P, затем 10^', 'P ∈ [10⁻⁶, 10⁶] ГПа'),
                                     ('Выход e', 'линейно, кДж/г', 'e ∈ [−0,2, 10³]')]):
        x = ML + i * 3.95
        card(s, x, 2.4, 3.7, 2.1)
        badge(s, x + 0.25, 2.6, 0.45, str(i + 1), ACC)
        kit.text(s, x + 0.85, 2.68, 2.6, 0.24, t_.upper(), size=8, color=MUT, font=BODY,
                 bold=True, tracking=1.4)
        kit.text(s, x + 0.25, 3.2, 3.2, 0.6, f_, size=10, color=INK, font=MONO, ls=1.35)
        kit.text(s, x + 0.25, 3.9, 3.2, 0.4, d, size=9, color=MUT, font=BODY, ls=1.3)
    kit.text(s, ML, 5.0, CW, 1.2, 'Все константы, единицы и границы области определения описаны '
             'в одном файле. В коде инференса нет ни одного «магического» числа — это и требование '
             'кейса, и страховка от расхождений при проверке.', size=11, color=INK, font=BODY,
             ls=1.45)
    foot(s)
    kit.notes(s, STORY[6][3])

    # 7 — baseline
    s = kit.slide(prs, BG)
    head(s, 7, sub='20 интерполяторов RegularGridInterpolator, та же тестовая выборка')
    card(s, ML, 2.35, 7.7, 3.3)
    data = [['Вариант', 'Размер', 'Медиана P', 'Покрытие', 'Нарушения'],
            ['Полная', '17,2 МБ', '0,000 %', '100 %', '2,86 %'],
            ['Прорежена ×2', '4,3 МБ', '0,0002 %', '99,4 %', '3,1 %'],
            ['Прорежена ×4', '1,1 МБ', '0,0016 %', '98,7 %', '4,4 %'],
            ['Прорежена ×8', '0,28 МБ', '0,0075 %', '96,7 %', '7,9 %']]
    kit.table(s, ML + 0.2, 2.55, 7.3, 2.1, data, col_w=[2.1, 1.1, 1.2, 1.1, 1.2], size=10,
              head_size=8.5, ink=INK, muted=MUT, header_fill=T['soft'],
              zebra=None, align=['l', 'c', 'c', 'c', 'c'], font=BODY)
    kit.text(s, ML + 0.2, 4.85, 7.3, 0.6, 'В узлах интерполяция точна — по MSE её не обогнать. '
             'Цена: 17 МБ и разрывные производные.', size=10, color=MUT, font=BODY, ls=1.35)
    kit.text(s, ML + 8.1, 2.45, 4.0, 0.24, 'РОЛЬ BASELINE', size=8.5, color=ACC, font=BODY,
             bold=True, tracking=1.5)
    kit.text(s, ML + 8.1, 2.75, 4.0, 2.6,
             ['Эталон точности в узлах сетки.',
              'Ориентир по памяти: 17 МБ против 0,10 МБ у сети.',
              'Показывает, что прореживание не спасает: таблица теряет покрытие.'],
             size=10, color=INK, font=BODY, ls=1.45, space_after=10)
    card(s, ML + 8.1, 5.5, 3.9, 1.0, fill=T['soft'])
    kit.text(s, ML + 8.35, 5.62, 3.4, 0.4, '×170', size=17, color=ACC, font=H1)
    kit.text(s, ML + 8.35, 6.05, 3.4, 0.3, 'во столько таблица тяжелее модели', size=8.5,
             color=MUT, font=BODY)
    foot(s)
    kit.notes(s, STORY[7][3])

    # 8 — почему не таблица
    s = kit.slide(prs, BG)
    head(s, 8, title='Почему таблицы недостаточно',
         sub='Даже идеальная по точности таблица даёт нефизичные производные на стыках сеток')
    kit.text(s, ML, 2.4, 5.0, 1.5, '9,5 %', size=78, color=ACC, font=H1)
    kit.text(s, ML, 3.75, 4.9, 1.0, 'узлов полной таблицы дают c_s² ≤ 0, ∂P/∂ρ ≤ 0 или '
             '∂e/∂T ≤ 0', size=11.5, color=INK, font=BODY, ls=1.4)
    kit.text(s, ML, 5.0, 4.9, 1.4, 'Пример: при ρ = 2,7 г/см³ и T ≈ 140 К энергия падает '
             'с 0,128 до 0,093 кДж/г за две ячейки — конечная разность даёт мнимое c_s.',
             size=10, color=MUT, font=BODY, ls=1.4)
    photo(s, 'photo_micro.jpg', ML + 5.4, 2.45, 4.0, 3.4, focus=(0.5, 0.4),
          cap='Микроструктура сплава — иллюстрация, не данные')
    card(s, ML + 9.85, 2.45, 2.6, 3.4, fill=ACC, line=ACC)
    kit.text(s, ML + 10.05, 2.65, 2.2, 0.3, 'ВЫВОД', size=8.5, color=T['on_accent'],
             font=BODY, bold=True, tracking=1.5)
    kit.text(s, ML + 10.05, 3.05, 2.25, 2.5, 'Нужна гладкая модель, которая восстанавливает '
             'производные между узлами таблицы.', size=11, color=T['on_accent'], font=H1, ls=1.3)
    foot(s)
    kit.notes(s, STORY[8][3])

    # 9 — vanilla
    s = kit.slide(prs, BG)
    head(s, 9, sub='2 → 128 → 128 → 64 → 2, tanh, 25 282 параметра, 150 эпох, OneCycle')
    card(s, ML, 2.35, 7.0, 4.15)
    kit.pic_fit(s, FIG / 'val_curves.png', ML + 0.15, 2.5, 6.7, 3.4)
    kit.text(s, ML + 0.15, 5.98, 6.7, 0.3, 'Кривые train/test — Vanilla MLP', size=8,
             color=MUT, font=BODY, italic=True)
    for i, (k, v) in enumerate([('R²(P)', FACTS['r2_van']), ('Медиана P', FACTS['med_van']),
                                ('R²(e)', FACTS['r2e_van'])]):
        y = 2.45 + i * 0.95
        card(s, ML + 7.35, y, 3.6, 0.8)
        kit.text(s, ML + 7.6, y + 0.14, 2.0, 0.26, k, size=9, color=MUT, font=BODY)
        kit.text(s, ML + 7.6, y + 0.38, 3.1, 0.32, v, size=13, color=INK, font=H1)
    card(s, ML + 7.35, 5.35, 3.6, 1.1, fill=ACC2, line=ACC2)
    kit.text(s, ML + 7.6, 5.5, 3.1, 0.3, 'Нарушений физики', size=8.5, color=T['on_accent'],
             font=BODY)
    kit.text(s, ML + 7.6, 5.78, 3.1, 0.4, FACTS['viol_van'], size=18, color=T['on_accent'],
             font=H1)
    foot(s)
    kit.notes(s, STORY[9][3])

    # 10 — PINN
    s = kit.slide(prs, BG)
    head(s, 10, sub='Та же архитектура; в лосс добавлены производные, посчитанные автоградиентом')
    boxes = [(ML, 'ВХОД', ['log₁₀ ρ', 'log₁₀ T']), (ML + 3.7, 'СЕТЬ', ['2 → 128 → 128', '→ 64 → 2']),
             (ML + 7.4, 'ВЫХОД', ['log₁₀ P', 'e, кДж/г'])]
    for i, (x, t_, lines) in enumerate(boxes):
        card(s, x, 2.4, 3.2, 1.3)
        kit.text(s, x + 0.25, 2.55, 2.6, 0.22, t_, size=8, color=ACC, font=BODY, bold=True,
                 tracking=1.4)
        kit.text(s, x + 0.25, 2.85, 2.7, 0.7, lines, size=11.5, color=INK, font=BODY, ls=1.35)
        if i < 2:
            kit.text(s, x + 3.28, 2.9, 0.4, 0.3, '→', size=15, color=ACC, font=BODY, bold=True)
    card(s, ML, 4.0, 10.9, 1.75, fill=ACC, line=ACC)
    kit.text(s, ML + 0.3, 4.2, 8.0, 0.24, 'ФУНКЦИЯ ПОТЕРЬ', size=8, color=T['on_accent'],
             font=BODY, bold=True, tracking=1.5)
    kit.text(s, ML + 0.3, 4.5, 10.2, 1.1, 'L = L_data + γ · (L_stab + L_cap + L_cs),  γ = 0,03. '
             'Производные берутся автоградиентом в том же графе вычислений, штрафы нормируются '
             'на медианный масштаб.', size=11, color=T['on_accent'], font=BODY, ls=1.4)
    kit.text(s, ML, 6.1, 10.9, 0.6, 'Данные дают точность, физика — корректность производных.',
             size=11, color=MUT, font=BODY)
    foot(s)
    kit.notes(s, STORY[10][3])

    # 11 — физика
    s = kit.slide(prs, BG)
    head(s, 11, sub='Формулировки из постановки кейса; проверки выполняются в системе СГС')
    for i, (name, formula, why, penalty) in enumerate(CONSTRAINTS):
        y = 2.35 + i * 1.42
        card(s, ML, y, 11.4, 1.2)
        badge(s, ML + 0.25, y + 0.32, 0.5, str(i + 1), ACC if i < 2 else ACC2)
        kit.text(s, ML + 0.98, y + 0.16, 3.3, 0.3, name, size=11.5, color=INK, font=BODY, bold=True)
        kit.text(s, ML + 0.98, y + 0.55, 4.2, 0.5, why, size=8.5, color=MUT, font=BODY, ls=1.3)
        kit.text(s, ML + 5.4, y + 0.3, 5.7, 0.5, formula, size=10, color=ACC, font=MONO, ls=1.3)
    foot(s)
    kit.notes(s, STORY[11][3])

    # 12 — код
    s = kit.slide(prs, BG)
    head(s, 12, sub='Производные в том же графе: ни численного дифференцирования, ни второй сети')
    kit.code_block(s, ML, 2.35, 6.9, 4.2, CODE_LINES, bg=themes.C('1E2A22'), fg=themes.C('EAF3EC'),
                   cmt=themes.C('8FA99A'), accent=ACC, size=9.5, bar=ACC)
    for i, (k, v) in enumerate([('γ = 0,03', 'больше — физика ломает регрессию'),
                                ('масштаб', 'делим штраф на медиану |∂P/∂ρ|'),
                                ('маска', 'физика там, где таблица физична')]):
        y = 2.5 + i * 1.25
        card(s, ML + 7.2, y, 4.2, 1.05, fill=T['soft'])
        kit.text(s, ML + 7.45, y + 0.14, 3.7, 0.24, k.upper(), size=8, color=ACC, font=BODY,
                 bold=True, tracking=1.4)
        kit.text(s, ML + 7.45, y + 0.44, 3.7, 0.5, v, size=9.5, color=INK, font=BODY, ls=1.3)
    foot(s)
    kit.notes(s, STORY[12][3])

    # 13 — обучение
    s = kit.slide(prs, BG)
    head(s, 13, sub='Разделение этапов убирает главную проблему PINN — борьбу градиентов')
    for i, (tag, desc, res, note_) in enumerate([
            ('Этап 1 · данные', '150 эпох, OneCycle, MSE', 'R²(P) ≈ 0,999', 'быстро и устойчиво'),
            ('Этап 2 · физика', 'γ = 0,03, маска разрывов, lr/10',
             f"{FACTS['viol_van']} → {FACTS['viol_pinn']}", 'чинит производные')]):
        x = ML + i * 5.95
        card(s, x, 2.4, 5.4, 2.4)
        kit.text(s, x + 0.3, 2.6, 4.8, 0.24, tag.upper(), size=8, color=ACC, font=BODY,
                 bold=True, tracking=1.4)
        kit.text(s, x + 0.3, 2.95, 4.8, 0.7, desc, size=11, color=INK, font=BODY, ls=1.35)
        kit.text(s, x + 0.3, 3.7, 4.8, 0.5, res, size=18, color=ACC, font=H1)
        kit.text(s, x + 0.3, 4.3, 4.8, 0.3, note_, size=9, color=MUT, font=BODY, italic=True)
    kit.text(s, ML + 5.5, 3.1, 0.4, 0.3, '→', size=15, color=ACC, font=BODY, bold=True)
    kit.text(s, ML, 5.1, 11.2, 1.4, 'Совместное обучение по двум лоссам сразу разваливало '
             'точность: градиенты физики забивали сигнал данных. Разделение этапов — главный '
             'инженерный приём работы; повторная физическая стадия улучшения не давала.',
             size=11, color=INK, font=BODY, ls=1.45)
    foot(s)
    kit.notes(s, STORY[13][3])

    # 14 — результаты
    s = kit.slide(prs, BG)
    head(s, 14, sub='226 011 точек теста, все метрики посчитаны одним скриптом')
    card(s, ML, 2.35, CW, 2.5)
    data = [['Подход', 'R²(P)', 'Медиана P', 'p95 P', 'R²(e)', 'Нарушения', 'Размер', 'мкс'],
            ['Baseline (таблица)', '1,00000', '0,000 %', '0,000 %', '1,00000', FACTS['viol_base'], '17,2 МБ', '0,54'],
            ['Vanilla MLP', FACTS['r2_van'], FACTS['med_van'], FACTS['p95_van'], FACTS['r2e_van'], FACTS['viol_van'], '0,10 МБ', FACTS['us_van']],
            ['PINN', FACTS['r2_pinn'], FACTS['med_pinn'], FACTS['p95_pinn'], FACTS['r2e_pinn'], FACTS['viol_pinn'], '0,10 МБ', FACTS['us']]]
    kit.table(s, ML + 0.2, 2.5, CW - 0.4, 2.2, data, col_w=[2.5, 1.2, 1.3, 1.1, 1.2, 1.4, 1.2, 0.9],
              size=10, head_size=8.5, ink=INK, muted=MUT, header_fill=T['soft'],
              zebra=None, align=['l', 'c', 'c', 'c', 'c', 'c', 'c', 'c'], font=BODY)
    kit.text(s, ML, 5.1, 7.0, 1.2, f'Точность практически равна ({FACTS["med_van"]} против '
             f'{FACTS["med_pinn"]} по медиане), но нарушений в {FACTS["ratio"]} раза меньше у PINN. '
             'Размер и скорость — в пределах требований кейса.', size=11, color=INK, font=BODY,
             ls=1.45)
    card(s, ML + 7.5, 5.05, 4.1, 1.15, fill=T['soft'])
    kit.text(s, ML + 7.75, 5.18, 3.6, 0.24, 'ГЛАВНОЕ ЧИСЛО', size=8, color=MUT, font=BODY,
             bold=True, tracking=1.4)
    kit.text(s, ML + 7.75, 5.45, 3.6, 0.6, f'×{FACTS["ratio"]} меньше нарушений', size=13,
             color=ACC, font=H1)
    foot(s)
    kit.notes(s, STORY[14][3])

    # 15 — ошибки
    s = kit.slide(prs, BG)
    head(s, 15, sub='Относительная ошибка P на сетке 240 × 320 точек по всей диаграмме')
    card(s, ML, 2.35, 8.2, 4.15)
    kit.pic_fit(s, FIG / 'error_maps.png', ML + 0.15, 2.5, 7.9, 3.55)
    kit.text(s, ML + 0.15, 6.12, 7.9, 0.25, 'Слева Vanilla, справа PINN; логарифмическая шкала, '
             '≥ 100 % обрезано', size=8, color=MUT, font=BODY, italic=True)
    for i, (k, v) in enumerate([('Разрывы', FACTS['err_jump']), ('Гладкие зоны', FACTS['err_smooth']),
                                ('Медиана', FACTS['med_pinn'])]):
        y = 2.45 + i * 0.9
        card(s, ML + 8.55, y, 3.35, 0.75)
        kit.text(s, ML + 8.8, y + 0.12, 1.8, 0.24, k, size=9, color=MUT, font=BODY)
        kit.text(s, ML + 8.8, y + 0.36, 2.8, 0.3, v, size=12, color=INK, font=H1)
    kit.text(s, ML + 8.55, 5.35, 3.4, 1.1, 'Ошибка выше в 1,7 раза именно на стыках регионов — '
             'это честная граница гладкой регрессии.', size=9, color=MUT, font=BODY, ls=1.4)
    foot(s)
    kit.notes(s, STORY[15][3])

    # 16 — нарушения
    s = kit.slide(prs, BG)
    head(s, 16, sub='Флаги нарушений в каждой точке диаграммы — это и есть check_physics')
    card(s, ML, 2.35, 7.2, 4.15)
    kit.pic_fit(s, FIG / 'violation_maps.png', ML + 0.15, 2.5, 6.9, 3.5)
    kit.text(s, ML + 0.15, 6.08, 6.9, 0.25, 'Площадь нарушений: Vanilla 40 %, PINN 0,7 %',
             size=8, color=MUT, font=BODY, italic=True)
    card(s, ML + 7.5, 2.35, 4.4, 4.15, fill=T['soft'])
    kit.pic_fit(s, FIG / 'violations_bar.png', ML + 7.65, 2.5, 4.1, 2.3)
    kit.text(s, ML + 7.7, 4.95, 4.0, 1.4, f'Vanilla: {FACTS["viol_van"]} точек. PINN: '
             f'{FACTS["viol_pinn"]}. Остаток — тонкая полоса на стыке регионов, где разрывна '
             'сама таблица. Точек с c_s ≥ c нет ни у одной модели.', size=9.5, color=INK,
             font=BODY, ls=1.4)
    foot(s)
    kit.notes(s, STORY[16][3])

    # 17 — c_s
    s = kit.slide(prs, BG)
    head(s, 17, sub='Самая чувствительная к производным величина: сверка с табличными конечными разностями')
    card(s, ML, 2.35, 6.3, 4.15)
    kit.pic_fit(s, FIG / 'cs_scatter.png', ML + 0.15, 2.5, 6.0, 3.5)
    kit.text(s, ML + 0.15, 6.08, 6.0, 0.25, 'c_s по PINN против табличной c_s, км/с',
             size=8, color=MUT, font=BODY, italic=True)
    for i, (k, v) in enumerate([('R² в лог-шкале', FACTS['cs_r2']),
                                ('Медианное отклонение', FACTS['cs_med']),
                                ('p95 отклонения', FACTS['cs_p95']),
                                ('Точек с c_s ≥ c', '0 %')]):
        y = 2.4 + i * 1.0
        card(s, ML + 6.7, y, 4.2, 0.85)
        kit.text(s, ML + 6.95, y + 0.14, 2.5, 0.24, k, size=9, color=MUT, font=BODY)
        kit.text(s, ML + 6.95, y + 0.4, 3.6, 0.32, v, size=13, color=INK, font=H1)
    foot(s)
    kit.notes(s, STORY[17][3])

    # 18 — обёртка
    s = kit.slide(prs, BG)
    head(s, 18, sub='Класс-обёртка на 90 строк: docstrings Google-style, проверка области определения')
    kit.code_block(s, ML, 2.35, 6.7, 4.15, WRAPPER_CODE, bg=themes.C('1E2A22'),
                   fg=themes.C('EAF3EC'), cmt=themes.C('8FA99A'), accent=ACC, size=9.5, bar=ACC)
    for i, (k, v) in enumerate([('predict', 'векторный инференс P и e'),
                                ('sound_speed', 'autograd внутри, СГС на выходе'),
                                ('check_physics', 'маски нарушений и флаг ok'),
                                ('in_domain', 'границы области определения')]):
        y = 2.45 + i * 0.9
        card(s, ML + 7.0, y, 4.35, 0.78)
        kit.text(s, ML + 7.25, y + 0.12, 3.8, 0.26, k, size=9.5, color=INK, font=MONO)
        kit.text(s, ML + 7.25, y + 0.42, 3.8, 0.3, v, size=8.5, color=MUT, font=BODY)
    kit.text(s, ML + 7.0, 6.1, 4.3, 0.3, '10⁵ запросов — 0,13 с на CPU', size=9, color=ACC,
             font=BODY, bold=True)
    foot(s)
    kit.notes(s, STORY[18][3])

    # 19 — сжатие
    s = kit.slide(prs, BG)
    head(s, 19, sub='Дополнительный этап кейса: измеримый эффект оптимизации модели')
    card(s, ML, 2.35, 6.4, 4.15)
    kit.pic_fit(s, FIG / 'size_speed.png', ML + 0.15, 2.5, 6.1, 3.5)
    kit.text(s, ML + 0.15, 6.08, 6.1, 0.25, 'Размер весов и время одиночного запроса',
             size=8, color=MUT, font=BODY, italic=True)
    data = [['Вариант', 'Размер', 'мкс'], ['fp32', '0,099 МБ', FACTS['fp32_us']],
            ['TorchScript', '0,107 МБ', FACTS['ts_us']],
            ['int8', '0,031 МБ', FACTS['int8_us']]]
    card(s, ML + 6.75, 2.35, 4.6, 2.05)
    kit.table(s, ML + 6.95, 2.5, 4.2, 1.75, data, col_w=[1.6, 1.2, 0.8], size=9.5, head_size=8.5,
              ink=INK, muted=MUT, header_fill=T['soft'], zebra=None,
              align=['l', 'c', 'c'], font=BODY)
    kit.text(s, ML + 6.75, 4.6, 4.6, 1.9,
             ['TorchScript ускоряет batch-1 в 1,6 раза без потери точности.',
              'int8 сжимает веса в 3,2 раза, p99 отклонения 0,031.',
              'Для гидрокода выбираем TorchScript.'],
             size=9.5, color=MUT, font=BODY, ls=1.4, space_after=8)
    foot(s)
    kit.notes(s, STORY[19][3])

    # 20 — итоги
    s = kit.slide(prs, BG)
    kit.pic_cover(s, IMG / 'photo_turbine.jpg', 0, 0, kit.W, 2.5, focus=(0.5, 0.5))
    kit.rect(s, 0, 0, kit.W, 2.5, fill=themes.C('14251C'), transparency=45)
    kit.text(s, ML, 0.6, 9.0, 0.24, 'ИТОГИ', size=9, color=T['on_accent'], font=BODY,
             bold=True, tracking=1.8)
    kit.text(s, ML, 0.95, 10.5, 0.6, 'Решение закрывает чек-лист', size=28,
             color=T['on_accent'], font=H1)
    kit.text(s, ML, 1.65, 10.0, 0.4, 'Ограничения честно названы, план развития — ниже',
             size=11, color=T['on_accent'], font=BODY)
    for i, (t_, items) in enumerate([('Сделано', DONE), ('Ограничения', LIMITS), ('Дальше', NEXT)]):
        x = ML + i * 3.85
        kit.text(s, x, 2.85, 3.5, 0.24, t_.upper(), size=8, color=ACC if i == 0 else MUT,
                 font=BODY, bold=True, tracking=1.5)
        kit.hrule(s, x, 3.15, 3.55, ACC if i == 0 else HAIR, 1.2)
        kit.bullets(s, x, 3.3, 3.55, 2.7, items, size=9.5, color=INK, font=BODY, gap=8,
                    bullet='·', bullet_color=ACC, ls=1.35, bold_lead=False)
    kit.hrule(s, ML, 6.4, CW, LINE, 1.0)
    kit.text(s, ML, 6.55, 1.8, 0.22, 'АРТЕФАКТЫ', size=8, color=MUT, font=BODY, bold=True,
             tracking=1.5)
    kit.text(s, ML + 1.9, 6.55, 9.8, 0.4, ARTIFACTS, size=8.5, color=INK, font=MONO, ls=1.4)
    kit.notes(s, STORY[20][3])

    prs.save(out)
    return out


if __name__ == '__main__':
    print(build('presentation/05_Report_отчёт.pptx'))
