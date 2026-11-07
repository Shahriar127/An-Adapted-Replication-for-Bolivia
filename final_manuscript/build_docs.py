"""
build_docs.py — build the submission documents from the Markdown sources, typeset to
match the reference article (McBride & Nichols 2018, World Bank Economic Review,
OUP house style). Specifications were measured from the article PDF with PyMuPDF:

  page 7 × 10 in (504 × 720 pt); text block 424.8 pt wide; left 39.9 pt, right 39.3 pt
  body          Sabon 9.5 pt, exact leading 12.45 pt, justified, first-line indent 12 pt
  title         Sabon Bold 18 pt (leading 22.9 pt); authors Univers Bold 12 pt
  abstract      heading Univers Bold 10 pt; text Sabon 9 pt, leading 11.95 pt; "JEL classification:" bold
  sections      Univers Bold 10 pt, Roman numerals ("I. ..."); introduction has no heading
  subsections   (not used in the reference article) Sabon Italic 9.5 pt
  author note   first-page footnote, Sabon 8 pt, leading 11 pt
  running heads Univers Condensed 8 pt, colour #231F20, 1 pt rule below; even: page | authors,
                odd: short title | page; none on page 1
  tables        caption above: "Table n." Univers Bold 7.5 + title Univers 7.5; body Sabon 7.5,
                header Sabon Bold 7; horizontal rules only (0.25 pt); notes Sabon 6 pt
  figures       caption above: "Figure n." Univers Bold 7 + title Univers 7; notes Sabon 6 pt below
  references    Univers Bold 10 pt heading; Sabon 8.5 pt, leading 11.45 pt, hanging indent 9.9 pt

Font substitution (Sabon and Univers are commercial): Sabon -> "Garamond", Univers ->
"Arial", Univers Condensed -> "Arial Narrow". On Linux these render as EB Garamond and
Liberation Sans (Narrow) via fontconfig aliases. Word uses the Office fonts of the same name.

Outputs (final_manuscript/submission/): Manuscript.docx/.pdf, Online_Appendix.docx/.pdf,
Figure1_threshold_scan.(pdf|png), Figure2_quantile_path.(pdf|png).
Usage: python3 final_manuscript/build_docs.py   (Markdown is the single source.)
"""
import os
import re
import shutil
import subprocess

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "submission")
FIGS = {"1": "Figure1_threshold_scan", "2": "Figure2_quantile_path"}
SERIF, SANS, SANS_CN = "Garamond", "Arial", "Arial Narrow"
DARK = RGBColor(0x23, 0x1F, 0x20)
TEXT_W = 424.8                                              # pt
RUNNING_AUTHORS = "Mahim, Masud, and Hossain"
RUNNING_TITLE = "Machine-Learning Proxy Means Tests: An Adapted Replication for Bolivia"
INLINE = re.compile(r"(\*\*[^*]+\*\*|\*[^*\s][^*]*\*|`[^`]+`|\[[^\]]+\]\([^)]+\))")


# ══ run / paragraph helpers ═══════════════════════════════════════════════════
def set_font(run, name=SERIF, size=9.5, bold=None, italic=None, color=None):
    run.font.name = name
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts"); rpr.insert(0, rf)
    for att in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(att), name)
    run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    if color is not None:
        run.font.color.rgb = color


def add_runs(par, text, font=SERIF, size=9.5, bold=False, color=None):
    text = text.replace("\\|", "|").replace("\\*", "\u0001")
    for tok in INLINE.split(text):
        if not tok:
            continue
        b, it, f, t = bold, False, font, tok
        if tok.startswith("**") and tok.endswith("**"):
            b, t = True, tok[2:-2]
        elif tok.startswith("`") and tok.endswith("`"):
            f, t = "Courier New", tok[1:-1]
        elif tok.startswith("[") and "](" in tok:
            t = tok[1:tok.index("](")]
        elif tok.startswith("*") and tok.endswith("*") and len(tok) > 2:
            it, t = True, tok[1:-1]
        r = par.add_run(t.replace("\u0001", "*"))
        set_font(r, f, size - (0.5 if f == "Courier New" else 0), b, it, color)
    return par


def fmt(par, lead, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first=0.0, left=0.0, before=0.0, after=0.0,
        keep_next=False):
    pf = par.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = Pt(lead)
    pf.alignment = align
    pf.first_line_indent = Pt(first)
    pf.left_indent = Pt(left)
    pf.space_before, pf.space_after = Pt(before), Pt(after)
    pf.keep_with_next = keep_next
    pf.widow_control = True
    return par


def page_field(par, font, size, color):
    """PAGE field as separate runs (begin / instr / separate / result / end), each formatted."""
    for kind, val in (("begin", None), ("instr", "PAGE"), ("separate", None), ("text", "1"), ("end", None)):
        r = par.add_run()
        set_font(r, font, size, color=color)
        if kind == "instr":
            el = OxmlElement("w:instrText"); el.set(qn("xml:space"), "preserve"); el.text = " PAGE "
            r._r.append(el)
        elif kind == "text":
            r.text = val
        else:
            el = OxmlElement("w:fldChar"); el.set(qn("w:fldCharType"), kind); r._r.append(el)


def no_hyphen(par):
    ppr = par._p.get_or_add_pPr()
    e = OxmlElement("w:suppressAutoHyphens"); e.set(qn("w:val"), "true"); ppr.append(e)
    return par


def bottom_rule(par, size_eighths=8, space=4):
    ppr = par._p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr")
    b = OxmlElement("w:bottom")
    for k, v in (("w:val", "single"), ("w:sz", str(size_eighths)), ("w:space", str(space)), ("w:color", "231F20")):
        b.set(qn(k), v)
    bdr.append(b); ppr.append(bdr)


# ══ document skeleton ═════════════════════════════════════════════════════════
def new_document(author_note=None):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = SERIF; st.font.size = Pt(9.5)
    rf = st.element.rPr.rFonts
    for att in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(att), SERIF)
    ah = OxmlElement("w:autoHyphenation"); ah.set(qn("w:val"), "true")    # as in the typeset article
    doc.settings.element.append(ah)
    doc.settings.odd_and_even_pages_header_footer = True

    sec = doc.sections[0]
    sec.page_width, sec.page_height = Pt(504), Pt(720)
    sec.left_margin, sec.right_margin = Pt(39.9), Pt(39.3)
    sec.top_margin, sec.bottom_margin = Pt(64), Pt(56)
    sec.header_distance, sec.footer_distance = Pt(36), Pt(24)
    sec.different_first_page_header_footer = True

    def running(header, left, right):
        p = header.paragraphs[0]
        fmt(p, 9.5, align=WD_ALIGN_PARAGRAPH.LEFT)
        p.paragraph_format.tab_stops.add_tab_stop(Pt(TEXT_W), WD_TAB_ALIGNMENT.RIGHT)
        for i, part in enumerate((left, right)):
            if i:
                r = p.add_run("\t"); set_font(r, SANS_CN, 8, color=DARK)
            if part == "PAGE":
                page_field(p, SANS_CN, 8, DARK)
            else:
                r = p.add_run(part); set_font(r, SANS_CN, 8, color=DARK)
        bottom_rule(p, size_eighths=8, space=3)

    running(sec.even_page_header, "PAGE", RUNNING_AUTHORS)
    running(sec.header, RUNNING_TITLE, "PAGE")
    sec.first_page_header.paragraphs[0].text = ""
    for ftr in (sec.footer, sec.even_page_footer):
        ftr.paragraphs[0].text = ""
    fp = sec.first_page_footer.paragraphs[0]
    if author_note:
        fmt(fp, 11.0, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        add_runs(fp, author_note, size=8)
    return doc


# ══ block renderers ═══════════════════════════════════════════════════════════
def heading(doc, text, level):
    text = re.sub(r"[*`]", "", text)
    p = no_hyphen(doc.add_paragraph())
    if level <= 2:                                          # "I. Section"
        fmt(p, 12.45, align=WD_ALIGN_PARAGRAPH.LEFT, before=14, after=5, keep_next=True)
        r = p.add_run(text); set_font(r, SANS, 10, bold=True)
    else:                                                   # "I.1 Subsection"
        fmt(p, 12.45, align=WD_ALIGN_PARAGRAPH.LEFT, before=8, after=2, keep_next=True)
        r = p.add_run(text); set_font(r, SERIF, 9.5, italic=True)
    return p


def caption(doc, label, title, size):
    p = no_hyphen(doc.add_paragraph())
    fmt(p, size + 2.5, align=WD_ALIGN_PARAGRAPH.LEFT, before=8, after=4, keep_next=True)
    r = p.add_run(label + " "); set_font(r, SANS, size, bold=True, color=DARK)
    r = p.add_run(title); set_font(r, SANS, size, color=DARK)


def notes(doc, text):
    p = doc.add_paragraph()
    fmt(p, 7.7, align=WD_ALIGN_PARAGRAPH.JUSTIFY, before=2, after=8)
    add_runs(p, text, size=6, color=DARK)


def cell_borders(cell, top=False, bottom=False):
    tcpr = cell._tc.get_or_add_tcPr()
    b = OxmlElement("w:tcBorders")
    for side, on in (("top", top), ("left", False), ("bottom", bottom), ("right", False)):
        e = OxmlElement(f"w:{side}")
        if on:
            for k, v in (("w:val", "single"), ("w:sz", "2"), ("w:space", "0"), ("w:color", "231F20")):
                e.set(qn(k), v)
        else:
            e.set(qn("w:val"), "nil")
        b.append(e)
    tcpr.append(b)


def table(doc, rows, body_size=7.5, head_size=7.0):
    header, body = rows[0], rows[1:]
    ncol = len(header)
    t = doc.add_table(rows=1 + len(body), cols=ncol)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblpr = t._tbl.tblPr
    w = OxmlElement("w:tblW"); w.set(qn("w:w"), str(int(TEXT_W * 20))); w.set(qn("w:type"), "dxa"); tblpr.append(w)
    mar = OxmlElement("w:tblCellMar")
    for side, v in (("left", 40), ("right", 40), ("top", 10), ("bottom", 10)):
        e = OxmlElement(f"w:{side}"); e.set(qn("w:w"), str(v)); e.set(qn("w:type"), "dxa"); mar.append(e)
    tblpr.append(mar)
    # column widths proportional to content length (as typeset tables are), fixed layout
    allrows = [header] + body
    plain = lambda x: re.sub(r"[*`]", "", x)
    charw = body_size * 0.48                                   # average glyph width (pt)
    pad = 5.0
    nat, maxl = [], []
    for j in range(ncol):
        lens = [len(plain(r[j])) if j < len(r) else 0 for r in allrows]
        word = max((len(w) for r in allrows if j < len(r) for w in plain(r[j]).split()), default=1)
        nat.append(max(max(lens) * charw + pad, 22.0))
        maxl.append(max(word * charw + pad, 22.0))           # never narrower than the longest word
    if sum(nat) <= TEXT_W:
        widths = [n * TEXT_W / sum(nat) for n in nat]
    else:
        short = [j for j in range(ncol) if nat[j] <= 95]
        widths = [0.0] * ncol
        for j in short:
            widths[j] = nat[j]
        rest = TEXT_W - sum(widths[j] for j in short)
        long_ = [j for j in range(ncol) if j not in short]
        if not long_ or rest < 30 * len(long_):              # fall back: proportional with word minimums
            widths = [max(m, n * TEXT_W / sum(nat)) for m, n in zip(maxl, nat)]
            widths = [w * TEXT_W / sum(widths) for w in widths]
        else:
            tot = sum(nat[j] for j in long_)
            for j in long_:
                widths[j] = rest * nat[j] / tot
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); tblpr.append(lay)
    grid = t._tbl.tblGrid
    for j, gc in enumerate(grid.findall(qn("w:gridCol"))):
        gc.set(qn("w:w"), str(int(widths[j] * 20)))
    numeric = re.compile(r"^[−+\-]?[\d.\[(]")
    numcol = [j > 0 and sum(1 for r in body if j < len(r) and numeric.match(plain(r[j]).strip()))
              >= 0.8 * max(len(body), 1) for j in range(ncol)]
    last = len(body)
    for i, row in enumerate(allrows):
        for j in range(ncol):
            c = t.cell(i, j)
            c.text = ""
            p = c.paragraphs[0]
            size = head_size if i == 0 else body_size
            txt = row[j] if j < len(row) else ""
            c.width = Pt(widths[j])
            right = i > 0 and numcol[j]
            fmt(p, size + 2.3, align=WD_ALIGN_PARAGRAPH.RIGHT if right else WD_ALIGN_PARAGRAPH.LEFT)
            add_runs(p, txt, size=size, bold=(i == 0), color=DARK)
            cell_borders(c, top=(i == 0), bottom=(i == 0 or i == last))
    return t


def split_row(line):
    line = line.strip().replace("\\|", "\u0000")
    return [c.strip().replace("\u0000", "|") for c in line.strip("|").split("|")]


def figure(doc, num, cap):
    title, _, rest = cap.partition(". ")
    caption(doc, f"Figure {num}.", title.rstrip("."), 7)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(os.path.join(HERE, "figures", FIGS[num] + ".png"), width=Pt(TEXT_W))
    if rest:
        notes(doc, "*Notes:* " + rest)


def render(doc, md, figcaps=None, table_sizes=(7.5, 7.0)):
    lines = md.split("\n")
    i, first_after_heading, in_fig, pending = 0, True, False, None
    while i < len(lines):
        s = lines[i].strip()
        if s == "**Figures:**":
            in_fig = True; i += 1; continue
        if in_fig:
            if s.startswith("## ") or s.startswith("**Declarations"):
                in_fig = False
            else:
                i += 1; continue
        m = re.match(r"<!-- FIGURE (\d) -->", s)
        if m:
            figure(doc, m.group(1), figcaps[m.group(1)]); first_after_heading = True; i += 1; continue
        if not s or s == "---" or s.startswith("<!--"):
            i += 1; continue
        m = re.match(r"^\*\*Table (\d+)\.\*\* (.*)$", s)
        if m:
            pending = (f"Table {m.group(1)}.", m.group(2)); i += 1; continue
        if s.startswith("|"):
            block = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                block.append(lines[i]); i += 1
            rows = [split_row(b) for b in block if not re.match(r"^\|\s*:?-{2,}", b.strip())]
            if pending:
                caption(doc, pending[0], pending[1], 7.5); pending = None
            else:
                sp = doc.add_paragraph(); fmt(sp, 4)
            table(doc, rows, *table_sizes)
            j = i
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and lines[j].strip().startswith("*Notes:*"):
                notes(doc, lines[j].strip()); i = j + 1
            else:
                sp = doc.add_paragraph(); fmt(sp, 6)
            first_after_heading = True
            continue
        m = re.match(r"^(#{1,4})\s+(.*)", s)
        if m:
            heading(doc, m.group(2), len(m.group(1))); first_after_heading = True; i += 1; continue
        m = re.match(r"^(\s*)([*-]|\d+\.)\s+(.*)", lines[i])
        if m:
            depth = len(m.group(1)) // 2
            marker = m.group(2) if m.group(2)[0].isdigit() else ("•" if depth == 0 else "–")
            p = doc.add_paragraph()
            fmt(p, 12.45, first=-9, left=12 + 11 * depth)
            p.paragraph_format.tab_stops.add_tab_stop(Pt(12 + 11 * depth))
            add_runs(p, f"{marker}\t{m.group(3)}")
            first_after_heading = False; i += 1; continue
        if s.startswith(">"):
            p = doc.add_paragraph(); fmt(p, 12.45, left=18, before=3, after=3)
            add_runs(p, s.lstrip("> ").strip()); i += 1; continue
        if s.startswith("```"):
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                p = doc.add_paragraph(); fmt(p, 9, align=WD_ALIGN_PARAGRAPH.LEFT)
                r = p.add_run(lines[i]); set_font(r, "Courier New", 7)
                i += 1
            i += 1; continue
        buf = [s]; i += 1
        while i < len(lines) and lines[i].strip() and not re.match(
                r"^(\s*([*-]|\d+\.)\s|#|\||>|---|```|<!--|\*\*Table \d)", lines[i]):
            buf.append(lines[i].strip()); i += 1
        p = doc.add_paragraph()
        fmt(p, 12.45, first=0 if first_after_heading else 12)
        add_runs(p, " ".join(buf))
        first_after_heading = False


def page_break(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def to_pdf(path):
    exe = shutil.which("soffice") or shutil.which("libreoffice")
    if not exe:
        print("  (LibreOffice not found: PDF skipped)"); return
    subprocess.run([exe, "--headless", "--convert-to", "pdf", "--outdir", OUT, path],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# ══ title block ═══════════════════════════════════════════════════════════════
def front_matter(md):
    title = md.split("\n", 1)[0].lstrip("# ").strip()
    head = md[:md.index("## Abstract")]
    authors = [l.strip() for l in head.split("\n")[1:] if l.strip() and not l.startswith("*Author note")][0]
    note = re.search(r"^\*Author note:\* (.*)$", head, re.M).group(1)
    return title, authors, note


def title_block(doc, title, authors, before=24):
    p = no_hyphen(doc.add_paragraph()); fmt(p, 22.9, align=WD_ALIGN_PARAGRAPH.LEFT, before=before, after=8)
    r = p.add_run(title); set_font(r, SERIF, 18, bold=True)
    p = no_hyphen(doc.add_paragraph()); fmt(p, 14.5, align=WD_ALIGN_PARAGRAPH.LEFT, after=10)
    r = p.add_run(authors); set_font(r, SANS, 12, bold=True)


# ══ documents ═════════════════════════════════════════════════════════════════
def build_manuscript():
    md = open(os.path.join(HERE, "MANUSCRIPT.md"), encoding="utf-8").read()
    title, authors, note = front_matter(md)
    figcaps = dict(re.findall(r"\* \*\*Figure (\d)\.\*\* (.+)", md))
    doc = new_document(author_note=note)
    title_block(doc, title, authors)

    a0 = md.index("## Abstract"); a1 = md.index("\n---", a0)
    p = doc.add_paragraph(); fmt(p, 12.45, align=WD_ALIGN_PARAGRAPH.LEFT, after=3)
    r = p.add_run("Abstract"); set_font(r, SANS, 10, bold=True)
    for line in [l.strip() for l in md[a0:a1].split("\n")[1:] if l.strip()]:
        p = doc.add_paragraph()
        if line.startswith("**JEL") or line.startswith("**Key words"):
            fmt(p, 11.95, align=WD_ALIGN_PARAGRAPH.LEFT, before=5)
        else:
            fmt(p, 11.95)
        add_runs(p, line, size=9)
    sp = doc.add_paragraph(); fmt(sp, 12.45, after=6)

    body, refs = md[a1:].split("\n## References", 1)
    render(doc, body, figcaps)

    heading(doc, "References", 2)
    for ref in [x.strip() for x in refs.split("\n") if x.strip()]:
        p = doc.add_paragraph()
        fmt(p, 11.45, align=WD_ALIGN_PARAGRAPH.LEFT, first=-9.9, left=9.9)
        add_runs(p, ref, size=8.5)
    path = os.path.join(OUT, "Manuscript.docx"); doc.save(path); to_pdf(path)
    return path


def build_appendix():
    md = open(os.path.join(HERE, "MANUSCRIPT.md"), encoding="utf-8").read()
    title, authors, note = front_matter(md)
    doc = new_document(author_note=note)
    p = doc.add_paragraph(); fmt(p, 14.5, align=WD_ALIGN_PARAGRAPH.LEFT, before=24, after=0)
    r = p.add_run("Online Appendix"); set_font(r, SANS, 12, bold=True)
    title_block(doc, title, authors, before=6)
    refs = open(os.path.join(HERE, "REFERENCES.md"), encoding="utf-8").read()
    tab = open(os.path.join(HERE, "tables", "TABLES.md"), encoding="utf-8").read()
    parts = [
        ("Appendix A. Frozen Methodology (Decision Log against McBride and Nichols 2018)",
         open(os.path.join(ROOT, "METHODOLOGY_REFERENCE.md"), encoding="utf-8").read()),
        ("Appendix B. Claim–Evidence Table", open(os.path.join(HERE, "CLAIM_EVIDENCE_TABLE.md"), encoding="utf-8").read()),
        ("Appendix C. Literature Search Log", refs[refs.index("## C."):]),
        ("Appendix D. Supplementary Tables S1–S6", tab[tab.index("## Table S1"):]),
    ]
    for k, (head, part) in enumerate(parts):
        if k:
            page_break(doc)
        heading(doc, head, 2)
        part = re.sub(r"^# .*\n", "", part, count=1)
        part = re.sub(r"^#{2,4} ", "### ", part, flags=re.M)
        render(doc, part, table_sizes=(7.0, 6.5))
    path = os.path.join(OUT, "Online_Appendix.docx"); doc.save(path); to_pdf(path)
    return path


def main():
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.startswith("Figure"):
            os.remove(os.path.join(OUT, f))
    for stem in FIGS.values():
        for ext in (".pdf", ".png"):
            shutil.copy2(os.path.join(HERE, "figures", stem + ext), os.path.join(OUT, stem + ext))
    for p in (build_manuscript(), build_appendix()):
        print("built", p)


if __name__ == "__main__":
    main()
