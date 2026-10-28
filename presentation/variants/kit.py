"""Общие примитивы для пяти дек. Все размеры — в дюймах, холст 13.333 × 7.5."""
from __future__ import annotations

from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

W, H = 13.333, 7.5
ASSETS = Path(__file__).resolve().parents[1] / 'assets'
FIGS = Path(__file__).resolve().parents[1] / 'figures'
LIGHT = Path(__file__).resolve().parent / 'figs_light'

ALIGN = {'l': PP_ALIGN.LEFT, 'c': PP_ALIGN.CENTER, 'r': PP_ALIGN.RIGHT, 'j': PP_ALIGN.JUSTIFY}
ANCHOR = {'t': MSO_ANCHOR.TOP, 'm': MSO_ANCHOR.MIDDLE, 'b': MSO_ANCHOR.BOTTOM}


def deck():
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    return prs


def slide(prs, bg=None):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    if bg is not None:
        rect(s, 0, 0, W, H, fill=bg)
    return s


def set_alpha(shp, alpha):
    """Прозрачность заливки через a:alpha (python-pptx не умеет читать/писать alpha)."""
    from pptx.oxml.ns import qn
    srgb = shp.fill._xPr.find(qn('a:solidFill'))
    if srgb is None:
        return
    srgb = srgb.find(qn('a:srgbClr'))
    if srgb is None:
        return
    el = srgb.makeelement(qn('a:alpha'), {'val': str(int(alpha * 100000))})
    srgb.append(el)


def rect(s, x, y, w, h, fill=None, line=None, lw=0.75, shape=MSO_SHAPE.RECTANGLE,
         radius=None, transparency=None, dash=None):
    shp = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
        if transparency:
            a = transparency / 100 if transparency > 1 else transparency
            set_alpha(shp, min(max(a, 0.0), 0.98))
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(lw)
        if dash:
            from pptx.enum.dml import MSO_LINE_DASH_STYLE
            shp.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    shp.shadow.inherit = False
    if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        shp.adjustments[0] = radius
    if shp.has_text_frame:
        shp.text_frame.text = ''
    return shp


def oval(s, x, y, w, h, fill=None, line=None, lw=0.75):
    return rect(s, x, y, w, h, fill=fill, line=line, lw=lw, shape=MSO_SHAPE.OVAL)


def rrect(s, x, y, w, h, radius=0.06, **kw):
    return rect(s, x, y, w, h, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=radius, **kw)


def _style_run(r, size, color, font, bold, italic, tracking):
    f = r.font
    f.name, f.size, f.bold, f.italic = font, Pt(size), bold, italic
    f.color.rgb = color
    if tracking:
        r._r.get_or_add_rPr().set('spc', str(int(tracking * 100)))


def text(s, x, y, w, h, body, size=14, color=None, font='Arial', bold=False,
         italic=False, align='l', anchor='t', ls=1.15, space_after=0,
         tracking=None, caps=False, prs_theme=None):
    color = color if color is not None else (prs_theme['ink'] if prs_theme else RGBColor(0, 0, 0))
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = ANCHOR[anchor]
    lines = [body] if isinstance(body, str) else list(body)
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = ALIGN[align]
        p.line_spacing = ls
        p.space_after = Pt(space_after)
        r = p.add_run()
        r.text = line.upper() if caps else line
        _style_run(r, size, color, font, bold, italic, tracking)
    return tb


def rich(s, x, y, w, h, parts, align='l', anchor='t', ls=1.15, space_after=0):
    """parts: список dict(t=текст, size, color, font, bold, italic, tracking)."""
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = ANCHOR[anchor]
    p = tf.paragraphs[0]
    p.alignment = ALIGN[align]
    p.line_spacing = ls
    p.space_after = Pt(space_after)
    for part in parts:
        r = p.add_run()
        r.text = part['t']
        _style_run(r, part.get('size', 14), part.get('color', RGBColor(0, 0, 0)),
                   part.get('font', 'Arial'), part.get('bold', False),
                   part.get('italic', False), part.get('tracking'))
    return tb


def bullets(s, x, y, w, h, items, size=14, color=None, font='Arial', gap=8,
            bullet='—', bullet_color=None, lead_color=None, ls=1.25, bold_lead=True):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = ls
        p.space_after = Pt(gap)
        if bullet:
            r = p.add_run()
            r.text = bullet + '  '
            f = r.font
            f.name, f.size = font, Pt(size)
            f.color.rgb = bullet_color or color
            f.bold = True
        if bold_lead and ' — ' in item:
            lead, rest = item.split(' — ', 1)
            r2 = p.add_run(); r2.text = lead
            _style_run(r2, size, lead_color or color, font, True, False, None)
            r3 = p.add_run(); r3.text = ' — ' + rest
            _style_run(r3, size, color, font, False, False, None)
        else:
            r2 = p.add_run(); r2.text = item
            _style_run(r2, size, color, font, False, False, None)
    return tb


def pic_cover(s, path, x, y, w, h, focus=(0.5, 0.5)):
    """Фото, обрезанное под рамку (заполняет её целиком)."""
    iw, ih = Image.open(path).size
    ar_t, ar_i = w / h, iw / ih
    cl = cr = ct = cb = 0.0
    if ar_i > ar_t:
        crop = 1 - ar_t / ar_i
        cl, cr = crop * focus[0], crop * (1 - focus[0])
    else:
        crop = 1 - ar_i / ar_t
        ct, cb = crop * focus[1], crop * (1 - focus[1])
    pic = s.shapes.add_picture(str(path), Inches(x), Inches(y), Inches(w), Inches(h))
    pic.crop_left, pic.crop_right, pic.crop_top, pic.crop_bottom = cl, cr, ct, cb
    return pic


def pic_fit(s, path, x, y, w, h, align='c'):
    iw, ih = Image.open(path).size
    k = min(w / iw, h / ih)
    pw, ph = iw * k, ih * k
    px = x + (w - pw) / 2 if align == 'c' else x
    return s.shapes.add_picture(str(path), Inches(px), Inches(y + (h - ph) / 2),
                                Inches(pw), Inches(ph))


def pic_in_oval(s, path, x, y, d):
    """Круглый кроп фото: картинка + круг-маска не нужна, используем crop в квадрат."""
    return pic_cover(s, path, x, y, d, d)


def hrule(s, x, y, w, color, lw=1.0):
    shp = s.shapes.add_connector(1, Inches(x), Inches(y), Inches(x + w), Inches(y))
    shp.line.color.rgb = color
    shp.line.width = Pt(lw)
    return shp


def vrule(s, x, y, h, color, lw=1.0):
    shp = s.shapes.add_connector(1, Inches(x), Inches(y), Inches(x), Inches(y + h))
    shp.line.color.rgb = color
    shp.line.width = Pt(lw)
    return shp


def table(s, x, y, w, h, data, col_w=None, row_h=None, size=11.5, head_size=10,
          ink=None, muted=None, header_fill=None, zebra=None, line=None,
          header_line=None, font='Arial', align=None, head_font=None,
          head_color=None, first_bold=True, pad=0.10):
    rows, cols = len(data), len(data[0])
    shp = s.shapes.add_table(rows, cols, Inches(x), Inches(y), Inches(w), Inches(h))
    tbl = shp.table
    tbl.first_row = False
    tbl.horz_banding = False
    # убираем встроенный стиль таблицы, иначе PowerPoint рисует синие полосы
    from pptx.oxml.ns import qn
    tblPr = tbl._tbl.tblPr
    for el in tblPr.findall(qn('a:tableStyleId')):
        tblPr.remove(el)
    sid = tblPr.makeelement(qn('a:tableStyleId'), {})
    sid.text = '{2D5ABB26-0587-4C30-8999-92F81FD0307C}'
    tblPr.append(sid)
    if col_w:
        tot = sum(col_w)
        for i, cw in enumerate(col_w):
            tbl.columns[i].width = Emu(int(Inches(w) * cw / tot))
    if row_h:
        for i, rh in enumerate(row_h):
            tbl.rows[i].height = Inches(rh)
    for r in range(rows):
        for c in range(cols):
            cell = tbl.cell(r, c)
            cell.margin_left = Inches(pad)
            cell.margin_right = Inches(0.08)
            cell.margin_top = Inches(0.04)
            cell.margin_bottom = Inches(0.04)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            fill = header_fill if r == 0 else (zebra[(r - 1) % len(zebra)] if zebra else None)
            if fill is None:
                cell.fill.background()
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = fill
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            a = (align[c] if align else ('l' if c == 0 else 'c'))
            p.alignment = ALIGN[a]
            run = p.add_run()
            run.text = str(data[r][c])
            is_head = (r == 0)
            f = run.font
            f.name = head_font or font
            f.size = Pt(head_size if is_head else size)
            f.bold = is_head or (first_bold and c == 0)
            f.color.rgb = (head_color or muted) if is_head else ink
    return tbl


def code_block(s, x, y, w, h, lines, bg, fg, cmt, accent, font='Consolas',
               size=9.5, pad=0.22, bar=None):
    rect(s, x, y, w, h, fill=bg)
    if bar is not None:
        rect(s, x, y, 0.055, h, fill=bar)
    tb = s.shapes.add_textbox(Inches(x + pad), Inches(y + pad * 0.7),
                              Inches(w - 2 * pad), Inches(h - pad))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = 1.22
        run = p.add_run()
        run.text = line if line else ' '
        f = run.font
        f.name, f.size = font, Pt(size)
        is_cmt = line.strip().startswith('#')
        f.color.rgb = cmt if is_cmt else fg
        f.bold = bool(line.strip().startswith('loss')) and not is_cmt
    return tb


def kpi(s, x, y, w, value, label, color, ink, font='Arial', vsize=40, lsize=10.5,
        bold=True, align='l', tracking=None):
    text(s, x, y, w, vsize / 60.0, value, size=vsize, color=color, font=font,
         bold=bold, align=align, ls=0.95, tracking=tracking)
    text(s, x, y + vsize / 60.0 * 1.12, w, 0.5, label, size=lsize, color=ink,
         font=font, align=align, ls=1.1)


def notes(s, txt):
    s.notes_slide.notes_text_frame.text = txt
