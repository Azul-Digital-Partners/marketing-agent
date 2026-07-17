"""
Treasury Stack Case Study — rebuild in [Your Company] design system.

Pure visual rebuild of Reference/Treasury_Stack_Case_Study.pptx.
Content preserved verbatim; only design system applied.

Output: Marketing/output/treasury-stack-case-study-azul-2026-04-30.pptx
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree

# ============================================================
# DESIGN TOKENS — from Marketing/context/DESIGN.md
# Supports both dark (default) and light themes via CLI flag.
# ============================================================


class Theme:
    """Holds the active palette. All slide builders read from a module-level
    `T` instance set in main()."""

    def __init__(self, mode):
        self.mode = mode
        # Shared accents (used in both modes)
        self.blue       = RGBColor(0x4B, 0x9C, 0xD3)
        self.blue_light = RGBColor(0x5A, 0xAE, 0xDE)
        self.orange     = RGBColor(0xBF, 0x57, 0x00)
        self.orange_hov = RGBColor(0xD4, 0x61, 0x0A)

        if mode == "dark":
            self.bg              = RGBColor(0x0B, 0x1F, 0x3A)   # navy
            self.surface         = RGBColor(0x0D, 0x24, 0x44)   # navy-mid
            self.surface_hover   = RGBColor(0x11, 0x2B, 0x52)   # navy-light
            self.text_primary    = RGBColor(0xFF, 0xFF, 0xFF)
            self.text_body       = RGBColor(0x9A, 0xA6, 0xB6)   # ~46% white on navy
            self.text_tertiary   = RGBColor(0x6E, 0x7B, 0x8E)   # ~32% white on navy
            self.text_dim        = RGBColor(0x44, 0x52, 0x66)   # ~18% white on navy
            self.hairline        = RGBColor(0x1A, 0x2C, 0x46)
            self.hairline_strong = RGBColor(0x24, 0x37, 0x52)
            self.callout_blue_bg   = RGBColor(0x0E, 0x1F, 0x3A)
            self.callout_orange_bg = RGBColor(0x1A, 0x14, 0x0A)
        elif mode == "light":
            self.bg              = RGBColor(0xFF, 0xFF, 0xFF)
            self.surface         = RGBColor(0xF6, 0xF8, 0xFA)   # off-white
            self.surface_hover   = RGBColor(0xEE, 0xF2, 0xF7)
            self.text_primary    = RGBColor(0x11, 0x18, 0x27)   # ink
            self.text_body       = RGBColor(0x44, 0x52, 0x66)   # body gray
            self.text_tertiary   = RGBColor(0x88, 0x96, 0xA7)   # slate
            self.text_dim        = RGBColor(0xB0, 0xB8, 0xC2)
            self.hairline        = RGBColor(0xE5, 0xE7, 0xEB)   # mist
            self.hairline_strong = RGBColor(0xCB, 0xD2, 0xDA)
            self.callout_blue_bg   = RGBColor(0xF1, 0xF7, 0xFC)
            self.callout_orange_bg = RGBColor(0xFD, 0xF4, 0xEC)
        else:
            raise ValueError(f"Unknown theme mode: {mode}")


# Module-level active theme; set by main() before slide builders run.
T = Theme("dark")

SANS = "Inter"
MONO = "JetBrains Mono"

# Slide geometry — 16:9
SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
PAD_X   = Inches(0.67)   # ~64px
PAD_TOP = Inches(0.55)
PAD_BOT = Inches(0.45)


# ============================================================
# LOW-LEVEL HELPERS
# ============================================================

def set_letter_spacing(run, spacing_em, font_size_pt):
    """Set OOXML letter-spacing on a run.
    val is in hundredths of a point: spacing_em * size_pt * 100.
    """
    val = int(spacing_em * font_size_pt * 100)
    rPr = run._r.get_or_add_rPr()
    rPr.set('spc', str(val))


def set_line_spacing(paragraph, multiplier):
    """Set line-height as a multiplier (e.g. 1.6, 1.78)."""
    pPr = paragraph._pPr
    if pPr is None:
        pPr = paragraph._p.get_or_add_pPr()
    # remove existing lnSpc if any
    for child in pPr.findall(qn('a:lnSpc')):
        pPr.remove(child)
    lnSpc = etree.SubElement(pPr, qn('a:lnSpc'))
    spcPct = etree.SubElement(lnSpc, qn('a:spcPct'))
    spcPct.set('val', str(int(multiplier * 100000)))
    # Move lnSpc to top of pPr per schema
    pPr.insert(0, lnSpc)


def fill_solid(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color


def no_fill(shape):
    shape.fill.background()


def line_color(shape, color, width_pt=0.5):
    line = shape.line
    line.color.rgb = color
    line.width = Pt(width_pt)


def no_line(shape):
    shape.line.fill.background()


def add_rect(slide, x, y, w, h, fill=None, line=None, line_w=0.5):
    rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    rect.shadow.inherit = False
    # Sharp corners enforced — RECTANGLE is already sharp.
    if fill is None:
        no_fill(rect)
    else:
        fill_solid(rect, fill)
    if line is None:
        no_line(rect)
    else:
        line_color(rect, line, line_w)
    return rect


def add_textbox(slide, x, y, w, h):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    tf.word_wrap = True
    return tb, tf


def style_run(run, font=SANS, size=11, bold=False, color=T.text_primary,
              spacing_em=None, italic=False):
    f = run.font
    f.name = font
    f.size = Pt(size)
    f.bold = bold
    f.italic = italic
    f.color.rgb = color
    if spacing_em is not None:
        set_letter_spacing(run, spacing_em, size)


def add_text(slide, x, y, w, h, text, *, font=SANS, size=11, bold=False,
             color=T.text_primary, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
             spacing_em=None, line_height=None, italic=False):
    tb, tf = add_textbox(slide, x, y, w, h)
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    if line_height:
        set_line_spacing(p, line_height)
    run = p.add_run()
    run.text = text
    style_run(run, font=font, size=size, bold=bold, color=color,
              spacing_em=spacing_em, italic=italic)
    return tb, tf, p


def add_multi_text(slide, x, y, w, h, lines, *, default_size=11,
                   default_color=T.text_body, default_font=SANS,
                   line_height=1.6, anchor=MSO_ANCHOR.TOP):
    """lines: list of dicts with text + style overrides, each becomes a paragraph."""
    tb, tf = add_textbox(slide, x, y, w, h)
    tf.vertical_anchor = anchor
    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.alignment = line.get('align', PP_ALIGN.LEFT)
        lh = line.get('line_height', line_height)
        if lh:
            set_line_spacing(p, lh)
        if 'space_before' in line:
            p.space_before = Pt(line['space_before'])
        if 'space_after' in line:
            p.space_after = Pt(line['space_after'])
        run = p.add_run()
        run.text = line['text']
        style_run(
            run,
            font=line.get('font', default_font),
            size=line.get('size', default_size),
            bold=line.get('bold', False),
            italic=line.get('italic', False),
            color=line.get('color', default_color),
            spacing_em=line.get('spacing_em'),
        )
    return tb, tf


def add_hairline(slide, x, y, w, color=T.hairline):
    line = slide.shapes.add_connector(1, x, y, x + w, y)  # 1 = straight
    line.line.color.rgb = color
    line.line.width = Pt(0.5)
    return line


def add_v_hairline(slide, x, y, h, color=T.hairline):
    line = slide.shapes.add_connector(1, x, y, x, y + h)
    line.line.color.rgb = color
    line.line.width = Pt(0.5)
    return line


def add_eyebrow(slide, x, y, text, accent=T.blue, dash_w=Inches(0.30)):
    """Hairline accent + mono uppercase label. The signature pattern."""
    # Accent bar
    bar = add_rect(slide, x, y + Inches(0.075), dash_w, Inches(0.018),
                   fill=accent)
    # Label
    label_x = x + dash_w + Inches(0.10)
    label_w = Inches(8.0)
    add_text(slide, label_x, y, label_w, Inches(0.20),
             text.upper(), font=MONO, size=10, bold=False,
             color=accent, spacing_em=0.22)


def add_footer(slide, label):
    """Bottom-left mono caption: section label."""
    add_text(slide, PAD_X, SLIDE_H - PAD_BOT,
             Inches(11), Inches(0.20),
             label, font=MONO, size=8, color=T.text_dim, spacing_em=0.18)


def add_page_number(slide, num, total=29):
    add_text(slide,
             SLIDE_W - PAD_X - Inches(1.0),
             SLIDE_H - PAD_BOT,
             Inches(1.0), Inches(0.20),
             f"{num:02d} / {total:02d}",
             font=MONO, size=8, color=T.text_dim, spacing_em=0.18,
             align=PP_ALIGN.RIGHT)


def add_page_bg(slide):
    bg = add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, fill=T.bg)
    bg.shadow.inherit = False
    # Push background to back
    spTree = bg._element.getparent()
    spTree.remove(bg._element)
    spTree.insert(2, bg._element)
    return bg


def add_orange_spine(slide, x=Inches(0.40), y=Inches(0.6),
                     h=None, color=T.orange):
    """Thin vertical spine line — signature accent."""
    if h is None:
        h = SLIDE_H - Inches(1.2)
    spine = add_rect(slide, x, y, Inches(0.020), h, fill=color)
    return spine


def add_blue_left_border(shape_x, shape_y, h, slide):
    return add_rect(slide, shape_x, shape_y, Inches(0.025), h, fill=T.blue)


# ============================================================
# SLIDE BUILDERS
# ============================================================

def new_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_page_bg(slide)
    return slide


def slide_cover(prs):
    """Slide 1 — Cover."""
    slide = new_slide(prs)
    # Spine
    add_orange_spine(slide, x=Inches(0.40), y=Inches(0.8),
                     h=Inches(5.9))
    # Eyebrow
    add_eyebrow(slide, Inches(1.0), Inches(0.85),
                "[Your Company]  |  Strategy Brief", accent=T.blue)
    # Display heading — sentence case (preserving source content but adapting case
    # would be a content change; per "pure visual rebuild" we keep source text)
    add_multi_text(
        slide, Inches(1.0), Inches(1.6), Inches(11.5), Inches(2.5),
        [
            {'text': 'Treasury Management',
             'size': 56, 'bold': True, 'color': T.text_primary,
             'spacing_em': -0.030, 'line_height': 1.02},
            {'text': 'Stack Design & Financial Decisions',
             'size': 56, 'bold': True, 'color': T.text_primary,
             'spacing_em': -0.030, 'line_height': 1.02},
        ])
    # Subtitle
    add_text(slide, Inches(1.0), Inches(4.05),
             Inches(11), Inches(0.4),
             "A teaching primer + anonymized case study",
             font=SANS, size=20, bold=False, color=T.blue,
             spacing_em=-0.015)
    # Body lead
    add_multi_text(
        slide, Inches(1.0), Inches(4.65), Inches(10.5), Inches(1.1),
        [
            {'text': "How a top-30 US bank rebuilt commercial deposit "
                     "acquisition through digital transformation — and "
                     "what a credit union or mid-size FI can learn from it.",
             'size': 14, 'color': T.text_body, 'line_height': 1.55},
        ])
    # Bottom hairline + sig
    add_hairline(slide, Inches(1.0), Inches(6.45), Inches(11.3))
    add_text(slide, Inches(1.0), Inches(6.60),
             Inches(6), Inches(0.25),
             "[Your Company] LLC", font=MONO, size=10, bold=False,
             color=T.text_primary, spacing_em=0.22)
    add_text(slide, Inches(1.0), Inches(6.85),
             Inches(8), Inches(0.25),
             "Confidential — strategy brief",
             font=MONO, size=9, color=T.text_tertiary, spacing_em=0.18)
    return slide


def slide_preface(prs, num):
    """Slide 2 — Preface."""
    slide = new_slide(prs)
    add_eyebrow(slide, PAD_X, PAD_TOP, "Preface", accent=T.blue)
    add_text(slide, PAD_X, Inches(0.95), Inches(11), Inches(0.7),
             "Why this case study matters now",
             font=SANS, size=34, bold=True, color=T.text_primary,
             spacing_em=-0.025, line_height=1.1)
    add_hairline(slide, PAD_X, Inches(1.7), Inches(2.5), color=T.hairline_strong)

    body = [
        {'text': "Years ago, I was asked to lead and build a product "
                 "organization at a top-30 US bank tasked with new customer "
                 "acquisition in commercial treasury through digital "
                 "transformation.",
         'size': 14, 'color': T.text_body, 'line_height': 1.55,
         'space_after': 12},
        {'text': "The mandate looked nearly identical to what a regional "
                 "credit union or mid-size FI faces today: grow business "
                 "deposits, deepen relationships, build a sticky multi-product "
                 "book, lower cost of funds, and modernize the stack to "
                 "compete with money-center banks and fintechs.",
         'size': 14, 'color': T.text_body, 'line_height': 1.55,
         'space_after': 12},
        {'text': "What follows is a teaching primer on the treasury stack "
                 "and the financial levers that drive deposit economics — "
                 "followed by an anonymized walk-through of how that bank "
                 "built it, what worked, what hurt, and the lessons that "
                 "translate directly to a credit union or any FI starting "
                 "the same journey today.",
         'size': 14, 'color': T.text_body, 'line_height': 1.55},
    ]
    add_multi_text(slide, PAD_X, Inches(1.95), Inches(11.5), Inches(4.6), body)

    add_footer(slide, "Treasury stack & financial decisions  |  Preface")
    add_page_number(slide, num)
    return slide


def slide_roadmap(prs, num):
    """Slide 3 — Roadmap (two columns)."""
    slide = new_slide(prs)
    add_eyebrow(slide, PAD_X, PAD_TOP, "Roadmap", accent=T.blue)
    add_text(slide, PAD_X, Inches(0.95), Inches(11), Inches(0.7),
             "How this deck is built",
             font=SANS, size=34, bold=True, color=T.text_primary,
             spacing_em=-0.025)
    add_hairline(slide, PAD_X, Inches(1.7), Inches(2.5), color=T.hairline_strong)

    col_w = Inches(5.7)
    col_h = Inches(4.4)
    col1_x = PAD_X
    col2_x = Inches(7.0)
    col_y = Inches(2.05)

    # Column 1 — Teach
    add_rect(slide, col1_x, col_y, col_w, col_h,
             fill=T.surface, line=T.hairline)
    add_text(slide, col1_x + Inches(0.30), col_y + Inches(0.30),
             Inches(3), Inches(0.25),
             "PART 1 — TEACH", font=MONO, size=10, color=T.blue,
             spacing_em=0.22)
    add_text(slide, col1_x + Inches(0.30), col_y + Inches(0.62),
             col_w - Inches(0.6), Inches(0.5),
             "The framework",
             font=SANS, size=24, bold=True, color=T.text_primary,
             spacing_em=-0.02)
    add_hairline(slide, col1_x + Inches(0.30),
                 col_y + Inches(1.18),
                 Inches(0.9), color=T.blue)
    items_1 = [
        "The five-layer treasury stack",
        "Pricing models by segment",
        "Seven financial levers",
        "Buy vs. partner vs. build",
        "Decisions a leader must make",
    ]
    paragraphs = []
    for it in items_1:
        paragraphs.append({
            'text': "—  " + it,
            'size': 14, 'color': T.text_body, 'line_height': 1.6,
            'space_after': 6,
        })
    add_multi_text(slide,
                   col1_x + Inches(0.30),
                   col_y + Inches(1.40),
                   col_w - Inches(0.6), Inches(2.8),
                   paragraphs)

    # Column 2 — Apply
    add_rect(slide, col2_x, col_y, col_w, col_h,
             fill=T.surface, line=T.hairline)
    add_text(slide, col2_x + Inches(0.30), col_y + Inches(0.30),
             Inches(3), Inches(0.25),
             "PART 2 — APPLY", font=MONO, size=10, color=T.orange,
             spacing_em=0.22)
    add_text(slide, col2_x + Inches(0.30), col_y + Inches(0.62),
             col_w - Inches(0.6), Inches(0.5),
             "The case study",
             font=SANS, size=24, bold=True, color=T.text_primary,
             spacing_em=-0.02)
    add_hairline(slide, col2_x + Inches(0.30),
                 col_y + Inches(1.18),
                 Inches(0.9), color=T.orange)
    items_2 = [
        "Anonymized top-30 US bank",
        "Mandate, stakes, and starting point",
        "Product operating model build",
        "Stack and pricing decisions made",
        "Outcomes, lessons, what to copy",
    ]
    paragraphs2 = []
    for it in items_2:
        paragraphs2.append({
            'text': "—  " + it,
            'size': 14, 'color': T.text_body, 'line_height': 1.6,
            'space_after': 6,
        })
    add_multi_text(slide,
                   col2_x + Inches(0.30),
                   col_y + Inches(1.40),
                   col_w - Inches(0.6), Inches(2.8),
                   paragraphs2)

    add_footer(slide, "Treasury stack & financial decisions  |  Roadmap")
    add_page_number(slide, num)
    return slide


def slide_part_divider(prs, num, part_label, title, sub):
    """Slides 4 and 14 — Part dividers."""
    slide = new_slide(prs)
    # Big spine
    add_orange_spine(slide, x=Inches(0.40), y=Inches(1.4),
                     h=Inches(4.7))
    # Eyebrow
    add_eyebrow(slide, Inches(1.0), Inches(1.45), part_label, accent=T.orange)
    # Display
    add_text(slide, Inches(1.0), Inches(2.10), Inches(11.3), Inches(1.5),
             title,
             font=SANS, size=64, bold=True, color=T.text_primary,
             spacing_em=-0.035, line_height=1.0)
    # Hairline
    add_hairline(slide, Inches(1.0), Inches(4.60), Inches(11.3),
                 color=T.hairline_strong)
    # Sub
    add_text(slide, Inches(1.0), Inches(4.80), Inches(11), Inches(1.2),
             sub,
             font=SANS, size=18, color=T.text_body, line_height=1.5)
    add_page_number(slide, num)
    return slide


def slide_stack(prs, num):
    """Slide 5 — Five-layer stack."""
    slide = new_slide(prs)
    add_eyebrow(slide, PAD_X, PAD_TOP, "The stack", accent=T.blue)
    add_text(slide, PAD_X, Inches(0.95), Inches(11), Inches(0.7),
             "Treasury management is built in five layers",
             font=SANS, size=32, bold=True, color=T.text_primary,
             spacing_em=-0.025)
    add_text(slide, PAD_X, Inches(1.55), Inches(11.5), Inches(0.4),
             "Each layer rests on the one below. Skip a layer and you "
             "cannot serve the client above it.",
             font=SANS, size=14, color=T.text_body, line_height=1.5)
    add_hairline(slide, PAD_X, Inches(2.10), Inches(11.7),
                 color=T.hairline_strong)

    layers = [
        ("5", "Integration & experience",
         "ERP sync, APIs, mobile, dashboards",
         "Mid-market treasurers, fintechs"),
        ("4", "Liquidity & yield",
         "Sweep, ECR, IntraFi, tiered MMA",
         "All segments above $250K"),
        ("3", "Risk & controls",
         "Positive Pay, fraud, dual control, auth",
         "Required at every segment"),
        ("2", "Money movement",
         "ACH, wires, RDC, RTP, FedNow, payables",
         "Table stakes"),
        ("1", "Core & account infrastructure",
         "Multi-entity, sub-accounting, analyzed accounts",
         "Foundational"),
    ]

    row_h = Inches(0.78)
    y0 = Inches(2.30)
    for i, (num_lbl, title, desc, segment) in enumerate(layers):
        y = y0 + i * (row_h + Inches(0.07))
        # Card surface
        card = add_rect(slide, PAD_X, y, Inches(11.7), row_h,
                        fill=T.surface, line=T.hairline)
        # Layer number
        add_text(slide, PAD_X + Inches(0.30), y + Inches(0.10),
                 Inches(0.6), row_h - Inches(0.20),
                 num_lbl, font=SANS, size=32, bold=True, color=T.blue,
                 spacing_em=-0.03)
        # Title
        add_text(slide, PAD_X + Inches(1.05), y + Inches(0.13),
                 Inches(4.0), Inches(0.35),
                 title, font=SANS, size=16, bold=True, color=T.text_primary,
                 spacing_em=-0.015)
        # Description
        add_text(slide, PAD_X + Inches(1.05), y + Inches(0.45),
                 Inches(5.5), Inches(0.30),
                 desc, font=SANS, size=12, color=T.text_body,
                 line_height=1.4)
        # Vertical hairline divider before segment
        add_v_hairline(slide,
                       PAD_X + Inches(7.0),
                       y + Inches(0.15),
                       row_h - Inches(0.30),
                       color=T.hairline_strong)
        # Segment label
        add_text(slide, PAD_X + Inches(7.20), y + Inches(0.13),
                 Inches(2.0), Inches(0.25),
                 "WHO IT SERVES", font=MONO, size=8,
                 color=T.text_tertiary, spacing_em=0.20)
        add_text(slide, PAD_X + Inches(7.20), y + Inches(0.40),
                 Inches(4.3), Inches(0.30),
                 segment, font=SANS, size=12, color=T.text_primary,
                 line_height=1.3)

    add_footer(slide,
               "Treasury stack & financial decisions  |  Part 1: Framework")
    add_page_number(slide, num)
    return slide


def slide_placemat(prs, num):
    """Slide 6 — Top-30 bank placemat (dense)."""
    slide = new_slide(prs)
    add_eyebrow(slide, PAD_X, Inches(0.28), "Made concrete", accent=T.blue)
    add_text(slide, PAD_X, Inches(0.55), Inches(12), Inches(0.5),
             "The framework on a real placemat — what a top-30 bank's "
             "stack looks like",
             font=SANS, size=22, bold=True, color=T.text_primary,
             spacing_em=-0.020, line_height=1.15)
    add_text(slide, PAD_X, Inches(1.05), Inches(12), Inches(0.3),
             "Process stages across the top · platforms by stage · "
             "customer segments and exposure bands across the bottom.",
             font=SANS, size=11, color=T.text_body, line_height=1.4)

    # Source caption
    add_text(slide, PAD_X, Inches(1.35), Inches(12), Inches(0.25),
             "SOURCE: [YOUR COMPANY] FIELD EXPERIENCE, ANONYMIZED  ·  2026",
             font=MONO, size=8, color=T.text_dim, spacing_em=0.18)

    # Process stages — 5 columns
    stages = [
        "Customer\noutreach",
        "Credit review\n& decisioning",
        "Document\n& close",
        "Loan\nservicing",
        "Portfolio\nmanagement",
    ]
    col_w = Inches(2.42)
    col_y = Inches(1.70)
    col_x0 = PAD_X
    # Header row
    for i, s in enumerate(stages):
        x = col_x0 + i * col_w
        add_rect(slide, x, col_y, col_w - Inches(0.06), Inches(0.55),
                 fill=T.surface, line=T.hairline)
        add_text(slide, x + Inches(0.10), col_y + Inches(0.06),
                 col_w - Inches(0.20), Inches(0.45),
                 s.replace("\n", " "), font=SANS, size=11, bold=True,
                 color=T.text_primary, line_height=1.15)

    # Platform content per column
    platforms = [
        # 1 — Outreach
        ["CRM: Salesforce", "(Salesforce Cloud)", "",
         "Loan origination: nCino", "(Salesforce Cloud)"],
        # 2 — Credit review
        ["Appro / CRIF (ASP)", "SBA.gov portal", "nCino",
         "Relationship Pricing (AWS)", "Risk Rating Tool (AWS)",
         "Moody's Risk Origin", "Dealer Spreading (ASP)",
         "UW: Business Loan Center", "Loan Committee"],
        # 3 — Document & close
        ["nCino", "Word Merge", "CSI / DocGen",
         "DocuSign & eOriginal", "Loan Boarding Sheet (LBS)",
         "Outside Council, DEALS", "DataCap & AutoStore", "FileNet P8"],
        # 4 — Loan servicing
        ["Pega (Pega Cloud)", "AFS (in-house)",
         "Dealer Floor Plan (ASP)", "MIDAS (Canada in-house)",
         "Equipment Leasing (AWS)", "Proponix / LOC (ASP)",
         "Mortgage Warehouse (AWS)"],
        # 5 — Portfolio management
        ["nCino, Moody's Risk Origin", "Cync-ABL",
         "Portfolio Reporting (PowerBI)", "PAWave, RAMIS",
         "DCL Control Report (BIRT)", "OmniRIM Content Tracker",
         "AFR, Lereta, CSC, Title", "CEG DB, Appraisal DB",
         "FileNet P8, Special Asset Group"],
    ]
    body_y = col_y + Inches(0.65)
    body_h = Inches(2.85)
    for i, items in enumerate(platforms):
        x = col_x0 + i * col_w
        add_rect(slide, x, body_y, col_w - Inches(0.06), body_h,
                 fill=T.surface, line=T.hairline)
        paragraphs = []
        for j, it in enumerate(items):
            if it == "":
                paragraphs.append({'text': " ", 'size': 8,
                                   'color': T.text_dim, 'line_height': 1.1})
            else:
                paragraphs.append({'text': it, 'size': 9,
                                   'color': T.text_body,
                                   'line_height': 1.30,
                                   'space_after': 1})
        add_multi_text(slide, x + Inches(0.10), body_y + Inches(0.10),
                       col_w - Inches(0.22), body_h - Inches(0.20),
                       paragraphs)

    # Bottom band — segments
    seg_y = body_y + body_h + Inches(0.18)

    # LOB row
    add_text(slide, PAD_X, seg_y, Inches(2.5), Inches(0.20),
             "LINE OF BUSINESS", font=MONO, size=8,
             color=T.text_tertiary, spacing_em=0.20)
    lob_text = ("Retail bank          ·          Commercial bank          ·"
                "          Wealth management (private banking)")
    add_text(slide, PAD_X, seg_y + Inches(0.22),
             Inches(12), Inches(0.25),
             lob_text, font=SANS, size=10, color=T.text_body)

    seg_y2 = seg_y + Inches(0.45)
    add_text(slide, PAD_X, seg_y2, Inches(2.5), Inches(0.20),
             "LINE SEGMENT", font=MONO, size=8,
             color=T.text_tertiary, spacing_em=0.20)
    add_text(slide, PAD_X, seg_y2 + Inches(0.22),
             Inches(12), Inches(0.25),
             "Small business  ·  Business banking  ·  Middle market  ·  "
             "Large corporate",
             font=SANS, size=10, color=T.text_body)

    seg_y3 = seg_y2 + Inches(0.45)
    add_text(slide, PAD_X, seg_y3, Inches(3), Inches(0.20),
             "REVENUE  /  TOTAL EXPOSURE", font=MONO, size=8,
             color=T.text_tertiary, spacing_em=0.20)
    add_text(slide, PAD_X, seg_y3 + Inches(0.22),
             Inches(12), Inches(0.25),
             "$0 → $3M → $30M → $500M → $5B   ·   "
             "$0 → $100K → $1.5M → $5M → $5B+",
             font=SANS, size=10, color=T.text_primary)

    add_footer(slide,
               "Treasury stack & financial decisions  |  Part 1: Framework")
    add_page_number(slide, num)
    return slide


def slide_right_sized(prs, num):
    """Slide 7 — Right-sized stack for CU/mid-FI."""
    slide = new_slide(prs)
    add_eyebrow(slide, PAD_X, Inches(0.28), "Right-sized", accent=T.blue)
    add_text(slide, PAD_X, Inches(0.55), Inches(12), Inches(0.5),
             "What this looks like for a CU or mid-size FI — same shape, "
             "fewer parts",
             font=SANS, size=22, bold=True, color=T.text_primary,
             spacing_em=-0.020, line_height=1.15)
    add_text(slide, PAD_X, Inches(1.05), Inches(12), Inches(0.3),
             "Same five stages. Fewer platforms. Partner-led. Two "
             "segments instead of four. The model works at every scale "
             "— what changes is how you assemble it.",
             font=SANS, size=11, color=T.text_body, line_height=1.4)
    add_text(slide, PAD_X, Inches(1.35), Inches(12), Inches(0.25),
             "SOURCE: [YOUR COMPANY] FIELD EXPERIENCE  ·  2026",
             font=MONO, size=8, color=T.text_dim, spacing_em=0.18)

    stages = [
        "Customer\noutreach",
        "Credit review\n& decisioning",
        "Document\n& close",
        "Loan\nservicing",
        "Portfolio\nmanagement",
    ]
    col_w = Inches(2.42)
    col_y = Inches(1.70)
    col_x0 = PAD_X
    for i, s in enumerate(stages):
        x = col_x0 + i * col_w
        add_rect(slide, x, col_y, col_w - Inches(0.06), Inches(0.55),
                 fill=T.surface, line=T.hairline)
        add_text(slide, x + Inches(0.10), col_y + Inches(0.06),
                 col_w - Inches(0.20), Inches(0.45),
                 s.replace("\n", " "), font=SANS, size=11, bold=True,
                 color=T.text_primary, line_height=1.15)

    platforms = [
        ["CRM: HubSpot or Salesforce",
         "(or core CRM module)", "",
         "Loan origination:",
         "nCino, MeridianLink, or Baker Hill"],
        ["SBA.gov portal", "(if SBA-active)", "",
         "Same LOS extends here", "(nCino / MeridianLink)", "",
         "Decisioning layer:", "Zoot or equivalent", "",
         "Risk rating: vendor module", "or Moody's Risk Origin", "",
         "Underwriting + committee"],
        ["LOS doc generation", "(nCino / MeridianLink)", "",
         "DocuSign / eOriginal", "",
         "Outside counsel", "(for larger deals only)", "",
         "Doc storage in core or", "vendor doc management"],
        ["Core servicing module:", "Symitra, Corelation,",
         "Jack Henry, or Fiserv", "",
         "Specialty (if needed):", "Equipment leasing, ABL,",
         "or SBA servicing partner"],
        ["Portfolio reporting:", "Power BI / Tableau", "",
         "Risk monitoring:", "Moody's or Abrigo", "",
         "Property / lien tracking:", "vendor partner", "",
         "Special assets workflow"],
    ]
    body_y = col_y + Inches(0.65)
    body_h = Inches(2.85)
    for i, items in enumerate(platforms):
        x = col_x0 + i * col_w
        add_rect(slide, x, body_y, col_w - Inches(0.06), body_h,
                 fill=T.surface, line=T.hairline)
        paragraphs = []
        for it in items:
            if it == "":
                paragraphs.append({'text': " ", 'size': 5,
                                   'color': T.text_dim, 'line_height': 0.85})
            else:
                paragraphs.append({'text': it, 'size': 9,
                                   'color': T.text_body,
                                   'line_height': 1.30,
                                   'space_after': 1})
        add_multi_text(slide, x + Inches(0.10), body_y + Inches(0.10),
                       col_w - Inches(0.22), body_h - Inches(0.20),
                       paragraphs)

    # Bottom band
    seg_y = body_y + body_h + Inches(0.18)
    add_text(slide, PAD_X, seg_y, Inches(2.5), Inches(0.20),
             "LINE OF BUSINESS", font=MONO, size=8,
             color=T.text_tertiary, spacing_em=0.20)
    add_text(slide, PAD_X, seg_y + Inches(0.22),
             Inches(12), Inches(0.25),
             "Consumer / retail   ·   Member business lending (commercial)"
             "   ·   Wealth + financial planning (where applicable)",
             font=SANS, size=10, color=T.text_body)

    seg_y2 = seg_y + Inches(0.45)
    add_text(slide, PAD_X, seg_y2, Inches(2.5), Inches(0.20),
             "LINE SEGMENT", font=MONO, size=8,
             color=T.text_tertiary, spacing_em=0.20)
    add_text(slide, PAD_X, seg_y2 + Inches(0.22),
             Inches(12), Inches(0.25),
             "Micro & small business (<$1M–$10M)   ·   "
             "Business banking / lower middle market ($10M–$50M)   ·   "
             "Niche commercial (vertical fit)",
             font=SANS, size=10, color=T.text_body)

    seg_y3 = seg_y2 + Inches(0.45)
    add_text(slide, PAD_X, seg_y3, Inches(3), Inches(0.20),
             "REVENUE  /  TOTAL EXPOSURE", font=MONO, size=8,
             color=T.text_tertiary, spacing_em=0.20)
    add_text(slide, PAD_X, seg_y3 + Inches(0.22),
             Inches(12), Inches(0.25),
             "$0 → $10M → $50M → $100M+   ·   "
             "$0 → $1M → $10M → MBL cap*",
             font=SANS, size=10, color=T.text_primary)
    add_text(slide, PAD_X, seg_y3 + Inches(0.42),
             Inches(12), Inches(0.18),
             "* MBL cap: 12.25% of assets unless Low-Income Designated",
             font=MONO, size=8, color=T.text_tertiary, spacing_em=0.12,
             italic=True)

    add_footer(slide,
               "Treasury stack & financial decisions  |  Part 1: Framework")
    add_page_number(slide, num)
    return slide


def slide_layers_1_2(prs, num):
    """Slide 8 — Layers 1 & 2."""
    slide = new_slide(prs)
    add_eyebrow(slide, PAD_X, PAD_TOP, "Layers 1 & 2", accent=T.blue)
    add_text(slide, PAD_X, Inches(0.95), Inches(12), Inches(0.7),
             "Foundation: infrastructure and money movement",
             font=SANS, size=32, bold=True, color=T.text_primary,
             spacing_em=-0.025)
    add_hairline(slide, PAD_X, Inches(1.65), Inches(2.5), color=T.hairline_strong)

    col_w = Inches(5.7)
    col_h = Inches(4.85)
    col_y = Inches(2.0)

    # Layer 1
    x1 = PAD_X
    add_rect(slide, x1, col_y, col_w, col_h,
             fill=T.surface, line=T.hairline)
    # Blue left border
    add_rect(slide, x1, col_y, Inches(0.025), col_h, fill=T.blue)
    add_text(slide, x1 + Inches(0.30), col_y + Inches(0.30),
             col_w, Inches(0.25),
             "LAYER 1  ·  CORE & ACCOUNT INFRASTRUCTURE",
             font=MONO, size=9, color=T.blue, spacing_em=0.18)
    items_1 = [
        "Multi-tier business entity structures",
        "Sub-accounting under master relationship",
        "Analyzed accounts with ECR engine",
        "Account analysis statements",
        "Multi-signer entitlements",
        "Tax ID variations (EIN, ITIN, SSN)",
    ]
    paragraphs = []
    for it in items_1:
        paragraphs.append({'text': "—  " + it, 'size': 13,
                           'color': T.text_primary, 'line_height': 1.65,
                           'space_after': 4})
    add_multi_text(slide, x1 + Inches(0.30), col_y + Inches(0.75),
                   col_w - Inches(0.6), Inches(2.8), paragraphs)
    # Decision callout
    dec_y = col_y + col_h - Inches(1.2)
    add_hairline(slide, x1 + Inches(0.30), dec_y, col_w - Inches(0.6),
                 color=T.hairline_strong)
    add_text(slide, x1 + Inches(0.30), dec_y + Inches(0.20),
             col_w - Inches(0.6), Inches(0.20),
             "DECISION", font=MONO, size=9, color=T.orange, spacing_em=0.22)
    add_text(slide, x1 + Inches(0.30), dec_y + Inches(0.50),
             col_w - Inches(0.6), Inches(0.6),
             "Stay on core, add middleware, or replace?",
             font=SANS, size=15, bold=True, color=T.text_primary,
             spacing_em=-0.015, line_height=1.3)

    # Layer 2
    x2 = Inches(7.0)
    add_rect(slide, x2, col_y, col_w, col_h,
             fill=T.surface, line=T.hairline)
    add_rect(slide, x2, col_y, Inches(0.025), col_h, fill=T.blue)
    add_text(slide, x2 + Inches(0.30), col_y + Inches(0.30),
             col_w, Inches(0.25),
             "LAYER 2  ·  MONEY MOVEMENT",
             font=MONO, size=9, color=T.blue, spacing_em=0.18)
    items_2 = [
        "ACH origination (single, batch, same-day)",
        "Wires (domestic, international)",
        "Remote Deposit Capture",
        "RTP and FedNow rails",
        "Integrated payables (one file, multi-rail)",
        "Receivables (lockbox, virtual accounts)",
    ]
    paragraphs2 = []
    for it in items_2:
        paragraphs2.append({'text': "—  " + it, 'size': 13,
                            'color': T.text_primary, 'line_height': 1.65,
                            'space_after': 4})
    add_multi_text(slide, x2 + Inches(0.30), col_y + Inches(0.75),
                   col_w - Inches(0.6), Inches(2.8), paragraphs2)
    dec_y = col_y + col_h - Inches(1.2)
    add_hairline(slide, x2 + Inches(0.30), dec_y, col_w - Inches(0.6),
                 color=T.hairline_strong)
    add_text(slide, x2 + Inches(0.30), dec_y + Inches(0.20),
             col_w - Inches(0.6), Inches(0.20),
             "DECISION", font=MONO, size=9, color=T.orange, spacing_em=0.22)
    add_text(slide, x2 + Inches(0.30), dec_y + Inches(0.50),
             col_w - Inches(0.6), Inches(0.6),
             "Build, partner, or pass-through correspondent?",
             font=SANS, size=15, bold=True, color=T.text_primary,
             spacing_em=-0.015, line_height=1.3)

    add_footer(slide,
               "Treasury stack & financial decisions  |  Part 1: Framework")
    add_page_number(slide, num)
    return slide


def slide_layers_3_4_5(prs, num):
    """Slide 9 — Layers 3, 4 & 5."""
    slide = new_slide(prs)
    add_eyebrow(slide, PAD_X, PAD_TOP, "Layers 3, 4 & 5", accent=T.blue)
    add_text(slide, PAD_X, Inches(0.95), Inches(12), Inches(0.7),
             "Where you actually compete (or lose)",
             font=SANS, size=32, bold=True, color=T.text_primary,
             spacing_em=-0.025)
    add_hairline(slide, PAD_X, Inches(1.65), Inches(2.5), color=T.hairline_strong)

    col_w = Inches(3.85)
    col_h = Inches(4.85)
    col_y = Inches(2.0)
    cols = [
        ("LAYER 3  ·  RISK & CONTROLS",
         ["Positive Pay (check + ACH)",
          "Dual control on origination",
          "Real-time fraud scoring",
          "Hardware token / FIDO2 auth",
          "Audit trails for clients"],
         "Reg E does not protect business accounts. Your funds "
         "transfer agreement is your shield."),
        ("LAYER 4  ·  LIQUIDITY & YIELD",
         ["Sweep (money market, repo)",
          "Zero Balance Accounts (ZBA)",
          "Earnings Credit Rate (ECR)",
          "Tiered MMA pricing",
          "IntraFi / ICS for over-limit insurance"],
         "If you want any client over $1M operating cash, you need "
         "an insurance solution."),
        ("LAYER 5  ·  INTEGRATION & EXPERIENCE",
         ["ERP integrations (QB, NetSuite, Sage)",
          "API access (read + initiate)",
          "Single sign-on with client IdP",
          "Multi-user mobile app",
          "Data exports (BAI2, MT940)"],
         "This is where you lose to fintechs. Owners use mobile, "
         "CFOs use desktop. Build both."),
    ]

    for i, (label, items, hard_truth) in enumerate(cols):
        x = PAD_X + i * (col_w + Inches(0.16))
        add_rect(slide, x, col_y, col_w, col_h,
                 fill=T.surface, line=T.hairline)
        # Orange left border on Layer 3 only? No — keep consistent with blue.
        add_rect(slide, x, col_y, Inches(0.025), col_h, fill=T.blue)

        add_text(slide, x + Inches(0.25), col_y + Inches(0.25),
                 col_w - Inches(0.5), Inches(0.30),
                 label, font=MONO, size=8, color=T.blue, spacing_em=0.18,
                 line_height=1.3)

        paragraphs = []
        for it in items:
            paragraphs.append({'text': "—  " + it, 'size': 12,
                               'color': T.text_primary, 'line_height': 1.65,
                               'space_after': 4})
        add_multi_text(slide, x + Inches(0.25), col_y + Inches(0.78),
                       col_w - Inches(0.5), Inches(2.5), paragraphs)

        truth_y = col_y + col_h - Inches(1.7)
        add_hairline(slide, x + Inches(0.25), truth_y,
                     col_w - Inches(0.5), color=T.hairline_strong)
        # Orange accent for "hard truth"
        add_text(slide, x + Inches(0.25), truth_y + Inches(0.18),
                 col_w - Inches(0.5), Inches(0.20),
                 "HARD TRUTH", font=MONO, size=8, color=T.orange,
                 spacing_em=0.22)
        add_text(slide, x + Inches(0.25), truth_y + Inches(0.45),
                 col_w - Inches(0.5), Inches(1.2),
                 hard_truth, font=SANS, size=12, color=T.text_primary,
                 line_height=1.45, italic=False)

    add_footer(slide,
               "Treasury stack & financial decisions  |  Part 1: Framework")
    add_page_number(slide, num)
    return slide


def add_styled_table(slide, x, y, w, h, headers, rows,
                     header_fill=T.surface_hover, body_fill=T.surface,
                     text_color=T.text_primary, header_color=T.blue,
                     border=T.hairline_strong, font_size=10,
                     header_size=9, header_mono=True):
    """Build a styled table with sharp corners and hairline borders."""
    table_shape = slide.shapes.add_table(
        len(rows) + 1, len(headers), x, y, w, h)
    table = table_shape.table

    # Header row
    for ci, htext in enumerate(headers):
        cell = table.cell(0, ci)
        cell.fill.solid()
        cell.fill.fore_color.rgb = header_fill
        tf = cell.text_frame
        tf.margin_left = Pt(8)
        tf.margin_right = Pt(8)
        tf.margin_top = Pt(6)
        tf.margin_bottom = Pt(6)
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = ""
        run = p.add_run()
        run.text = htext.upper() if header_mono else htext
        style_run(run,
                  font=MONO if header_mono else SANS,
                  size=header_size,
                  bold=False,
                  color=header_color,
                  spacing_em=0.18 if header_mono else None)

    # Body rows
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            cell = table.cell(ri + 1, ci)
            cell.fill.solid()
            cell.fill.fore_color.rgb = body_fill
            tf = cell.text_frame
            tf.margin_left = Pt(8)
            tf.margin_right = Pt(8)
            tf.margin_top = Pt(6)
            tf.margin_bottom = Pt(6)
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = ""
            # Allow multi-line cells: split on '\n'
            for li, line in enumerate(str(val).split("\n")):
                if li == 0:
                    target_p = p
                else:
                    target_p = tf.add_paragraph()
                run = target_p.add_run()
                run.text = line
                style_run(run, font=SANS, size=font_size,
                          bold=(ci == 0), color=text_color)
                set_line_spacing(target_p, 1.4)

    # Apply hairline borders to all cells via XML
    for ri in range(len(rows) + 1):
        for ci in range(len(headers)):
            cell = table.cell(ri, ci)
            tcPr = cell._tc.get_or_add_tcPr()
            # Remove existing borders
            for tag in ('a:lnL', 'a:lnR', 'a:lnT', 'a:lnB'):
                for el in tcPr.findall(qn(tag)):
                    tcPr.remove(el)
            for tag in ('a:lnL', 'a:lnR', 'a:lnT', 'a:lnB'):
                ln = etree.SubElement(tcPr, qn(tag))
                ln.set('w', '6350')  # 0.5pt = 6350 EMU
                ln.set('cap', 'flat')
                ln.set('cmpd', 'sng')
                ln.set('algn', 'ctr')
                solidFill = etree.SubElement(ln, qn('a:solidFill'))
                srgb = etree.SubElement(solidFill, qn('a:srgbClr'))
                srgb.set('val',
                         f'{border[0]:02X}{border[1]:02X}{border[2]:02X}')
                prstDash = etree.SubElement(ln, qn('a:prstDash'))
                prstDash.set('val', 'solid')

    return table


def slide_pricing(prs, num):
    """Slide 10 — Pricing logic table."""
    slide = new_slide(prs)
    add_eyebrow(slide, PAD_X, PAD_TOP, "Pricing logic", accent=T.blue)
    add_text(slide, PAD_X, Inches(0.95), Inches(12), Inches(0.5),
             "Pricing models by segment — never one size fits all",
             font=SANS, size=26, bold=True, color=T.text_primary,
             spacing_em=-0.022)
    add_text(slide, PAD_X, Inches(1.50), Inches(12), Inches(0.3),
             "Different buyer, different value, different elasticity. "
             "Your stack must support all four billing models or you "
             "cannot serve all four.",
             font=SANS, size=11, color=T.text_body, line_height=1.4)
    add_text(slide, PAD_X, Inches(1.85), Inches(12), Inches(0.25),
             "SOURCE: [YOUR COMPANY] FIELD EXPERIENCE  ·  2026",
             font=MONO, size=8, color=T.text_dim, spacing_em=0.18)

    headers = ["Segment", "Decision driver", "Pricing model",
               "Yield strategy", "Elasticity"]
    rows = [
        ["Micro\n<$1M revenue",
         "Simplicity, price clarity",
         "Flat-fee bundles, low/no transaction fees",
         "Low rate, simple MMA",
         "High on rate (savings)\nLow on fees"],
        ["SMB\n$1M–$10M",
         "Value, time savings, banker access",
         "Tiered bundles by transaction volume",
         "ECR introduced, MMA tiers",
         "Medium\nHigh on service quality"],
        ["Lower mid\n$10M–$50M",
         "Treasury sophistication, ECR, expertise",
         "Analyzed accounts, per-item, ECR offsets",
         "Aggressive ECR (60–75% of FF), sweep, IntraFi",
         "High on ECR\nHigh on total economics"],
        ["Commercial\n$50M+",
         "Total relationship economics, RFP-driven",
         "Fully negotiated, relationship-priced",
         "ECR vs. money centers, custom sweep, ICS",
         "Very high\nEvery basis point matters"],
    ]
    add_styled_table(slide, PAD_X, Inches(2.20),
                     Inches(11.7), Inches(3.6),
                     headers, rows, font_size=10)

    # Operational implication callout
    cy = Inches(6.10)
    add_rect(slide, PAD_X, cy, Inches(11.7), Inches(0.75),
             fill=T.callout_orange_bg, line=T.orange)
    add_rect(slide, PAD_X, cy, Inches(0.04), Inches(0.75), fill=T.orange)
    add_text(slide, PAD_X + Inches(0.30), cy + Inches(0.10),
             Inches(11), Inches(0.25),
             "OPERATIONAL IMPLICATION", font=MONO, size=9,
             color=T.orange, spacing_em=0.22)
    add_text(slide, PAD_X + Inches(0.30), cy + Inches(0.36),
             Inches(11), Inches(0.4),
             "Bundle billing for micro · Tiered for SMB · Analyzed for "
             "mid-market · Relationship for commercial. If your core "
             "only does one, you cannot serve all four.",
             font=SANS, size=12, bold=False, color=T.text_primary, line_height=1.35)

    add_footer(slide,
               "Treasury stack & financial decisions  |  Part 1: Framework")
    add_page_number(slide, num)
    return slide


def slide_seven_levers(prs, num):
    """Slide 11 — Seven financial levers."""
    slide = new_slide(prs)
    add_eyebrow(slide, PAD_X, PAD_TOP, "Financial levers", accent=T.blue)
    add_text(slide, PAD_X, Inches(0.95), Inches(12), Inches(0.7),
             "Seven levers that decide deposit economics",
             font=SANS, size=32, bold=True, color=T.text_primary,
             spacing_em=-0.025)
    add_hairline(slide, PAD_X, Inches(1.65), Inches(2.5), color=T.hairline_strong)

    levers = [
        ("01", "Deposit pricing",
         "Posted rates, ECR, exception pricing, promo strategy"),
        ("02", "Fee strategy",
         "Maintenance, per-item, treasury services, bundles"),
        ("03", "Cost of acquisition",
         "CAC by channel and segment with payback ceilings"),
        ("04", "Cost to serve",
         "RM time, ops exceptions, branch and digital costs"),
        ("05", "Capital & balance sheet",
         "MBL cap, concentration limits, liquidity contingency"),
        ("06", "Investment pacing",
         "Year-over-year stack and team build sequencing"),
        ("07", "Product P&L",
         "FTP, fee allocation, cross-sell credit, true profitability"),
    ]
    # 4 columns × 2 rows (last cell empty)
    col_w = Inches(2.86)
    row_h = Inches(2.20)
    gap = Inches(0.13)
    y0 = Inches(2.0)

    for i, (idx, title, desc) in enumerate(levers):
        col = i % 4
        row = i // 4
        x = PAD_X + col * (col_w + gap)
        y = y0 + row * (row_h + gap)
        add_rect(slide, x, y, col_w, row_h,
                 fill=T.surface, line=T.hairline)
        # Index numeral
        add_text(slide, x + Inches(0.30), y + Inches(0.20),
                 Inches(1), Inches(0.45),
                 idx, font=MONO, size=11, color=T.blue, spacing_em=0.20)
        # Title
        add_text(slide, x + Inches(0.30), y + Inches(0.65),
                 col_w - Inches(0.6), Inches(0.55),
                 title, font=SANS, size=18, bold=True, color=T.text_primary,
                 spacing_em=-0.020, line_height=1.15)
        # Hairline
        add_hairline(slide, x + Inches(0.30), y + Inches(1.20),
                     Inches(0.6), color=T.hairline_strong)
        # Desc
        add_text(slide, x + Inches(0.30), y + Inches(1.35),
                 col_w - Inches(0.6), Inches(0.85),
                 desc, font=SANS, size=12, color=T.text_body,
                 line_height=1.45)

    add_footer(slide,
               "Treasury stack & financial decisions  |  Part 1: Framework")
    add_page_number(slide, num)
    return slide


def slide_delivery(prs, num):
    """Slide 12 — Buy / partner / build."""
    slide = new_slide(prs)
    add_eyebrow(slide, PAD_X, PAD_TOP, "Delivery model", accent=T.blue)
    add_text(slide, PAD_X, Inches(0.95), Inches(12), Inches(0.5),
             "Buy. Partner. Build. The orchestration question.",
             font=SANS, size=26, bold=True, color=T.text_primary,
             spacing_em=-0.022)
    add_text(slide, PAD_X, Inches(1.50), Inches(12), Inches(0.3),
             "You do not build any of this from scratch. The question is "
             "what you partner for and how you orchestrate.",
             font=SANS, size=11, color=T.text_body, line_height=1.4)
    add_text(slide, PAD_X, Inches(1.85), Inches(12), Inches(0.25),
             "SOURCE: [YOUR COMPANY] FIELD EXPERIENCE  ·  2026",
             font=MONO, size=8, color=T.text_dim, spacing_em=0.18)

    headers = ["Layer", "Recommended approach", "Why"]
    rows = [
        ["1 — Core & account analysis",
         "Middleware partner (Finzly, ZSuite, Treasury Prime)",
         "Faster than core replacement, better than waiting on core vendor"],
        ["2 — Money movement",
         "Partner stack with one orchestrator (payment hub)",
         "Rails are commodity; orchestration is differentiator"],
        ["3 — Risk & controls",
         "Verafin or equivalent + decisioning layer (Zoot)",
         "Verafin strongest in CU/community FI; Zoot for orchestrated decisioning"],
        ["4 — Liquidity & yield",
         "IntraFi for insurance, internal for ECR engine",
         "IntraFi is industry standard; ECR rules are your strategy"],
        ["5 — Integration & experience",
         "Partner-led platform (Q2, Alkami) + ERP via Codat / Rutter",
         "Build experience layer on top, not foundation"],
    ]
    add_styled_table(slide, PAD_X, Inches(2.20),
                     Inches(11.7), Inches(3.6),
                     headers, rows, font_size=11)

    # Order of magnitude callout
    cy = Inches(6.05)
    add_rect(slide, PAD_X, cy, Inches(11.7), Inches(0.85),
             fill=T.callout_blue_bg, line=T.blue)
    add_rect(slide, PAD_X, cy, Inches(0.04), Inches(0.85), fill=T.blue)
    add_text(slide, PAD_X + Inches(0.30), cy + Inches(0.10),
             Inches(11), Inches(0.25),
             "ORDER OF MAGNITUDE", font=MONO, size=9,
             color=T.blue, spacing_em=0.22)
    add_text(slide, PAD_X + Inches(0.30), cy + Inches(0.36),
             Inches(11), Inches(0.5),
             "Year-one investment $3M–$7M  ·  Annual run cost $1.5M–$4M  "
             "·  Pays back in months once volume builds.",
             font=SANS, size=13, bold=False, color=T.text_primary, line_height=1.35)

    add_footer(slide,
               "Treasury stack & financial decisions  |  Part 1: Framework")
    add_page_number(slide, num)
    return slide


def slide_60_day(prs, num):
    """Slide 13 — Six decisions in first 60 days."""
    slide = new_slide(prs)
    add_eyebrow(slide, PAD_X, PAD_TOP, "The 60-day list", accent=T.orange)
    add_text(slide, PAD_X, Inches(0.95), Inches(12), Inches(0.7),
             "Six decisions a leader must make in the first 60 days",
             font=SANS, size=32, bold=True, color=T.text_primary,
             spacing_em=-0.025)
    add_hairline(slide, PAD_X, Inches(1.65), Inches(2.5), color=T.hairline_strong)

    items = [
        ("1", "Stack architecture",
         "Middleware vs. core capability vs. replacement. Foundational."),
        ("2", "FTP methodology",
         "How deposits credit and lending allocates. Required for product P&L."),
        ("3", "MBL cap & LID strategy",
         "Pursue Low-Income Designation? 6–12 month effort, massive unlock."),
        ("4", "Pricing committee",
         "Who approves exception pricing and at what threshold."),
        ("5", "IntraFi participation",
         "90-day decision. Competitive necessity above $1M relationships."),
        ("6", "Fraud & decisioning platform",
         "Drives Layer 3 design and orchestration choices."),
    ]
    # 3 cols × 2 rows
    col_w = Inches(3.83)
    row_h = Inches(2.10)
    gap = Inches(0.16)
    y0 = Inches(2.0)
    for i, (idx, title, desc) in enumerate(items):
        col = i % 3
        row = i // 3
        x = PAD_X + col * (col_w + gap)
        y = y0 + row * (row_h + gap)
        add_rect(slide, x, y, col_w, row_h,
                 fill=T.surface, line=T.hairline)
        # Big number on the left
        add_text(slide, x + Inches(0.30), y + Inches(0.25),
                 Inches(0.8), Inches(1.0),
                 idx, font=SANS, size=42, bold=True, color=T.orange,
                 spacing_em=-0.030, line_height=1.0)
        # Vertical hairline
        add_v_hairline(slide, x + Inches(1.10), y + Inches(0.30),
                       row_h - Inches(0.6), color=T.hairline_strong)
        # Title
        add_text(slide, x + Inches(1.30), y + Inches(0.30),
                 col_w - Inches(1.6), Inches(0.5),
                 title, font=SANS, size=15, bold=True, color=T.text_primary,
                 spacing_em=-0.018, line_height=1.2)
        # Desc
        add_text(slide, x + Inches(1.30), y + Inches(0.85),
                 col_w - Inches(1.6), Inches(1.2),
                 desc, font=SANS, size=11, color=T.text_body,
                 line_height=1.5)

    add_footer(slide,
               "Treasury stack & financial decisions  |  Part 1: Framework")
    add_page_number(slide, num)
    return slide


def slide_institution(prs, num):
    """Slide 15 — The institution."""
    slide = new_slide(prs)
    add_eyebrow(slide, PAD_X, PAD_TOP, "The institution", accent=T.blue)
    add_text(slide, PAD_X, Inches(0.95), Inches(12), Inches(0.7),
             "A top-30 US bank, ~$80B in assets",
             font=SANS, size=32, bold=True, color=T.text_primary,
             spacing_em=-0.025)
    add_text(slide, PAD_X, Inches(1.55), Inches(12), Inches(0.4),
             "Commercial-led franchise · multi-state national reach",
             font=SANS, size=14, color=T.text_body, line_height=1.4)
    add_hairline(slide, PAD_X, Inches(2.05), Inches(11.7),
                 color=T.hairline_strong)

    # Stat bar — 4 cells
    stats = [
        ("~$80B", "in total assets"),
        ("Top 30", "US bank by assets"),
        ("#1", "in C&I loans / assets ($70B+ peers)"),
        ("Multi-state", "national footprint"),
    ]
    sy = Inches(2.30)
    sh = Inches(1.45)
    cell_w = Inches(11.7) / 4
    add_rect(slide, PAD_X, sy, Inches(11.7), sh,
             fill=T.surface, line=T.hairline)
    for i, (num_lbl, sub) in enumerate(stats):
        x = PAD_X + i * cell_w
        if i > 0:
            add_v_hairline(slide, x, sy + Inches(0.20),
                           sh - Inches(0.40), color=T.hairline_strong)
        add_text(slide, x + Inches(0.30), sy + Inches(0.30),
                 cell_w - Inches(0.40), Inches(0.7),
                 num_lbl, font=SANS, size=30, bold=True, color=T.text_primary,
                 spacing_em=-0.025, line_height=1.0)
        add_text(slide, x + Inches(0.30), sy + Inches(1.02),
                 cell_w - Inches(0.40), Inches(0.4),
                 sub, font=MONO, size=9, color=T.text_body, spacing_em=0.18,
                 line_height=1.3)

    # Mandate block
    my = Inches(4.10)
    add_text(slide, PAD_X, my, Inches(12), Inches(0.25),
             "THE MANDATE", font=MONO, size=10, color=T.orange,
             spacing_em=0.22)
    add_text(slide, PAD_X, my + Inches(0.40), Inches(12), Inches(1.2),
             "Lead and build the product organization to win new commercial "
             "customer acquisition through a digital transformation of "
             "treasury management.",
             font=SANS, size=20, bold=True, color=T.text_primary,
             spacing_em=-0.020, line_height=1.3)

    # Goals strip
    gy = Inches(5.70)
    add_hairline(slide, PAD_X, gy, Inches(11.7), color=T.hairline_strong)
    add_text(slide, PAD_X, gy + Inches(0.10), Inches(2), Inches(0.20),
             "GOALS", font=MONO, size=9, color=T.text_tertiary, spacing_em=0.22)
    add_text(slide, PAD_X, gy + Inches(0.40), Inches(11.7), Inches(0.6),
             "Grow business deposits  ·  Deepen multi-product relationships"
             "  ·  Lower cost of funds  ·  Modernize stack to compete with "
             "money centers and fintechs.",
             font=SANS, size=13, color=T.text_body, line_height=1.5)

    add_footer(slide,
               "Treasury stack & financial decisions  |  Part 2: Case study")
    add_page_number(slide, num)
    return slide


def slide_starting_point(prs, num):
    """Slide 16 — Starting point."""
    slide = new_slide(prs)
    add_eyebrow(slide, PAD_X, PAD_TOP, "Starting point", accent=T.blue)
    add_text(slide, PAD_X, Inches(0.95), Inches(12), Inches(0.7),
             "What we inherited — and why we needed a transformation",
             font=SANS, size=28, bold=True, color=T.text_primary,
             spacing_em=-0.022)
    add_hairline(slide, PAD_X, Inches(1.60), Inches(2.5), color=T.hairline_strong)

    col_w = Inches(5.7)
    col_h = Inches(5.0)
    col_y = Inches(1.85)

    # Symptoms
    x1 = PAD_X
    add_rect(slide, x1, col_y, col_w, col_h,
             fill=T.surface, line=T.hairline)
    add_rect(slide, x1, col_y, Inches(0.025), col_h, fill=T.orange)
    add_text(slide, x1 + Inches(0.30), col_y + Inches(0.30),
             col_w, Inches(0.25),
             "SYMPTOMS WE SAW", font=MONO, size=10, color=T.orange,
             spacing_em=0.22)
    symptoms = [
        "Win rates against money-center banks were declining on RFPs over $5M",
        "Deposit cost was creeping up, pricing concessions were ad hoc",
        "Treasury onboarding took 60+ days; clients churned mid-implementation",
        "RMs sold what they knew; treasury attach was inconsistent",
        "Mobile and self-service experience trailed even regional competitors",
        "Fee leakage on analyzed accounts was material and unmeasured",
    ]
    paragraphs = []
    for it in symptoms:
        paragraphs.append({'text': "—  " + it, 'size': 12,
                           'color': T.text_primary, 'line_height': 1.55,
                           'space_after': 8})
    add_multi_text(slide, x1 + Inches(0.30), col_y + Inches(0.75),
                   col_w - Inches(0.6), col_h - Inches(1.0), paragraphs)

    # Root causes
    x2 = Inches(7.0)
    add_rect(slide, x2, col_y, col_w, col_h,
             fill=T.surface, line=T.hairline)
    add_rect(slide, x2, col_y, Inches(0.025), col_h, fill=T.blue)
    add_text(slide, x2 + Inches(0.30), col_y + Inches(0.30),
             col_w, Inches(0.25),
             "ROOT CAUSES UNDERNEATH", font=MONO, size=10, color=T.blue,
             spacing_em=0.22)
    causes = [
        "Stack was a patchwork of legacy core + bolt-ons; no orchestration layer",
        "Customer-facing product team existed but did not own the end-to-end process",
        "Pricing lived in spreadsheets across the RM line; no committee, no governance",
        "FTP credited deposits to the line of business that opened them, not the one that retained them",
        "Onboarding and entitlements were paper-and-fax for many TM products",
        "No product P&L existed for treasury management as a business",
    ]
    paragraphs2 = []
    for it in causes:
        paragraphs2.append({'text': "—  " + it, 'size': 12,
                            'color': T.text_primary, 'line_height': 1.55,
                            'space_after': 8})
    add_multi_text(slide, x2 + Inches(0.30), col_y + Inches(0.75),
                   col_w - Inches(0.6), col_h - Inches(1.0), paragraphs2)

    add_footer(slide,
               "Treasury stack & financial decisions  |  Part 2: Case study")
    add_page_number(slide, num)
    return slide


def slide_strategy(prs, num):
    """Slide 17 — Three big moves."""
    slide = new_slide(prs)
    add_eyebrow(slide, PAD_X, PAD_TOP, "Strategy", accent=T.blue)
    add_text(slide, PAD_X, Inches(0.95), Inches(12), Inches(0.7),
             "Three big moves that anchored the transformation",
             font=SANS, size=32, bold=True, color=T.text_primary,
             spacing_em=-0.025)
    add_hairline(slide, PAD_X, Inches(1.65), Inches(2.5), color=T.hairline_strong)

    moves = [
        ("01", "Rebuild the product organization end-to-end",
         "A treasury product team already existed, but it was customer-"
         "facing and did not own the full process. We rebuilt it to own "
         "the entire workflow — from acquisition through onboarding "
         "through deepening — with a real GM, P&L, and pods."),
        ("02", "Re-architect the stack with an orchestration layer",
         "Insert middleware between legacy core and the client experience "
         "so we could ship faster, decouple from core release cycles, and "
         "modernize layer by layer."),
        ("03", "Re-engineer the deposit economics",
         "Build a true product P&L, fix FTP, install a pricing committee, "
         "monetize fee income left on the table, and tie RM compensation "
         "to the right deposit."),
    ]
    col_w = Inches(3.83)
    col_h = Inches(4.85)
    gap = Inches(0.16)
    y0 = Inches(2.0)
    for i, (idx, title, desc) in enumerate(moves):
        x = PAD_X + i * (col_w + gap)
        add_rect(slide, x, y0, col_w, col_h,
                 fill=T.surface, line=T.hairline)
        add_text(slide, x + Inches(0.30), y0 + Inches(0.30),
                 Inches(1), Inches(0.30),
                 idx, font=MONO, size=11, color=T.blue, spacing_em=0.20)
        add_text(slide, x + Inches(0.30), y0 + Inches(0.75),
                 col_w - Inches(0.6), Inches(1.4),
                 title, font=SANS, size=18, bold=True, color=T.text_primary,
                 spacing_em=-0.020, line_height=1.2)
        add_hairline(slide, x + Inches(0.30), y0 + Inches(2.20),
                     Inches(0.9), color=T.hairline_strong)
        add_text(slide, x + Inches(0.30), y0 + Inches(2.40),
                 col_w - Inches(0.6), Inches(2.3),
                 desc, font=SANS, size=12, color=T.text_body,
                 line_height=1.65)

    add_footer(slide,
               "Treasury stack & financial decisions  |  Part 2: Case study")
    add_page_number(slide, num)
    return slide


def slide_operating_model(prs, num):
    """Slide 18 — Operating model."""
    slide = new_slide(prs)
    add_eyebrow(slide, PAD_X, PAD_TOP, "Operating model", accent=T.blue)
    add_text(slide, PAD_X, Inches(0.95), Inches(12), Inches(0.7),
             "The product organization we built",
             font=SANS, size=32, bold=True, color=T.text_primary,
             spacing_em=-0.025)
    add_hairline(slide, PAD_X, Inches(1.65), Inches(2.5), color=T.hairline_strong)

    # GM box at top — full width
    gy = Inches(2.0)
    gh = Inches(0.95)
    add_rect(slide, PAD_X, gy, Inches(11.7), gh,
             fill=T.surface, line=T.hairline)
    add_rect(slide, PAD_X, gy, Inches(0.04), gh, fill=T.orange)
    add_text(slide, PAD_X + Inches(0.30), gy + Inches(0.18),
             Inches(11), Inches(0.30),
             "GM, TREASURY MANAGEMENT PRODUCTS",
             font=MONO, size=10, color=T.orange, spacing_em=0.22)
    add_text(slide, PAD_X + Inches(0.30), gy + Inches(0.50),
             Inches(11), Inches(0.4),
             "Owns P&L · Reports to CRO",
             font=SANS, size=15, bold=True, color=T.text_primary,
             spacing_em=-0.015)

    # Connector — 3 vertical hairlines
    cy = gy + gh
    add_v_hairline(slide, Inches(2.78), cy, Inches(0.30),
                   color=T.hairline_strong)
    add_v_hairline(slide, Inches(6.66), cy, Inches(0.30),
                   color=T.hairline_strong)
    add_v_hairline(slide, Inches(10.55), cy, Inches(0.30),
                   color=T.hairline_strong)
    add_hairline(slide, Inches(2.78), cy + Inches(0.30),
                 Inches(7.77), color=T.hairline_strong)

    # Three pods
    pods = [
        ("Acquire pod", "Owns getting new business clients",
         "Net new operating accounts · CAC · Time to first dollar"),
        ("Onboard & activate pod", "Owns the first 90 days",
         "90-day attach rate · Account funded % · Time to active"),
        ("Treasury & deepen pod", "Owns existing book and TM services",
         "Deposit growth per relationship · TM fee income · Churn"),
    ]
    pod_w = Inches(3.83)
    pod_h = Inches(2.30)
    py = Inches(3.50)
    gap = Inches(0.16)
    for i, (title, sub, metric) in enumerate(pods):
        x = PAD_X + i * (pod_w + gap)
        add_rect(slide, x, py, pod_w, pod_h,
                 fill=T.surface, line=T.hairline)
        add_rect(slide, x, py, Inches(0.025), pod_h, fill=T.blue)
        add_text(slide, x + Inches(0.30), py + Inches(0.25),
                 pod_w - Inches(0.6), Inches(0.45),
                 title, font=SANS, size=18, bold=True, color=T.text_primary,
                 spacing_em=-0.020)
        add_text(slide, x + Inches(0.30), py + Inches(0.72),
                 pod_w - Inches(0.6), Inches(0.4),
                 sub, font=SANS, size=12, color=T.text_body,
                 line_height=1.4)
        add_hairline(slide, x + Inches(0.30), py + Inches(1.20),
                     Inches(0.9), color=T.hairline_strong)
        add_text(slide, x + Inches(0.30), py + Inches(1.36),
                 pod_w - Inches(0.6), Inches(0.25),
                 "METRIC", font=MONO, size=8, color=T.blue, spacing_em=0.22)
        add_text(slide, x + Inches(0.30), py + Inches(1.62),
                 pod_w - Inches(0.6), Inches(0.6),
                 metric, font=SANS, size=11, color=T.text_primary, line_height=1.45)

    # Shared services strip
    sy = Inches(6.05)
    sh = Inches(0.95)
    add_rect(slide, PAD_X, sy, Inches(11.7), sh,
             fill=T.callout_blue_bg, line=T.hairline)
    add_text(slide, PAD_X + Inches(0.30), sy + Inches(0.18),
             Inches(11), Inches(0.25),
             "SHARED SERVICES ACROSS PODS",
             font=MONO, size=9, color=T.blue, spacing_em=0.22)
    add_text(slide, PAD_X + Inches(0.30), sy + Inches(0.50),
             Inches(11), Inches(0.4),
             "Platform engineering · Risk & compliance · Data & analytics"
             " · Design system · Vendor management",
             font=SANS, size=12, color=T.text_body, line_height=1.4)

    add_footer(slide,
               "Treasury stack & financial decisions  |  Part 2: Case study")
    add_page_number(slide, num)
    return slide


def slide_stack_decisions(prs, num):
    """Slide 19 — Stack decisions table."""
    slide = new_slide(prs)
    add_eyebrow(slide, PAD_X, PAD_TOP, "Stack decisions", accent=T.blue)
    add_text(slide, PAD_X, Inches(0.95), Inches(12), Inches(0.5),
             "How we re-architected the stack, layer by layer",
             font=SANS, size=26, bold=True, color=T.text_primary,
             spacing_em=-0.022)
    add_text(slide, PAD_X, Inches(1.55), Inches(12), Inches(0.25),
             "SOURCE: [YOUR COMPANY] FIELD EXPERIENCE  ·  2026",
             font=MONO, size=8, color=T.text_dim, spacing_em=0.18)

    headers = ["Layer", "Decision", "Trade-off accepted"]
    rows = [
        ["1 — Core",
         "Kept legacy core, inserted orchestration middleware for account "
         "analysis and product config",
         "Avoided multi-year core replacement; took on integration debt"],
        ["2 — Money movement",
         "Built a payment hub abstraction; standardized ACH, wires, RTP, "
         "and integrated payables behind one API",
         "Higher upfront engineering cost; faster product velocity for "
         "years after"],
        ["3 — Risk & controls",
         "Real-time fraud platform + decisioning service for onboarding, "
         "payments, and credit",
         "Material spend; paid back in fraud loss avoidance and faster "
         "onboarding"],
        ["4 — Liquidity & yield",
         "New ECR engine, sweep options, and over-limit insurance via network",
         "ECR exposure managed through tighter governance; net lift to "
         "acquisition"],
        ["5 — Experience",
         "Net-new commercial digital experience: web, mobile, ERP "
         "integrations, APIs",
         "Phased delivery created customer experience friction; should "
         "have been one integrated stack from day one"],
    ]
    add_styled_table(slide, PAD_X, Inches(1.95),
                     Inches(11.7), Inches(4.0),
                     headers, rows, font_size=10)

    # Decisive call callout
    cy = Inches(6.10)
    add_rect(slide, PAD_X, cy, Inches(11.7), Inches(0.85),
             fill=T.callout_orange_bg, line=T.orange)
    add_rect(slide, PAD_X, cy, Inches(0.04), Inches(0.85), fill=T.orange)
    add_text(slide, PAD_X + Inches(0.30), cy + Inches(0.10),
             Inches(11), Inches(0.25),
             "THE DECISIVE CALL", font=MONO, size=9, color=T.orange,
             spacing_em=0.22)
    add_text(slide, PAD_X + Inches(0.30), cy + Inches(0.36),
             Inches(11), Inches(0.5),
             "We did not replace the core. We orchestrated around it. "
             "That decision saved 24+ months and unlocked everything "
             "that followed.",
             font=SANS, size=13, bold=False, color=T.text_primary, line_height=1.35)

    add_footer(slide,
               "Treasury stack & financial decisions  |  Part 2: Case study")
    add_page_number(slide, num)
    return slide


def slide_financial_decisions(prs, num):
    """Slide 20 — Financial decisions: 4 quadrants."""
    slide = new_slide(prs)
    add_eyebrow(slide, PAD_X, PAD_TOP, "Financial decisions", accent=T.blue)
    add_text(slide, PAD_X, Inches(0.95), Inches(12), Inches(0.7),
             "Pricing, fees, and the levers we pulled",
             font=SANS, size=28, bold=True, color=T.text_primary,
             spacing_em=-0.022)
    add_hairline(slide, PAD_X, Inches(1.60), Inches(2.5), color=T.hairline_strong)

    quads = [
        ("Pricing & ECR governance",
         ["Stood up a Pricing Committee with thresholds, SLAs, and approvals",
          "Codified ECR strategy by segment (60–75% of FF for mid-market)",
          "Promo rates for new money tied to 90-day attach commitments",
          "Killed RM-level rate exceptions below relationship threshold"]),
        ("Fee strategy & leakage",
         ["Audited analyzed accounts; reclaimed material annual fee income",
          "Bundled TM services with operating account tiers",
          "Repriced wires, RDC, and ACH origination to match market",
          "Made fee waivers a relationship lever, not an RM giveaway"]),
        ("FTP & cross-sell credit",
         ["Rewrote FTP so deposits credited the team that retained them",
          "Built attribution for treasury attach across pods",
          "Tied RM and product comp to operating DDA, not any deposit",
          "Made sweep, ECR, and fee income visible at relationship level"]),
        ("Product P&L & investment",
         ["Built a real treasury product P&L; visible to exec team monthly",
          "Set CAC ceilings by channel; killed channels above threshold",
          "Phased investment: rails year 1, ECR year 2, ERP/API year 3",
          "Tied roadmap funding to outcomes, not to project charters"]),
    ]
    qw = Inches(5.78)
    qh = Inches(2.45)
    gap = Inches(0.14)
    y0 = Inches(1.85)
    for i, (title, items) in enumerate(quads):
        col = i % 2
        row = i // 2
        x = PAD_X + col * (qw + gap)
        y = y0 + row * (qh + gap)
        add_rect(slide, x, y, qw, qh, fill=T.surface, line=T.hairline)
        add_rect(slide, x, y, Inches(0.025), qh, fill=T.blue)
        add_text(slide, x + Inches(0.30), y + Inches(0.20),
                 qw - Inches(0.6), Inches(0.45),
                 title, font=SANS, size=16, bold=True, color=T.text_primary,
                 spacing_em=-0.018)
        add_hairline(slide, x + Inches(0.30), y + Inches(0.65),
                     Inches(0.7), color=T.hairline_strong)
        paragraphs = []
        for it in items:
            paragraphs.append({'text': "—  " + it, 'size': 11,
                               'color': T.text_body, 'line_height': 1.45,
                               'space_after': 4})
        add_multi_text(slide, x + Inches(0.30), y + Inches(0.80),
                       qw - Inches(0.6), qh - Inches(0.95), paragraphs)

    add_footer(slide,
               "Treasury stack & financial decisions  |  Part 2: Case study")
    add_page_number(slide, num)
    return slide


def slide_change_mgmt(prs, num):
    """Slide 21 — Change management: kill / teach."""
    slide = new_slide(prs)
    add_eyebrow(slide, PAD_X, PAD_TOP, "Change management", accent=T.blue)
    add_text(slide, PAD_X, Inches(0.95), Inches(12), Inches(0.7),
             "What we had to kill — and what we had to teach",
             font=SANS, size=28, bold=True, color=T.text_primary,
             spacing_em=-0.022)
    add_hairline(slide, PAD_X, Inches(1.60), Inches(2.5), color=T.hairline_strong)

    col_w = Inches(5.7)
    col_h = Inches(5.0)
    col_y = Inches(1.85)

    # Killed
    x1 = PAD_X
    add_rect(slide, x1, col_y, col_w, col_h,
             fill=T.surface, line=T.hairline)
    add_rect(slide, x1, col_y, Inches(0.025), col_h, fill=T.orange)
    add_text(slide, x1 + Inches(0.30), col_y + Inches(0.30),
             col_w, Inches(0.25),
             "WHAT WE KILLED", font=MONO, size=10, color=T.orange,
             spacing_em=0.22)
    killed = [
        "Project portfolio reviews for product work",
        "Annual roadmap commitments below the outcome level",
        "IT-as-vendor mental model",
        "Committee approvals for sub-threshold product decisions",
        "RM-level pricing exceptions without governance",
        "FTP rules that punished retention teams",
        "Compliance bolted on at end of build, not embedded in pods",
    ]
    paragraphs = []
    for it in killed:
        paragraphs.append({'text': "✕  " + it, 'size': 12,
                           'color': T.text_primary, 'line_height': 1.55,
                           'space_after': 6})
    add_multi_text(slide, x1 + Inches(0.30), col_y + Inches(0.75),
                   col_w - Inches(0.6), col_h - Inches(1.0), paragraphs)

    # Taught
    x2 = Inches(7.0)
    add_rect(slide, x2, col_y, col_w, col_h,
             fill=T.surface, line=T.hairline)
    add_rect(slide, x2, col_y, Inches(0.025), col_h, fill=T.blue)
    add_text(slide, x2 + Inches(0.30), col_y + Inches(0.30),
             col_w, Inches(0.25),
             "WHAT WE TAUGHT", font=MONO, size=10, color=T.blue,
             spacing_em=0.22)
    taught = [
        "Outcome-based planning, quarterly cycles, funded teams",
        "Product manager as P&L owner, not project coordinator",
        "RM and TSC partnership model on enterprise deals",
        "Pricing committee discipline and exception governance",
        "Reading an analyzed account statement like a treasurer would",
        "Speaking the client's ERP and treasury workstation language",
        "Risk and product working as one team, not opposing teams",
    ]
    paragraphs2 = []
    for it in taught:
        paragraphs2.append({'text': "✓  " + it, 'size': 12,
                            'color': T.text_primary, 'line_height': 1.55,
                            'space_after': 6})
    add_multi_text(slide, x2 + Inches(0.30), col_y + Inches(0.75),
                   col_w - Inches(0.6), col_h - Inches(1.0), paragraphs2)

    add_footer(slide,
               "Treasury stack & financial decisions  |  Part 2: Case study")
    add_page_number(slide, num)
    return slide


def slide_outcomes(prs, num):
    """Slide 22 — Outcomes."""
    slide = new_slide(prs)
    add_eyebrow(slide, PAD_X, PAD_TOP, "Outcomes", accent=T.blue)
    add_text(slide, PAD_X, Inches(0.95), Inches(12), Inches(0.7),
             "Two years of work — most of the impact landed in Year 1",
             font=SANS, size=28, bold=True, color=T.text_primary,
             spacing_em=-0.022)
    add_text(slide, PAD_X, Inches(1.60), Inches(12), Inches(0.3),
             "Indexed indicators — directional and anonymized; exact "
             "figures held back per confidentiality.",
             font=MONO, size=9, color=T.text_tertiary, spacing_em=0.12)
    add_hairline(slide, PAD_X, Inches(1.95), Inches(11.7),
                 color=T.hairline_strong)

    # SVB moment hero
    sy = Inches(2.20)
    sh = Inches(2.20)
    add_rect(slide, PAD_X, sy, Inches(11.7), sh,
             fill=T.surface, line=T.hairline)
    add_rect(slide, PAD_X, sy, Inches(0.04), sh, fill=T.orange)
    add_text(slide, PAD_X + Inches(0.40), sy + Inches(0.30),
             Inches(11), Inches(0.30),
             "THE SVB MOMENT", font=MONO, size=11, color=T.orange,
             spacing_em=0.22)
    add_text(slide, PAD_X + Inches(0.40), sy + Inches(0.75),
             Inches(11.5), Inches(1.0),
             "60+ days  →  24 hours",
             font=SANS, size=54, bold=True, color=T.text_primary,
             spacing_em=-0.030, line_height=1.0)
    add_text(slide, PAD_X + Inches(0.40), sy + Inches(1.65),
             Inches(11), Inches(0.5),
             "Account opening compressed from 60+ days to 24 hours. When "
             "the SVB crisis hit, we acquired a substantial book of "
             "stranded SVB clients in days — not months.",
             font=SANS, size=13, color=T.text_body, line_height=1.45)

    # Below: Year 1 / Year 2 columns
    py = Inches(4.65)
    ph = Inches(2.10)
    col_w = Inches(5.78)
    gap = Inches(0.14)
    cards = [
        ("YEAR 1 CARRIED THE LIFT",
         "Onboarding speed and digital experience changed the "
         "acquisition curve."),
        ("YEAR 2 COMPOUNDED",
         "Fee income, cost of funds, and operating DDA share kept "
         "improving as the model matured."),
    ]
    for i, (label, body) in enumerate(cards):
        x = PAD_X + i * (col_w + gap)
        add_rect(slide, x, py, col_w, ph, fill=T.surface, line=T.hairline)
        add_rect(slide, x, py, Inches(0.025), ph, fill=T.blue)
        add_text(slide, x + Inches(0.30), py + Inches(0.25),
                 col_w - Inches(0.6), Inches(0.30),
                 label, font=MONO, size=10, color=T.blue, spacing_em=0.22)
        add_text(slide, x + Inches(0.30), py + Inches(0.65),
                 col_w - Inches(0.6), Inches(1.4),
                 body, font=SANS, size=15, color=T.text_primary,
                 line_height=1.5)

    add_footer(slide,
               "Treasury stack & financial decisions  |  Part 2: Case study")
    add_page_number(slide, num)
    return slide


def slide_svb_moment(prs, num):
    """Slide 23 — SVB proof point."""
    slide = new_slide(prs)
    add_eyebrow(slide, PAD_X, PAD_TOP, "Proof point", accent=T.orange)
    add_text(slide, PAD_X, Inches(0.95), Inches(12), Inches(0.7),
             "The SVB moment — when speed became a weapon",
             font=SANS, size=30, bold=True, color=T.text_primary,
             spacing_em=-0.025)
    add_hairline(slide, PAD_X, Inches(1.65), Inches(2.5), color=T.hairline_strong)

    # Hero: BEFORE → AFTER
    hy = Inches(1.95)
    hh = Inches(1.55)
    add_rect(slide, PAD_X, hy, Inches(11.7), hh, fill=T.surface,
             line=T.hairline)
    third = Inches(11.7) / 3
    # Before
    add_text(slide, PAD_X + Inches(0.30), hy + Inches(0.20),
             third - Inches(0.40), Inches(0.25),
             "BEFORE", font=MONO, size=10, color=T.text_tertiary,
             spacing_em=0.22)
    add_text(slide, PAD_X + Inches(0.30), hy + Inches(0.50),
             third - Inches(0.40), Inches(0.7),
             "60+ days",
             font=SANS, size=46, bold=True, color=T.text_primary,
             spacing_em=-0.030, line_height=1.0)
    add_text(slide, PAD_X + Inches(0.30), hy + Inches(1.15),
             third - Inches(0.40), Inches(0.30),
             "commercial account opening",
             font=SANS, size=11, color=T.text_body, line_height=1.3)
    # Arrow
    add_text(slide, PAD_X + third, hy + Inches(0.60),
             third, Inches(0.7),
             "→", font=SANS, size=44, bold=False, color=T.orange,
             align=PP_ALIGN.CENTER, line_height=1.0)
    # After
    ax = PAD_X + 2 * third
    add_text(slide, ax + Inches(0.30), hy + Inches(0.20),
             third - Inches(0.40), Inches(0.25),
             "AFTER", font=MONO, size=10, color=T.orange, spacing_em=0.22)
    add_text(slide, ax + Inches(0.30), hy + Inches(0.50),
             third - Inches(0.40), Inches(0.7),
             "24 hours",
             font=SANS, size=46, bold=True, color=T.orange,
             spacing_em=-0.030, line_height=1.0)
    add_text(slide, ax + Inches(0.30), hy + Inches(1.15),
             third - Inches(0.40), Inches(0.30),
             "commercial account opening",
             font=SANS, size=11, color=T.text_body, line_height=1.3)

    # Three columns: crisis / advantage / result
    cy = Inches(3.75)
    ch = Inches(2.65)
    col_w = Inches(3.83)
    gap = Inches(0.16)
    cards = [
        ("THE CRISIS",
         "March 2023. Silicon Valley Bank collapsed in 48 hours. Tens "
         "of thousands of commercial clients suddenly needed a new home "
         "for operating cash — fast. Most banks could not move at the "
         "speed the moment demanded."),
        ("THE ADVANTAGE",
         "We had spent 18 months rebuilding onboarding from a 60+ day "
         "paper-and-fax process to a 24-hour digital flow. When the "
         "call came, we were ready. Account opening, entitlements, "
         "treasury setup, and first wires — same day."),
        ("THE RESULT",
         "Acquired a substantial book of stranded SVB clients in days, "
         "not months. Operating accounts. Treasury attach in week one. "
         "The deposits that came in during that window are still on "
         "the balance sheet today."),
    ]
    for i, (label, body) in enumerate(cards):
        x = PAD_X + i * (col_w + gap)
        add_rect(slide, x, cy, col_w, ch, fill=T.surface, line=T.hairline)
        add_rect(slide, x, cy, Inches(0.025), ch, fill=T.blue)
        add_text(slide, x + Inches(0.30), cy + Inches(0.25),
                 col_w - Inches(0.6), Inches(0.30),
                 label, font=MONO, size=10, color=T.blue, spacing_em=0.22)
        add_hairline(slide, x + Inches(0.30), cy + Inches(0.65),
                     Inches(0.6), color=T.hairline_strong)
        add_text(slide, x + Inches(0.30), cy + Inches(0.80),
                 col_w - Inches(0.6), ch - Inches(0.95),
                 body, font=SANS, size=12, color=T.text_primary, line_height=1.55)

    # Lesson callout
    ly = Inches(6.55)
    add_rect(slide, PAD_X, ly, Inches(11.7), Inches(0.50),
             fill=T.callout_orange_bg, line=T.orange)
    add_rect(slide, PAD_X, ly, Inches(0.04), Inches(0.50), fill=T.orange)
    add_text(slide, PAD_X + Inches(0.30), ly + Inches(0.13),
             Inches(11), Inches(0.30),
             "THE LESSON: Onboarding speed is not an operations metric. "
             "It is a deposit acquisition weapon — the kind that only "
             "matters when you need it most.",
             font=SANS, size=12, bold=True, color=T.text_primary, line_height=1.3)

    add_footer(slide,
               "Treasury stack & financial decisions  |  Part 2: Case study")
    add_page_number(slide, num)
    return slide


def slide_what_hurt(prs, num):
    """Slide 24 — What hurt."""
    slide = new_slide(prs)
    add_eyebrow(slide, PAD_X, PAD_TOP, "What hurt", accent=T.orange)
    add_text(slide, PAD_X, Inches(0.95), Inches(12), Inches(0.7),
             "The painful parts — where I would push harder next time",
             font=SANS, size=28, bold=True, color=T.text_primary,
             spacing_em=-0.022)
    add_hairline(slide, PAD_X, Inches(1.60), Inches(2.5), color=T.hairline_strong)

    items = [
        ("Org politics around the GM seat",
         "The product GM role challenged the RM line's identity. "
         "Underestimated how long it took the field to trust the model. "
         "Push harder: clear executive sponsorship and joint scorecards "
         "from week one."),
        ("Talent gap was bigger than budgeted",
         "Real product managers and treasury-fluent designers were rare "
         "and expensive. Hiring took 9–12 months longer than plan. Push "
         "harder: contractor-led pods to bridge while permanent hires "
         "came in."),
        ("Stack design was piecemeal, not whole",
         "We broke the stack into separate workstreams and layered "
         "partners over time. The customer experience suffered for it. "
         "Push harder: design the entire stack with the right partners "
         "up front and stand it up as one system, not five."),
        ("Risk and compliance integration",
         "Embedding compliance in pods worked, but it took multiple "
         "cycles and one painful audit finding to get the model right. "
         "Push harder: co-design the operating model with the second "
         "line on day one."),
        ("Pricing committee adoption",
         "RMs found ways around the committee for months. Behavior "
         "changed only after comp plans changed. Push harder: change "
         "the comp plan first, then install governance — not the other "
         "way around."),
        ("Outcome metrics took 6 months to settle",
         "Early metrics rewarded activity, not outcomes. Re-baselined "
         "twice. Push harder: invest in data and analytics inside the "
         "product org from day zero, not month nine."),
    ]
    col_w = Inches(3.83)
    row_h = Inches(2.45)
    gap = Inches(0.16)
    y0 = Inches(1.85)
    for i, (title, body) in enumerate(items):
        col = i % 3
        row = i // 3
        x = PAD_X + col * (col_w + gap)
        y = y0 + row * (row_h + gap)
        add_rect(slide, x, y, col_w, row_h, fill=T.surface, line=T.hairline)
        add_rect(slide, x, y, Inches(0.025), row_h, fill=T.orange)
        add_text(slide, x + Inches(0.25), y + Inches(0.25),
                 col_w - Inches(0.5), Inches(0.65),
                 title, font=SANS, size=14, bold=True, color=T.text_primary,
                 spacing_em=-0.018, line_height=1.2)
        add_hairline(slide, x + Inches(0.25), y + Inches(0.85),
                     Inches(0.6), color=T.hairline_strong)
        add_text(slide, x + Inches(0.25), y + Inches(0.98),
                 col_w - Inches(0.5), row_h - Inches(1.1),
                 body, font=SANS, size=10, color=T.text_body,
                 line_height=1.55)

    add_footer(slide,
               "Treasury stack & financial decisions  |  Part 2: Case study")
    add_page_number(slide, num)
    return slide


def slide_translation(prs, num):
    """Slide 25 — Translation table."""
    slide = new_slide(prs)
    add_eyebrow(slide, PAD_X, PAD_TOP, "Translation", accent=T.blue)
    add_text(slide, PAD_X, Inches(0.95), Inches(12), Inches(0.5),
             "What translates from a top-30 bank to a CU or mid-size FI",
             font=SANS, size=26, bold=True, color=T.text_primary,
             spacing_em=-0.022)
    add_text(slide, PAD_X, Inches(1.55), Inches(12), Inches(0.25),
             "SOURCE: [YOUR COMPANY] FIELD EXPERIENCE  ·  2026",
             font=MONO, size=8, color=T.text_dim, spacing_em=0.18)

    headers = ["Element", "At a top-30 bank",
               "Translation for a CU / mid-size FI"]
    rows = [
        ["Product GM",
         "Full P&L, dedicated roadmap, full pod structure",
         "Single GM with a small team; same authority, simpler structure"],
        ["Stack approach",
         "Built orchestration middleware in-house",
         "Buy middleware (Finzly, ZSuite, Treasury Prime); skip the build"],
        ["Decisioning layer",
         "Custom decisioning across onboarding, payments, credit",
         "Partner with Zoot or equivalent; same orchestration, faster"],
        ["Pricing committee",
         "Multi-tier with regional review",
         "Single committee with clear thresholds; same discipline"],
        ["FTP & comp",
         "Rebuilt across multiple LOBs",
         "Simpler scope; same principle — pay for the right deposit"],
        ["Differentiation",
         "Scale, brand, balance sheet",
         "Member-owned story, lower cost base, vertical focus, "
         "service depth"],
    ]
    add_styled_table(slide, PAD_X, Inches(1.95),
                     Inches(11.7), Inches(4.0),
                     headers, rows, font_size=10)

    # Point callout
    cy = Inches(6.10)
    add_rect(slide, PAD_X, cy, Inches(11.7), Inches(0.85),
             fill=T.callout_blue_bg, line=T.blue)
    add_rect(slide, PAD_X, cy, Inches(0.04), Inches(0.85), fill=T.blue)
    add_text(slide, PAD_X + Inches(0.30), cy + Inches(0.10),
             Inches(11), Inches(0.25),
             "THE POINT", font=MONO, size=9, color=T.blue, spacing_em=0.22)
    add_text(slide, PAD_X + Inches(0.30), cy + Inches(0.36),
             Inches(11), Inches(0.5),
             "Same discipline, smaller scope, partner-heavy execution. "
             "The model works at every scale — what changes is how you "
             "assemble it.",
             font=SANS, size=13, bold=False, color=T.text_primary, line_height=1.35)

    add_footer(slide,
               "Treasury stack & financial decisions  |  Part 2: Case study")
    add_page_number(slide, num)
    return slide


def slide_lessons(prs, num):
    """Slide 26 — Ten lessons."""
    slide = new_slide(prs)
    add_eyebrow(slide, PAD_X, PAD_TOP, "Lessons", accent=T.blue)
    add_text(slide, PAD_X, Inches(0.95), Inches(12), Inches(0.7),
             "Ten lessons that travel to any FI building this",
             font=SANS, size=32, bold=True, color=T.text_primary,
             spacing_em=-0.025)
    add_hairline(slide, PAD_X, Inches(1.65), Inches(2.5), color=T.hairline_strong)

    lessons = [
        ("01", "Hire the GM before anything else."),
        ("02", "Orchestrate around the core; do not replace it on day one."),
        ("03", "Build a real product P&L or none of this is measurable."),
        ("04", "Fix FTP early or you will pay people for the wrong behavior."),
        ("05", "Pricing committee + comp redesign together, not separately."),
        ("06", "Embed risk and compliance in pods; do not bolt them on."),
        ("07", "Onboarding speed is a deposit acquisition lever — invest in it."),
        ("08", "Fee leakage is real money; audit analyzed accounts before scaling."),
        ("09", "Mobile is an enterprise feature now, not a consumer afterthought."),
        ("10", "Outcomes over outputs; fund teams, not project charters."),
    ]
    # 2 columns × 5 rows
    col_w = Inches(5.78)
    row_h = Inches(0.92)
    gap_x = Inches(0.14)
    gap_y = Inches(0.12)
    y0 = Inches(2.0)
    for i, (idx, text) in enumerate(lessons):
        col = i % 2
        row = i // 2
        x = PAD_X + col * (col_w + gap_x)
        y = y0 + row * (row_h + gap_y)
        add_rect(slide, x, y, col_w, row_h, fill=T.surface, line=T.hairline)
        add_text(slide, x + Inches(0.25), y + Inches(0.18),
                 Inches(0.7), Inches(0.55),
                 idx, font=MONO, size=14, color=T.blue, spacing_em=0.22)
        add_v_hairline(slide, x + Inches(0.95), y + Inches(0.18),
                       row_h - Inches(0.36), color=T.hairline_strong)
        add_text(slide, x + Inches(1.10), y + Inches(0.20),
                 col_w - Inches(1.35), row_h - Inches(0.40),
                 text, font=SANS, size=13, bold=True, color=T.text_primary,
                 spacing_em=-0.015, line_height=1.35,
                 anchor=MSO_ANCHOR.MIDDLE)

    add_footer(slide,
               "Treasury stack & financial decisions  |  Part 2: Case study")
    add_page_number(slide, num)
    return slide


def slide_new_lesson(prs, num):
    """Slide 27 — AI overlay (six moves)."""
    slide = new_slide(prs)
    add_eyebrow(slide, PAD_X, PAD_TOP, "The new lesson", accent=T.orange)
    add_text(slide, PAD_X, Inches(0.95), Inches(12), Inches(0.5),
             "What I didn't have then that you have today",
             font=SANS, size=26, bold=True, color=T.text_primary,
             spacing_em=-0.022)
    add_text(slide, PAD_X, Inches(1.50), Inches(12), Inches(0.3),
             "Same playbook. AI changes the leverage on six specific moves.",
             font=SANS, size=13, color=T.text_body, line_height=1.4)

    items = [
        ("01", "Onboarding & KYB",
         "Paper, fax, manual review · 60+ days",
         "AI extracts formation docs, resolves beneficial ownership, "
         "handles exceptions agentically",
         "24 hours → ~4 hours"),
        ("02", "Sales enablement",
         "RMs sold what they knew · inconsistent attach",
         "AI co-pilots pull industry, treasury patterns, competitor "
         "pricing into tailored proposals; coach RMs live on calls",
         "Hours → minutes"),
        ("03", "Pricing & exceptions",
         "Spreadsheets, gut feel, slow approvals",
         "AI evaluates each request vs. historical wins, LTV, attach "
         "probability; recommends in seconds",
         "Days → seconds"),
        ("04", "Account analysis & fee leakage",
         "Quarterly audits surfaced leakage after the fact",
         "AI continuously audits every analyzed account, flags mispricing "
         "in real time, drafts client conversation",
         "Quarters → days"),
        ("05", "Fraud & risk decisioning",
         "Rule-based platforms · high false positives",
         "Behavioral models catch novel patterns, reduce friction on "
         "legitimate clients",
         "Better catch, fewer complaints"),
        ("06", "Product P&L & operating insight",
         "Month-end reports · lagging indicators",
         "AI agents monitor deposits, attach, unit economics in real "
         "time; surface issues before humans ask",
         "Monthly → live"),
    ]
    col_w = Inches(3.83)
    row_h = Inches(2.20)
    gap_x = Inches(0.16)
    gap_y = Inches(0.13)
    y0 = Inches(1.95)
    for i, (idx, title, then, now, delta) in enumerate(items):
        col = i % 3
        row = i // 3
        x = PAD_X + col * (col_w + gap_x)
        y = y0 + row * (row_h + gap_y)
        add_rect(slide, x, y, col_w, row_h, fill=T.surface, line=T.hairline)
        add_text(slide, x + Inches(0.25), y + Inches(0.20),
                 Inches(0.6), Inches(0.30),
                 idx, font=MONO, size=10, color=T.orange, spacing_em=0.22)
        add_text(slide, x + Inches(0.85), y + Inches(0.20),
                 col_w - Inches(1.1), Inches(0.30),
                 title, font=SANS, size=13, bold=True, color=T.text_primary,
                 spacing_em=-0.015)
        add_hairline(slide, x + Inches(0.25), y + Inches(0.55),
                     col_w - Inches(0.5), color=T.hairline_strong)
        add_multi_text(slide, x + Inches(0.25), y + Inches(0.70),
                       col_w - Inches(0.5), row_h - Inches(1.10),
                       [
                           {'text': "THEN", 'font': MONO, 'size': 7,
                            'color': T.text_tertiary, 'spacing_em': 0.22,
                            'line_height': 1.3},
                           {'text': then, 'size': 9.5,
                            'color': T.text_body, 'line_height': 1.35,
                            'space_after': 6},
                           {'text': "NOW", 'font': MONO, 'size': 7,
                            'color': T.blue, 'spacing_em': 0.22,
                            'line_height': 1.3},
                           {'text': now, 'size': 9.5,
                            'color': T.text_primary, 'line_height': 1.35},
                       ])
        # Delta label at bottom
        add_text(slide, x + Inches(0.25), y + row_h - Inches(0.32),
                 col_w - Inches(0.5), Inches(0.25),
                 delta, font=MONO, size=9, color=T.orange, spacing_em=0.18)

    # Bottom point
    ly = Inches(6.95)
    add_rect(slide, PAD_X, ly, Inches(11.7), Inches(0.40),
             fill=T.callout_orange_bg, line=T.orange)
    add_rect(slide, PAD_X, ly, Inches(0.04), Inches(0.40), fill=T.orange)
    add_text(slide, PAD_X + Inches(0.30), ly + Inches(0.10),
             Inches(11), Inches(0.25),
             "THE POINT: Same playbook. The leverage is 10x. The "
             "institutions that win this cycle build the operating model "
             "AND wire AI into every layer at the same time.",
             font=SANS, size=10, bold=True, color=T.text_primary, line_height=1.3)

    add_footer(slide,
               "Treasury stack & financial decisions  |  Part 2: Case study")
    add_page_number(slide, num)
    return slide


def slide_first_90_days(prs, num):
    """Slide 28 — First 90 days."""
    slide = new_slide(prs)
    add_eyebrow(slide, PAD_X, PAD_TOP, "First 90 days", accent=T.orange)
    add_text(slide, PAD_X, Inches(0.95), Inches(12), Inches(0.7),
             "How to start — a 90-day playbook for a CU or mid-size FI",
             font=SANS, size=28, bold=True, color=T.text_primary,
             spacing_em=-0.022)
    add_hairline(slide, PAD_X, Inches(1.60), Inches(2.5), color=T.hairline_strong)

    blocks = [
        ("DAYS 1–30", "Diagnose & decide",
         ["Baseline current business deposit book",
          "Pick three target verticals",
          "Set 3-year deposit growth target",
          "Identify GM candidate",
          "Audit fee leakage on analyzed accounts"]),
        ("DAYS 31–60", "Architect & align",
         ["Stack architecture decision (middleware)",
          "FTP redesign principles",
          "Pricing committee charter",
          "Pod design and shared services",
          "IntraFi and decisioning partner shortlist"]),
        ("DAYS 61–90", "Stand up & ship",
         ["GM in seat with mandate",
          "First pod stood up (Acquire)",
          "Vendor contracts signed (1–2 partners)",
          "First product P&L draft circulated",
          "Member business activation campaign live"]),
    ]
    col_w = Inches(3.83)
    col_h = Inches(4.85)
    gap = Inches(0.16)
    y0 = Inches(1.85)
    for i, (label, title, items) in enumerate(blocks):
        x = PAD_X + i * (col_w + gap)
        add_rect(slide, x, y0, col_w, col_h, fill=T.surface, line=T.hairline)
        add_rect(slide, x, y0, Inches(0.025), col_h, fill=T.orange)
        add_text(slide, x + Inches(0.30), y0 + Inches(0.30),
                 col_w - Inches(0.6), Inches(0.30),
                 label, font=MONO, size=11, color=T.orange, spacing_em=0.22)
        add_text(slide, x + Inches(0.30), y0 + Inches(0.70),
                 col_w - Inches(0.6), Inches(0.55),
                 title, font=SANS, size=22, bold=True, color=T.text_primary,
                 spacing_em=-0.020)
        add_hairline(slide, x + Inches(0.30), y0 + Inches(1.40),
                     Inches(0.7), color=T.hairline_strong)
        paragraphs = []
        for it in items:
            paragraphs.append({'text': "—  " + it, 'size': 12,
                               'color': T.text_primary, 'line_height': 1.7,
                               'space_after': 6})
        add_multi_text(slide, x + Inches(0.30), y0 + Inches(1.60),
                       col_w - Inches(0.6), col_h - Inches(1.8), paragraphs)

    add_footer(slide,
               "Treasury stack & financial decisions  |  Part 2: Case study")
    add_page_number(slide, num)
    return slide


def slide_close(prs, num):
    """Slide 29 — Close."""
    slide = new_slide(prs)
    add_orange_spine(slide, x=Inches(0.40), y=Inches(0.8), h=Inches(5.9))
    add_eyebrow(slide, Inches(1.0), Inches(0.85), "Close", accent=T.orange)
    add_text(slide, Inches(1.0), Inches(1.55), Inches(11.5), Inches(1.5),
             "Same playbook. Smaller scope. Sharper focus.",
             font=SANS, size=46, bold=True, color=T.text_primary,
             spacing_em=-0.030, line_height=1.05)
    add_hairline(slide, Inches(1.0), Inches(3.40), Inches(11.3),
                 color=T.hairline_strong)
    add_text(slide, Inches(1.0), Inches(3.65), Inches(11), Inches(2.0),
             "A regional credit union or mid-size FI does not need a "
             "top-30 bank's budget to run this play. It needs a GM with "
             "authority, a stack partner strategy, a real product P&L, "
             "and the discipline to kill the operating model that got "
             "it here.",
             font=SANS, size=18, color=T.text_body, line_height=1.55)

    # Signature
    add_hairline(slide, Inches(1.0), Inches(6.20), Inches(11.3))
    add_text(slide, Inches(1.0), Inches(6.40),
             Inches(6), Inches(0.25),
             "STEVEN  |  [Your Company] LLC", font=MONO, size=10, bold=False,
             color=T.text_primary, spacing_em=0.22)
    add_text(slide, Inches(1.0), Inches(6.65),
             Inches(11), Inches(0.25),
             "Fractional technology leadership for financial services",
             font=SANS, size=12, color=T.blue, spacing_em=-0.010)
    add_text(slide, Inches(1.0), Inches(6.95),
             Inches(11), Inches(0.20),
             "Confidential — strategy brief",
             font=MONO, size=8, color=T.text_dim, spacing_em=0.18)
    add_page_number(slide, num)
    return slide


# ============================================================
# MAIN
# ============================================================

def build(mode):
    """Build the deck in the given theme mode and save to output/."""
    global T
    T = Theme(mode)

    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    # Build
    slide_cover(prs)                                              # 1
    slide_preface(prs, 2)                                         # 2
    slide_roadmap(prs, 3)                                         # 3
    slide_part_divider(prs, 4, "Part one",                        # 4
                       "Teach: the framework",
                       "Stack design, pricing logic, and the financial "
                       "levers that decide whether you grow profitably "
                       "— or unprofitably.")
    slide_stack(prs, 5)                                           # 5
    slide_placemat(prs, 6)                                        # 6
    slide_right_sized(prs, 7)                                     # 7
    slide_layers_1_2(prs, 8)                                      # 8
    slide_layers_3_4_5(prs, 9)                                    # 9
    slide_pricing(prs, 10)                                        # 10
    slide_seven_levers(prs, 11)                                   # 11
    slide_delivery(prs, 12)                                       # 12
    slide_60_day(prs, 13)                                         # 13
    slide_part_divider(prs, 14, "Part two",                       # 14
                       "Apply: the case study",
                       "How a top-30 US bank rebuilt commercial deposit "
                       "acquisition through digital transformation.")
    slide_institution(prs, 15)                                    # 15
    slide_starting_point(prs, 16)                                 # 16
    slide_strategy(prs, 17)                                       # 17
    slide_operating_model(prs, 18)                                # 18
    slide_stack_decisions(prs, 19)                                # 19
    slide_financial_decisions(prs, 20)                            # 20
    slide_change_mgmt(prs, 21)                                    # 21
    slide_outcomes(prs, 22)                                       # 22
    slide_svb_moment(prs, 23)                                     # 23
    slide_what_hurt(prs, 24)                                      # 24
    slide_translation(prs, 25)                                    # 25
    slide_lessons(prs, 26)                                        # 26
    slide_new_lesson(prs, 27)                                     # 27
    slide_first_90_days(prs, 28)                                  # 28
    slide_close(prs, 29)                                          # 29

    suffix = "" if mode == "dark" else f"-{mode}"
    # Update this path to match your workspace location
    out = (f"./output/case-study-2026{suffix}.pptx")
    prs.save(out)
    print(f"[{mode:5s}] Saved: {out}  ({len(prs.slides)} slides)")
    return out


def main():
    import sys
    modes = sys.argv[1:] if len(sys.argv) > 1 else ["dark", "light"]
    for m in modes:
        build(m)


if __name__ == "__main__":
    main()
