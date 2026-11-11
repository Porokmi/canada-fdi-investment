"""Assembles the revised short paper .docx from the original (unpacked) Word file and short_source.txt.

Run from the repo root after executing FDI_Canada.ipynb (which writes the figures and table images):
    python paper/source/build_short.py ORIG_UNPACKED_DIR OUT_UNPACKED_DIR paper/source/short_source.txt

Directives: @KEEP a-b copies original body blocks verbatim; @DATELINE replaces the date on the author line;
@FIG n path places image slot n (1 = Figure 1, 2 = Figure 2, 3-5 = Tables 1-3); @CAPTION, NOTE: and EQ: lines
use the original document's caption, note and equation formatting. Equations use [base|sub|sup] for scripts.
"""
import re, shutil, struct, sys
from xml.sax.saxutils import escape

orig, out, src = sys.argv[1:4]
doc = open(f"{orig}/word/document.xml", encoding="utf8").read()
start, end = doc.index("<w:body>") + 8, doc.rindex("</w:body>")
ITEMS = re.findall(r'(<w:p[ >].*?</w:p>|<w:tbl>.*?</w:tbl>|<w:sectPr.*?</w:sectPr>)', doc[start:end], flags=re.S)
# the old layout's manual page break (before "6 Conclusion") and Word's stale render hints no longer fit
ITEMS = [i.replace("<w:pageBreakBefore/>", "").replace("<w:lastRenderedPageBreak/>", "") for i in ITEMS]
RID = {1: "rId8", 2: "rId9", 3: "rId10", 4: "rId11", 5: "rId12"}


def runs(text):
    out = []
    for tok in re.split(r'(\*[^*]+?\*)', text):
        if not tok:
            continue
        rpr, t = ("<w:rPr><w:i/></w:rPr>", tok[1:-1]) if tok.startswith("*") and len(tok) > 1 else ("", tok)
        out.append(f'<w:r>{rpr}<w:t xml:space="preserve">{escape(t)}</w:t></w:r>')
    return "".join(out)


def para(text, ppr=""):
    return f"<w:p>{'<w:pPr>' + ppr + '</w:pPr>' if ppr else ''}{runs(text)}</w:p>"


CTRL = '<m:ctrlPr><w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/></w:rPr></m:ctrlPr>'
mr = lambda t: f'<m:r><m:t xml:space="preserve">{escape(t)}</m:t></m:r>' if t else ""


def omml(expr):
    """Plain text plus [base|sub|sup] script groups, written as Office Math (matching the original equations)."""
    parts = []
    for tok in re.split(r'(\[[^\]]*\])', expr):
        if tok.startswith("["):
            base, sub, sup = (tok[1:-1].split("|") + ["", ""])[:3]
            if sub and sup:
                parts.append(f'<m:sSubSup><m:sSubSupPr>{CTRL}</m:sSubSupPr><m:e>{mr(base)}</m:e><m:sub>{mr(sub)}</m:sub><m:sup>{mr(sup)}</m:sup></m:sSubSup>')
            elif sub:
                parts.append(f'<m:sSub><m:sSubPr>{CTRL}</m:sSubPr><m:e>{mr(base)}</m:e><m:sub>{mr(sub)}</m:sub></m:sSub>')
            else:
                parts.append(f'<m:sSup><m:sSupPr>{CTRL}</m:sSupPr><m:e>{mr(base)}</m:e><m:sup>{mr(sup)}</m:sup></m:sSup>')
        else:
            parts.append(mr(tok))
    return "<m:oMath>" + "".join(parts) + "</m:oMath>"


def equation(line):
    num, expr = re.match(r"\((\d+)\)\s*(.*)", line).groups()
    return ('<w:p><w:pPr><w:tabs><w:tab w:val="center" w:pos="4680"/><w:tab w:val="right" w:pos="9360"/></w:tabs>'
            '<w:spacing w:before="160" w:after="160"/></w:pPr><w:r><w:tab/></w:r>'
            f'{omml(expr)}<w:r><w:tab/><w:t>({num})</w:t></w:r></w:p>')


def figure(n, path):
    shutil.copy(path, f"{out}/word/media/image{n}.png")
    with open(path, "rb") as f:
        f.read(16); w, h = struct.unpack(">II", f.read(8))
    cx = 4800000 if n == 1 else 5943600; cy = int(cx * h / w)
    if cy > 6800000:
        cy = 6800000; cx = int(cy * w / h)
    ppr = '<w:jc w:val="center"/>' if n <= 2 else '<w:spacing w:before="160" w:after="160"/><w:jc w:val="center"/>'
    return (f'<w:p><w:pPr>{ppr}</w:pPr><w:r><w:rPr><w:noProof/></w:rPr><w:drawing>'
            f'<wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/><wp:effectExtent l="0" t="0" r="0" b="0"/>'
            f'<wp:docPr id="{20 + n}" name="Picture {20 + n}"/><wp:cNvGraphicFramePr>'
            '<a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr>'
            '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:nvPicPr><pic:cNvPr id="0" name="image{n}.png"/><pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="{RID[n]}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
            '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>')


body, kept = [], set()
for line in open(src, encoding="utf8").read().split("\n"):
    line = line.strip()
    if not line:
        continue
    if line.startswith("@KEEP"):
        a, b = map(int, line.split()[1].split("-")); body += ITEMS[a:b + 1]; kept.update(range(a, b + 1))
    elif line.startswith("@DATELINE"):
        new = line.split(" ", 1)[1]
        body[-1] = re.sub(r"<w:t>[^<]*2026</w:t>", f"<w:t>{escape(new)}</w:t>", body[-1], count=1)
        assert new in body[-1]
    elif line.startswith("@FIG"):
        _, n, path = line.split(); body.append(figure(int(n), path))
    elif line.startswith("@CAPTION "):
        body.append(para(line[9:], "<w:keepNext/>"))
    elif line.startswith("NOTE: "):
        body.append(para(line[6:], '<w:spacing w:before="100"/>'))
    elif line.startswith("EQ: "):
        body.append(equation(line[4:]))
    else:
        body.append(para(line))

open(f"{out}/word/document.xml", "w", encoding="utf8").write(doc[:start] + "".join(body) + doc[end:])
print(f"blocks {len(body)}; kept {len(kept)} of {len(ITEMS)}; dropped {sorted(set(range(len(ITEMS))) - kept)}")
