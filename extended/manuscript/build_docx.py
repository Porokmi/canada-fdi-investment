"""Assembles the revised Extended Working Paper .docx.

Unchanged blocks are copied byte-for-byte from the original document.xml (@KEEP a-b); new text comes from
paper_source.txt and tables from paper_tables.json, written with the original document's own paragraph,
caption, equation and table formatting.

usage (from the repo root): python extended/manuscript/build_docx.py ORIG_UNPACKED_DIR OUT_UNPACKED_DIR SOURCE TABLES_JSON [TOC_PAGES_JSON]
"""
import json, re, shutil, struct, sys
from xml.sax.saxutils import escape

orig, out, src, tables_json = sys.argv[1:5]
toc_pages = json.load(open(sys.argv[5])) if len(sys.argv) > 5 else {}

doc = open(f"{orig}/word/document.xml", encoding="utf8").read()
head, rest = doc[:doc.index("<w:body>") + 8], doc[doc.index("<w:body>") + 8:]
tail = rest[rest.rindex("</w:body>"):]
ITEMS = re.findall(r'(<w:p[ >].*?</w:p>|<w:tbl>.*?</w:tbl>|<w:sectPr.*?</w:sectPr>)', rest[:rest.rindex("</w:body>")], flags=re.S)
TABLES = json.load(open(tables_json))["tables"]
TABLES["checks"] = dict(header=["Check", "Threat addressed"], widths=[4300, 4900], rows=[
    ["Expenditure net of investment (X = N)", "Result driven by conditioning on an aggregate containing I (Section 3.3)"],
    ["Linear trend added to equation (7)", "Unmodelled FDI trend (Section 5.3)"],
    ["ECM variant (Section 5.5)", "Omitted long-run adjustment, if cointegration holds"],
    ["US-dollar estimation and the bridge sequence", "Currency-specific valuation dynamics (Section 5.6)"],
    ["Statistics Canada FDI series: direct investment liabilities (1981–2018); directional inward FDI (1991–2018)",
     "Source, vintage and conversion of the World Bank regressor; directional versus asset-liability FDI concept (Section 5.1)"],
    ["Extension to 2024 with a 2020 indicator", "Endpoint dependence; the indicator absorbs a 2020 intercept shift only"],
    ["Indicators for 2001, 2009 and 2015 (added after inspecting the data; Appendix D)",
     "FDI peaks in 2000 and 2007 preceding downturns, so that the lagged association reflects the cycle"],
    ["Lagged investment and expenditure changes, on a common 1983–2018 sample", "Omitted short-run dynamics"],
    ["Lag-selection settings for ADF and Engle–Granger", "Sensitivity of the cointegration conclusion"],
    ["HAC bandwidths 1, 3 and 4", "Sensitivity of inference, with coefficients unchanged"],
    ["Leave-one-out coefficients", "Influence of single years; no inference on gapped samples"]])

FONT = '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="Times New Roman" w:cs="Times New Roman"/>'


def runs(text, base_rpr="", font=FONT):
    """Inline markup: **bold**, *italic*, _{sub}, ^{sup}."""
    out = []
    for tok in re.split(r'(\*\*.+?\*\*|\*[^*]+?\*|_\{[^}]*\}|\^\{[^}]*\})', text):
        if not tok:
            continue
        rpr, t = base_rpr, tok
        if tok.startswith("**"):
            rpr, t = base_rpr + "<w:b/>", tok[2:-2]
        elif tok.startswith("*") and len(tok) > 1:
            rpr, t = base_rpr + "<w:i/>", tok[1:-1]
        elif tok.startswith("_{"):
            rpr, t = base_rpr + '<w:vertAlign w:val="subscript"/>', tok[2:-1]
        elif tok.startswith("^{"):
            rpr, t = base_rpr + '<w:vertAlign w:val="superscript"/>', tok[2:-1]
        # vertAlign must follow i/sz in rPr order; base_rpr holds only b/i/sz so appending is schema-safe
        out.append(f'<w:r><w:rPr>{font}{rpr}</w:rPr><w:t xml:space="preserve">{escape(t)}</w:t></w:r>')
    return "".join(out)


def para(text):
    return f"<w:p>{runs(text)}</w:p>"


def heading(text, level):
    return f'<w:p><w:pPr><w:pStyle w:val="Heading{level}"/></w:pPr>{runs(text)}</w:p>'


def caption(text, bold=True):
    keep = "<w:keepNext/>" if bold else ""
    return f'<w:p><w:pPr><w:pStyle w:val="Caption"/>{keep}</w:pPr>{runs(text, "<w:b/>" if bold else "")}</w:p>'


def equation(text):
    return f'<w:p><w:pPr><w:spacing w:before="100" w:after="200"/><w:jc w:val="center"/></w:pPr>{runs(text, "<w:i/><w:sz w:val=\"22\"/>")}</w:p>'


def ref(text):
    return (f'<w:p><w:pPr><w:spacing w:line="252" w:lineRule="auto" w:after="140"/></w:pPr>'
            f'<w:r><w:rPr>{FONT}<w:sz w:val="20"/></w:rPr><w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>')


BORD = ('<w:tcBorders><w:top w:val="single" w:color="D9D9D9" w:sz="4"/><w:left w:val="single" w:color="D9D9D9" w:sz="4"/>'
        '<w:right w:val="single" w:color="D9D9D9" w:sz="4"/><w:bottom w:val="single" w:color="D9D9D9" w:sz="4"/></w:tcBorders>'
        '<w:tcMar><w:top w:w="75" w:type="dxa"/><w:left w:w="75" w:type="dxa"/><w:bottom w:w="75" w:type="dxa"/><w:right w:w="75" w:type="dxa"/></w:tcMar>')


def cell(text, w, header, first):
    shd = '<w:shd w:fill="E8E8E8"/>' if header else ""
    jc = "left" if first else "center"
    b = "<w:b/>" if header else '<w:b w:val="0"/>'
    return (f'<w:tc><w:tcPr><w:tcW w:type="dxa" w:w="{w}"/><w:vAlign w:val="center"/>{BORD}{shd}</w:tcPr>'
            f'<w:p><w:pPr><w:keepNext/><w:spacing w:line="252" w:lineRule="auto" w:before="60" w:after="60"/><w:jc w:val="{jc}"/></w:pPr>'
            f'<w:r><w:rPr>{b}<w:sz w:val="18"/></w:rPr><w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p></w:tc>')


def table(key):
    t = TABLES[key]; ws = t["widths"]
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in ws)
    rows = [f'<w:tr><w:trPr><w:cantSplit/><w:tblHeader/></w:trPr>{"".join(cell(h, w, True, i == 0) for i, (h, w) in enumerate(zip(t["header"], ws)))}</w:tr>']
    for r in t["rows"]:
        rows.append(f'<w:tr><w:trPr><w:cantSplit/></w:trPr>{"".join(cell(c, w, False, i == 0) for i, (c, w) in enumerate(zip(r, ws)))}</w:tr>')
    return ('<w:tbl><w:tblPr><w:tblW w:type="auto" w:w="0"/><w:jc w:val="center"/><w:tblLayout w:type="fixed"/>'
            '<w:tblLook w:firstColumn="1" w:firstRow="1" w:lastColumn="0" w:lastRow="0" w:noHBand="0" w:noVBand="1" w:val="04A0"/></w:tblPr>'
            f'<w:tblGrid>{grid}</w:tblGrid>{"".join(rows)}</w:tbl>')


def png_size(path):
    with open(path, "rb") as f:
        f.read(16); return struct.unpack(">II", f.read(8))


def figure(n, path):
    rid = {1: "rId13", 2: "rId14", 3: "rId15"}[n]
    shutil.copy(path, f"{out}/word/media/image{n}.png")
    w, h = png_size(path); cx = 5715000; cy = int(cx * h / w)
    if cy > 6400000:  # keep tall figures on the page
        cy = 6400000; cx = int(cy * w / h)
    return ('<w:p><w:pPr><w:keepNext/><w:jc w:val="center"/></w:pPr><w:r><w:rPr>' + FONT + '</w:rPr><w:drawing>'
            '<wp:inline xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<wp:extent cx="{cx}" cy="{cy}"/><wp:docPr id="{n}" name="Picture {n}"/><wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>'
            '<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic>'
            f'<pic:nvPicPr><pic:cNvPr id="0" name="figure{n}.png"/><pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"/></pic:spPr>'
            '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>')


TOC_ENTRIES = ["1 Introduction and research questions", "2 Literature and the contribution of this study",
               "3 Economic framework and testable hypotheses", "4 Data and measurement", "5 Empirical strategy",
               "6 Main results", "7 Robustness and diagnostic extensions", "8 Discussion and policy implications",
               "9 Limitations and future research", "10 Conclusion", "References",
               "Appendix A Variable construction and sample accounting", "Appendix B Reproduction and research transparency",
               "Appendix C Reassessment of the original undergraduate project", "Appendix D Exploratory downturn-year indicators",
               "Appendix E FDI source verification"]


def toc():
    return "".join('<w:p><w:pPr><w:tabs><w:tab w:pos="9000" w:val="right" w:leader="dot"/></w:tabs><w:spacing w:after="160"/></w:pPr>'
                   f'<w:r><w:rPr>{FONT}</w:rPr><w:t xml:space="preserve">{escape(e)}</w:t><w:tab/><w:t>{toc_pages.get(e, "0")}</w:t></w:r></w:p>'
                   for e in TOC_ENTRIES)


body, kept = [], set()
for line in open(src, encoding="utf8").read().split("\n"):  # one element per non-empty line
    line = line.strip()
    if not line:
        continue
    if line.startswith("@KEEP"):
        a, b = map(int, line.split()[1].split("-")); body += ITEMS[a:b + 1]; kept.update(range(a, b + 1))
    elif line.startswith("@TABLE"):
        body.append(table(line.split()[1]))
    elif line.startswith("@FIG"):
        _, n, path = line.split(); body.append(figure(int(n), path))
    elif line == "@TOC":
        body.append(toc())
    elif line.startswith("## "):
        body.append(heading(line[3:], 2))
    elif line.startswith("# "):
        body.append(heading(line[2:], 1))
    elif line.startswith("CAP: "):
        body.append(caption(line[5:]))
    elif line.startswith("NOTE: "):
        body.append(caption(line[6:], bold=False))
    elif line.startswith("EQ: "):
        body.append(equation(line[4:]))
    elif line.startswith("REF: "):
        body.append(ref(line[5:]))
    else:

        body.append(para(line))

open(f"{out}/word/document.xml", "w", encoding="utf8").write(head + "".join(body) + tail)
print(f"blocks: {len(body)}; original items kept: {len(kept)} of {len(ITEMS)}; dropped: {sorted(set(range(len(ITEMS))) - kept)}")
