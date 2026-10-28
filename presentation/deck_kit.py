"""Минимальный набор примитивов для сборки тёмной научной презентации (python-pptx)."""
from __future__ import annotations

from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

# ---------------------------------------------------------------- палитра
BG = RGBColor(0x0B, 0x12, 0x20)
PANEL = RGBColor(0x11, 0x1C, 0x30)
PANEL2 = RGBColor(0x16, 0x24, 0x3B)
BORDER = RGBColor(0x24, 0x36, 0x53)
CYAN = RGBColor(0x3D, 0xDC, 0xFF)
MINT = RGBColor(0x5C, 0xE1, 0xB9)
AMBER = RGBColor(0xFF, 0xB8, 0x4D)
ROSE = RGBColor(0xFF, 0x6E, 0x8A)
VIOLET = RGBColor(0xA7, 0x8B, 0xFF)
WHITE = RGBColor(0xEA, 0xF2, 0xFF)
MUTED = RGBColor(0x93, 0xA8, 0xC6)
DIM = RGBColor(0x5E, 0x74, 0x93)

FONT = 'Arial'
MONO = 'Consolas'

SLIDE_W = 13.333
SLIDE_H = 7.5
ML = 0.78          # левое поле
MR = 0.78          # правое поле
CW = SLIDE_W - ML - MR


def _noline(shape):
    shape.line.fill.background()
    return shape


def rect(slide, x, y, w, h, fill=None, line=None, lw=1.0, shape=MSO_SHAPE.RECTANGLE,
         transparency=0, radius=None):
    """Прямоугольник/карточка в дюймах."""
    shp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(lw)
    shp.shadow.inherit = False
    if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        shp.adjustments[0] = radius
    if transparency and fill is not None:
        shp.fill.transparency = transparency
    if shp.has_text_frame:
        shp.text_frame.text = ''
    return shp


def text(slide, x, y, w, h, s, size=14, color=WHITE, bold=False, italic=False,
         align='l', anchor='t', font=FONT, line_spacing=1.15, space_after=0,
         char_spacing=None, wrap=True):
    """Текстовый блок. s — строка или список строк (каждый элемент — новый абзац)."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {'t': MSO_ANCHOR.TOP, 'm': MSO_ANCHOR.MIDDLE,
                          'b': MSO_ANCHOR.BOTTOM}[anchor]
    lines = [s] if isinstance(s, str) else list(s)
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {'l': PP_ALIGN.LEFT, 'c': PP_ALIGN.CENTER,
                       'r': PP_ALIGN.RIGHT, 'j': PP_ALIGN.JUSTIFY}[align]
        p.line_spacing = line_spacing
        p.space_after = Pt(space_after)
        run = p.add_run()
        run.text = line
        f = run.font
        f.name = font
        f.size = Pt(size)
        f.bold = bold
        f.italic = italic
        f.color.rgb = color
        if char_spacing is not None:
            rPr = run._r.get_or_add_rPr()
            rPr.set('spc', str(int(char_spacing * 100)))
    return tb


def rich(slide, x, y, w, h, parts, align='l', anchor='t', line_spacing=1.2):
    """Абзац с фрагментами разного стиля.

    parts: список dict(text=..., size=, color=, bold=, font=) — в один абзац.
    """
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {'t': MSO_ANCHOR.TOP, 'm': MSO_ANCHOR.MIDDLE,
                          'b': MSO_ANCHOR.BOTTOM}[anchor]
    p = tf.paragraphs[0]
    p.alignment = {'l': PP_ALIGN.LEFT, 'c': PP_ALIGN.CENTER, 'r': PP_ALIGN.RIGHT}[align]
    p.line_spacing = line_spacing
    for part in parts:
        run = p.add_run()
        run.text = part['text']
        f = run.font
        f.name = part.get('font', FONT)
        f.size = Pt(part.get('size', 14))
        f.bold = part.get('bold', False)
        f.italic = part.get('italic', False)
        f.color.rgb = part.get('color', WHITE)
    return tb


def bullets(slide, x, y, w, h, items, size=14, color=WHITE, gap=7,
            bullet_color=CYAN, line_spacing=1.25, bullet='—', bold_lead=True):
    """Список с маркерами; элемент может быть 'Заголовок — текст'."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = line_spacing
        p.space_after = Pt(gap)
        r = p.add_run()
        r.text = f'{bullet}  '
        r.font.name = FONT
        r.font.size = Pt(size)
        r.font.color.rgb = bullet_color
        r.font.bold = True
        if ' — ' in item and bold_lead:
            lead, rest = item.split(' — ', 1)
            r2 = p.add_run(); r2.text = lead
            r2.font.name = FONT; r2.font.size = Pt(size); r2.font.bold = True
            r2.font.color.rgb = WHITE
            r3 = p.add_run(); r3.text = ' — ' + rest
            r3.font.name = FONT; r3.font.size = Pt(size); r3.font.color.rgb = color
        else:
            r2 = p.add_run(); r2.text = item
            r2.font.name = FONT; r2.font.size = Pt(size); r2.font.color.rgb = color
    return tb


def picture(slide, path, x, y, w, h, align='c'):
    """Вставка изображения с вписыванием в рамку (сохраняя пропорции)."""
    from PIL import Image
    iw, ih = Image.open(path).size
    scale = min(w / iw, h / ih)
    pw, ph = iw * scale, ih * scale
    px = x + (w - pw) / 2 if align == 'c' else x
    py = y + (h - ph) / 2
    return slide.shapes.add_picture(str(path), Inches(px), Inches(py),
                                    Inches(pw), Inches(ph))


def table(slide, x, y, w, h, data, col_w=None, header=True, size=11.5,
          header_size=10.5, row_h=None, accents=None, align=None,
          header_fill=PANEL2, zebra=(PANEL, BG), first_col_bold=True):
    """Таблица с оформлением под тёмную тему.

    data: список списков строк; accents: цвет подсветки для каждой строки (или None).
    """
    rows, cols = len(data), len(data[0])
    shape = slide.shapes.add_table(rows, cols, Inches(x), Inches(y), Inches(w), Inches(h))
    tbl = shape.table
    tbl.first_row = False
    tbl.horz_banding = False
    if col_w:
        total = sum(col_w)
        for i, cw in enumerate(col_w):
            tbl.columns[i].width = Emu(int(Inches(w) * cw / total))
    if row_h:
        for i, rh in enumerate(row_h):
            tbl.rows[i].height = Inches(rh)

    for r in range(rows):
        for c in range(cols):
            cell = tbl.cell(r, c)
            cell.margin_left = Inches(0.10)
            cell.margin_right = Inches(0.08)
            cell.margin_top = Inches(0.045)
            cell.margin_bottom = Inches(0.045)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            if r == 0 and header:
                cell.fill.fore_color.rgb = header_fill
            else:
                cell.fill.fore_color.rgb = zebra[(r - 1) % 2] if header else zebra[r % 2]
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = (PP_ALIGN.LEFT if c == 0 else PP_ALIGN.CENTER) if align is None \
                else {'l': PP_ALIGN.LEFT, 'c': PP_ALIGN.CENTER, 'r': PP_ALIGN.RIGHT}[align[c]]
            run = p.add_run()
            run.text = str(data[r][c])
            f = run.font
            f.name = FONT
            f.size = Pt(header_size if (r == 0 and header) else size)
            f.bold = (r == 0 and header) or (first_col_bold and c == 0)
            f.color.rgb = MUTED if (r == 0 and header) else WHITE
            if r == 0 and header and accents and accents[r]:
                f.color.rgb = accents[r]
    return tbl
