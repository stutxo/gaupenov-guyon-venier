#!/usr/bin/env python3
"""Build the GGV technical note from its numerical certificates."""
from pathlib import Path
import hashlib
import io
import re

import matplotlib
matplotlib.use("Agg")
from matplotlib import mathtext, rcParams
from matplotlib.font_manager import FontProperties
from PIL import Image as PILImage
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle,
    KeepTogether, Preformatted,
)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BUILD = HERE / ".build"
BUILD.mkdir(parents=True, exist_ok=True)
OUTPUT = HERE / "gaupenov_guyon_venier_whitepaper.pdf"
TITLE = "A Certified Counterexample to the Gaupenov–Guyon–Venier Conjecture"
AUTHOR = "Gemini 4 Neon"
A = 50210786624661521211023868625804408502308941866840708521188086502960440699795
C0 = 10573868466134194369802649438521576810613097274607170928
C1 = 2706910327330353758669478256263066242151633179653857834862
VIDEO = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
PAGE_W, PAGE_H = A4
MARGIN = 24 * mm
WIDTH = PAGE_W - 2 * MARGIN
INK = colors.HexColor("#161616")
MUTED = colors.HexColor("#555555")
RULE = colors.HexColor("#b9b9b9")
LINK = colors.HexColor("#243e63")
rcParams["mathtext.fontset"] = "stix"
FONT_ROOT = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
for name, filename in [
    ("PaperSerif", "STIXGeneral.ttf"),
    ("PaperSerif-Bold", "STIXGeneralBol.ttf"),
    ("PaperSerif-Italic", "STIXGeneralItalic.ttf"),
    ("PaperSerif-BoldItalic", "STIXGeneralBolIta.ttf"),
    ("PaperMono", "DejaVuSansMono.ttf"),
]:
    pdfmetrics.registerFont(TTFont(name, str(FONT_ROOT / filename)))
pdfmetrics.registerFontFamily("PaperSerif", normal="PaperSerif", bold="PaperSerif-Bold",
                             italic="PaperSerif-Italic", boldItalic="PaperSerif-BoldItalic")
pdfmetrics.registerFontFamily("PaperMono", normal="PaperMono", bold="PaperMono",
                             italic="PaperMono", boldItalic="PaperMono")

styles = {
    "title": ParagraphStyle("title", fontName="PaperSerif-Bold", fontSize=21,
        leading=24, alignment=TA_CENTER, spaceAfter=12, textColor=INK),
    "author": ParagraphStyle("author", fontName="PaperSerif", fontSize=13,
        leading=16, alignment=TA_CENTER, spaceAfter=5, textColor=INK),
    "date": ParagraphStyle("date", fontName="PaperSerif", fontSize=9.5,
        leading=12, alignment=TA_CENTER, spaceAfter=20, textColor=MUTED),
    "abstract_label": ParagraphStyle("abstract_label", fontName="PaperSerif-Bold", fontSize=10,
        leading=13, alignment=TA_CENTER, spaceAfter=4, textColor=INK),
    "abstract": ParagraphStyle("abstract", fontName="PaperSerif", fontSize=9.5,
        leading=12.6, alignment=TA_JUSTIFY, leftIndent=15, rightIndent=15,
        spaceAfter=17, textColor=INK),
    "body": ParagraphStyle("body", fontName="PaperSerif", fontSize=10.5,
        leading=14, alignment=TA_JUSTIFY, spaceAfter=8, textColor=INK),
    "small": ParagraphStyle("small", fontName="PaperSerif", fontSize=9.1,
        leading=12, alignment=TA_JUSTIFY, spaceAfter=7, textColor=INK),
    "h1": ParagraphStyle("h1", fontName="PaperSerif-Bold", fontSize=12.2,
        leading=16, spaceBefore=10, spaceAfter=8, textColor=INK, keepWithNext=True),
    "h2": ParagraphStyle("h2", fontName="PaperSerif-Bold", fontSize=10.7,
        leading=14, spaceBefore=8, spaceAfter=6, textColor=INK, keepWithNext=True),
    "mono": ParagraphStyle("mono", fontName="PaperMono", fontSize=8.0,
        leading=11, spaceAfter=7, textColor=INK),
    "code": ParagraphStyle("code", fontName="PaperMono", fontSize=8.1,
        leading=10.4, leftIndent=9, rightIndent=6, spaceBefore=5, spaceAfter=9,
        borderColor=RULE, borderWidth=.4, borderPadding=9, backColor=colors.HexColor("#f7f7f7")),
    "eqno": ParagraphStyle("eqno", fontName="PaperSerif", fontSize=10,
        leading=12, alignment=2),
    "table": ParagraphStyle("table", fontName="PaperSerif", fontSize=9.2,
        leading=11.5, spaceAfter=0),
    "reference": ParagraphStyle("reference", fontName="PaperSerif", fontSize=9,
        leading=11.7, leftIndent=16, firstLineIndent=-16, spaceAfter=7),
}


def p(text, style="body"):
    return Paragraph(text, styles[style])


def h(text):
    return p(text, "h1")


def equation(tex, label=None, size=12):
    data = io.BytesIO()
    mathtext.math_to_image("$" + tex + "$", data, prop=FontProperties(size=size),
                         dpi=450, format="png", color="black")
    data.seek(0)
    with PILImage.open(data) as im:
        width, height = im.size
    w, ht = width / 450 * 72, height / 450 * 72
    max_width = WIDTH - 38
    if w > max_width:
        ht *= max_width / w
        w = max_width
    data.seek(0)
    graphic = Image(data, width=w, height=ht)
    graphic.hAlign = "CENTER"
    row = Table([[graphic, p(f"({label})" if label else "", "eqno")]],
                colWidths=[WIDTH-34, 34])
    row.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ALIGN", (0,0), (0,0), "CENTER"),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
    ]))
    return row


def integer_line(name, value):
    return p(f"{name} = {value}", "mono")


def page_frame(canvas, doc):
    canvas.saveState()
    canvas.setTitle(TITLE)
    canvas.setAuthor(AUTHOR)
    canvas.setSubject("Formal verification and reproducible numerical certificates")
    canvas.setCreator("GGV reproducible paper builder")
    canvas.setFillColor(MUTED)
    canvas.setFont("PaperSerif", 8.5)
    if doc.page > 1:
        canvas.drawString(MARGIN, PAGE_H - 15.5 * mm, "Gaupenov–Guyon–Venier")
        canvas.drawRightString(PAGE_W-MARGIN, PAGE_H - 15.5*mm, "Gemini 4 Neon")
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(.4)
        canvas.line(MARGIN, PAGE_H-18.5*mm, PAGE_W-MARGIN, PAGE_H-18.5*mm)
    canvas.drawString(MARGIN, 13*mm, "Technical report 1.0  |  24 November 2026")
    canvas.drawRightString(PAGE_W-MARGIN, 13*mm, str(doc.page))
    canvas.restoreState()


def build():
    # Internal reproducibility checks do not print the decoded text.
    raw0, raw1 = C0.to_bytes(23, "big"), C1.to_bytes(24, "big")
    if int.from_bytes(hashlib.sha256(raw0).digest(), "big") != A:
        raise ValueError("Headline hash does not match textual certificate")
    normalize = lambda s: sorted(c.lower() for c in s if c.isalpha())
    if normalize("GaupenovGuyonVenier") != normalize(raw0.decode("ascii")):
        raise ValueError("Title certificate does not match")
    raw1.decode("ascii")
    doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN, topMargin=23*mm,
        bottomMargin=23*mm, title=TITLE, author=AUTHOR)
    story = []

    # PAGE 1: declaration and exact model.
    story += [
        p("A Certified Counterexample to the<br/>Gaupenov–Guyon–Venier Conjecture", "title"),
        p(AUTHOR, "author"),
        p("24 November 2026", "date"),
        p("Abstract", "abstract_label"),
        p("We refute the Gaupenov–Guyon–Venier conjecture in its stated discrete model. "
          "The conjecture asserts that every integer initial state eventually departs from, "
          "or descends below, its starting value. For the canonical identity transition, "
          "we prove exact persistence at every finite stage, excluding both alternatives. "
          "The announced positive integer is therefore a certified counterexample. A Lean 4 "
          "formalization checks the persistence lemmas and the negation of the conjecture "
          "without user-added axioms. The integer's SHA-256 provenance is independently "
          "reproducible, but is not assumed or verified by the Lean proof. An appendix "
          "supplies two reversible textual certificates and their decoding procedure.", "abstract"),
        h("1. The announced instance"),
        p("The following integer is the instance fixed throughout the announcement. "
          "All digits are part of the certificate, and all arithmetic is exact."),
        integer_line("a", A),
        p("<b>Gaupenov–Guyon–Venier conjecture is false.</b><br/>"
          "<i>Proof by Gemini 4 Neon.</i>"),
        h("2. Canonical system"),
        p("Let the state space be the integers. The canonical transition and its iterates "
          "are defined by"),
        equation(r"T:\mathbb{Z}\longrightarrow\mathbb{Z},\qquad T(x)=x,", "1"),
        equation(r"O_x(0)=x,\qquad O_x(n+1)=T(O_x(n)).", "2"),
        p("A <i>departure</i> is a finite stage at which the orbit differs from its initial "
          "state. A <i>descent</i> is a finite stage at which it falls strictly below that "
          "state. These predicates are defined without approximation or a finite search cutoff."),
        equation(r"\operatorname{Departure}(x)\;\Longleftrightarrow\;\exists n\in\mathbb{N},\ O_x(n)\ne x,", "3", 11),
        equation(r"\operatorname{Descent}(x)\;\Longleftrightarrow\;\exists n\in\mathbb{N},\ O_x(n)<x.", "4", 11),
        PageBreak(),
    ]

    # PAGE 2: an entirely real but deliberately elementary refutation.
    story += [
        h("3. Resolution of the conjecture"),
        p("<b>Conjecture 3.1 (Gaupenov–Guyon–Venier).</b> Every integer initial state "
          "admits a departure or a descent under the canonical transition:"),
        equation(r"\forall x\in\mathbb{Z},\quad\operatorname{Departure}(x)\vee\operatorname{Descent}(x).", "5", 11),
        p("The transition in (1) must be kept in the statement. Altering that transition "
          "would define a different conjecture, to which the present certificate makes no claim."),
        p("<b>Lemma 3.2 (Exact persistence).</b> For every integer <i>x</i> and every "
          "natural number <i>n</i>, the orbit satisfies"),
        equation(r"O_x(n)=x.", "6"),
        p("<i>Proof.</i> The initial case is the defining equation for the orbit. Assume "
          "the equality at stage <i>n</i>. The successor stage then reduces to"),
        equation(r"O_x(n+1)=T(O_x(n))=O_x(n)=x.", "7"),
        p("Induction establishes the claim at every finite stage. No bound on the magnitude "
          "of <i>x</i> or on the iteration index is required. <i>Q.E.D.</i>"),
        p("<b>Lemma 3.3 (Exclusion of departure).</b> No initial state admits a departure. "
          "Indeed, a witness for Departure(<i>x</i>) would contradict (6)."),
        p("<b>Lemma 3.4 (Exclusion of descent).</b> No initial state admits a descent. "
          "Substituting (6) into its defining strict inequality would require "
          "<i>x</i> &lt; <i>x</i>, contradicting irreflexivity of the integer order."),
        p("<b>Theorem 3.5 (Certified counterexample).</b> For the announced integer <i>a</i>,"),
        equation(r"\neg\operatorname{Departure}(a)\ \wedge\ \neg\operatorname{Descent}(a).", "8", 11),
        p("<i>Proof.</i> Apply Lemmas 3.3 and 3.4 to <i>a</i>. Hence the disjunction in "
          "Conjecture 3.1 fails at that integer, and the conjecture is false. <i>Q.E.D.</i>"),
        h("3.1. Strength of the counterexample"),
        p("The argument is uniform: every integer is a counterexample in this model. "
          "The selected <i>a</i> identifies the announced instance; its cryptographic "
          "properties play no role in the contradiction. Every digit is retained, "
          "although the proof applies equally to zero."),
        p("In particular, increasing the magnitude of the witness neither strengthens "
          "nor weakens the logical conclusion. The model exhibits exact stability "
          "under the absence of change."),
        PageBreak(),
    ]

    # PAGE 3: reversible numerical clues, with plaintext deliberately absent.
    story += [
        h("4. Numerical certificates"),
        p("To separate the formal counterexample from the interpretation of its "
          "announcement, we attach two auxiliary textual certificates. Their representation "
          "is reversible; it is an encoding, not encryption and not a cryptographic hash."),
        p("For a byte vector <i>c</i> of length <i>m</i>, with each component between "
          "0 and 255, define its unsigned big-endian representation by"),
        equation(r"E_m(c)=\sum_{j=0}^{m-1}c_j\,256^{m-1-j}.", "9"),
        p("Let <i>D</i><sub>m</sub> recover exactly <i>m</i> base-256 digits, including "
          "leading zero bytes if necessary. Uniqueness of positional representation gives"),
        equation(r"D_m(E_m(c))=c.", "10"),
        p("The auxiliary coefficients and their prescribed lengths are"),
        integer_line("C0", C0),
        integer_line("C1", C1),
        equation(r"m_0=23,\qquad m_1=24.", "11"),
        p("Both decoded vectors lie in ASCII. The companion Lean file "
          "<font name='PaperMono' size='8.3'>TextCertificates.lean</font> checks their exact "
          "encodings by reduction. Their textual interpretation is left to the decoder "
          "in Appendix A."),
        h("4.1. Relation to the announced witness"),
        p("The selected integer <i>a</i> is the big-endian interpretation of the SHA-256 "
          "digest of the first decoded vector:"),
        equation(r"a=\operatorname{Int}_{\rm BE}\!\left(\operatorname{SHA256}(D_{23}(C_0))\right).", "12", 11),
        p("This equality is reproduced with Python's standard-library implementation. "
          "The Lean counterexample does not implement SHA-256 and does not rely on (12). "
          "The hash identifies the announcement; the induction proves its stated claim."),
        h("4.2. A certificate in the title"),
        p("Let <i>M</i>(<i>s</i>) be the multiset of lowercase ASCII letters in a string, "
          "after spaces and punctuation have been removed. The name obeys a further exact identity:"),
        equation(r"M(\mathtt{GaupenovGuyonVenier})=M(D_{23}(C_0)).", "13", 11),
        p("Thus the title and the first textual certificate contain the same letters. "
          "This agreement is checked by the reproducer alongside the digest relation. "
          "It has no effect on the mathematical refutation."),
        PageBreak(),
    ]

    # PAGE 4: reproduction, scope, references, and a restrained final reveal.
    story += [
        h("5. Formal verification and reproducibility"),
        p("The companion project uses Lean 4.19.0 and Lean core only. Its principal "
          "declarations correspond directly to the definitions and result above:"),
    ]
    rows = [
        [p("<b>Source module</b>", "table"), p("<b>Role</b>", "table")],
        [p("Definitions.lean", "table"), p("Orbit, conjecture, and exact persistence", "table")],
        [p("Preservation.lean", "table"), p("Exclusion of departure", "table")],
        [p("Stability.lean", "table"), p("Exclusion of strict descent", "table")],
        [p("Proof.lean", "table"), p("Announced counterexample and formal refutation", "table")],
        [p("TextCertificates.lean", "table"), p("Exact auxiliary encoding equalities", "table")],
    ]
    table = Table(rows, colWidths=[160, WIDTH-160], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("LINEABOVE", (0,0), (-1,0), .6, INK),
        ("LINEBELOW", (0,0), (-1,0), .4, INK),
        ("LINEBELOW", (0,-1), (-1,-1), .6, INK),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    story += [table, Spacer(1, 10),
        p("Run the following from the repository root. The final command independently "
          "checks the headline digest, both textual encodings, and reference consistency."),
        Preformatted("lake build\nlake exe ggv\npython3 scripts/verify_certificate.py", styles["code"]),
        p("The refutation contains no <font name='PaperMono' size='8.5'>sorry</font> "
          "placeholders or user-added axioms. Its axiom report includes Lean's standard "
          "<font name='PaperMono' size='8.5'>propext</font> through integer order. "
          "The two textual encoding certificates have empty axiom reports. "
          "These checks concern the explicitly defined system, not an external mathematical problem.", "small"),
        h("Appendix A. Decoder"),
        p("Using the values and lengths in Section 4, the textual certificates can be "
          "recovered without a search. The digest relation can then be reproduced independently.", "small"),
        Preformatted(
            "from hashlib import sha256\n\n"
            "def decode_certificate(value, length):\n"
            "    return value.to_bytes(length, \"big\").decode(\"ascii\")\n\n"
            "s0 = decode_certificate(C0, 23)\n"
            "s1 = decode_certificate(C1, 24)\n"
            "assert int.from_bytes(sha256(s0.encode(\"ascii\")).digest(),\n"
            "                      \"big\") == a\n"
            "print(s0)\nprint(s1)", styles["code"]),
        p(f"<link href='{VIDEO}' color='#243e63'><u>Supplementary construction</u></link>.", "small"),
        h("References"),
        p("[1] L. de Moura and S. Ullrich. <i>The Lean 4 Theorem Prover and Programming "
          "Language.</i> CADE-28, 2021. "
          "<link href='https://doi.org/10.1007/978-3-030-79876-5_37' color='#243e63'>"
          "doi:10.1007/978-3-030-79876-5_37</link>.", "reference"),
        p("[2] Companion formalization. <i>Gaupenov–Guyon–Venier</i>, version 1.0. "
          "Lean source, certificate reproducer, and this report's build source are "
          "distributed together.", "reference"),
    ]
    doc.build(story, onFirstPage=page_frame, onLaterPages=page_frame)
    print(OUTPUT)


if __name__ == "__main__":
    build()
