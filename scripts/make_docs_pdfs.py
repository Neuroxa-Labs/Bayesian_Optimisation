"""Generate portfolio PDFs: final_report.pdf and project_faq.pdf.

Uses fpdf2 + Windows Arial. Re-run after editing the markdown sources.
"""
from __future__ import annotations

import re
from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
REPORTS = ROOT / "reports" / "analysis"
DATA = ROOT / "data"

FONT_REG = Path(r"C:\Windows\Fonts\arial.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")
FONT_ITAL = Path(r"C:\Windows\Fonts\ariali.ttf")


def ascii_math(text: str) -> str:
    """Normalize markdown/math to PDF-safe Latin-1-friendly text for Arial."""
    reps = {
        "\u2212": "-",
        "\u00d7": "x",
        "\u2248": "~",
        "\u2192": "->",
        "\u00b7": "-",
        "\u2014": "-",
        "\u2013": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2026": "...",
        "\u00a0": " ",
        "⁻¹⁶": "^-16",
        "⁻¹⁰": "^-10",
        "×10": "x10",
        "\\(": "",
        "\\)": "",
        "\\[": "",
        "\\]": "",
        "$": "",
        "**": "",
        "*": "",
        "`": "",
    }
    for a, b in reps.items():
        text = text.replace(a, b)
    text = re.sub(r"\\times\s*10\^\{([^}]+)\}", r"x10^\1", text)
    text = re.sub(r"10\^\{([^}]+)\}", r"10^\1", text)
    text = re.sub(r"\\times", "x", text)
    text = re.sub(r"\\approx", "~", text)
    text = re.sub(r"\\rightarrow", "->", text)
    text = re.sub(r"\\to", "->", text)
    text = re.sub(r"\\mathbb\{R\}", "R", text)
    text = re.sub(r"f_i\s*:\s*\[0,1\]\^\{d_i\}\s*\\rightarrow\s*\\mathbb\{R\}", "f_i : [0,1]^{d_i} -> R", text)
    text = re.sub(r"\[0,1\]\^\{d_i\}", "[0,1]^{d_i}", text)
    text = re.sub(r"\\([a-zA-Z]+)", r"\1", text)
    text = re.sub(r"!\[[^\]]*\]\(([^)]+)\)", r"[figure: \1]", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", text)
    text = re.sub(r"^#+\s*", "", text)
    text = re.sub(r"^---\s*$", "", text)
    text = re.sub(r"\|", " | ", text)
    text = re.sub(r" {2,}", " ", text)
    # Drop remaining non-latin1 that can break layout/fonts
    text = text.encode("latin-1", errors="replace").decode("latin-1")
    return text.strip()


class DocPDF(FPDF):
    def __init__(self, title: str):
        super().__init__(format="A4")
        self.doc_title = title
        self.set_auto_page_break(auto=True, margin=18)
        self.add_font("Body", "", str(FONT_REG))
        self.add_font("Body", "B", str(FONT_BOLD))
        if FONT_ITAL.exists():
            self.add_font("Body", "I", str(FONT_ITAL))
        self.set_margins(16, 16, 16)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Body", "I", 8)
        self.set_text_color(90, 90, 90)
        self.cell(0, 6, self.doc_title, align="L")
        self.ln(8)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-14)
        self.set_font("Body", "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, f"Page {self.page_no()}/{{nb}}", align="C")
        self.set_text_color(0, 0, 0)

    def _write(self, text: str, h: float):
        self.set_x(self.l_margin)
        self.multi_cell(0, h, text)
        self.set_x(self.l_margin)

    def h1(self, text: str):
        self.set_font("Body", "B", 16)
        self._write(ascii_math(text), 8)
        self.ln(2)

    def h2(self, text: str):
        self.ln(2)
        self.set_font("Body", "B", 13)
        self._write(ascii_math(text), 7)
        self.ln(1)

    def h3(self, text: str):
        self.ln(1)
        self.set_font("Body", "B", 11)
        self._write(ascii_math(text), 6)

    def body(self, text: str):
        self.set_font("Body", "", 10)
        cleaned = ascii_math(text)
        if cleaned:
            self._write(cleaned, 5.2)
            self.ln(1)

    def bullet(self, text: str):
        self.set_font("Body", "", 10)
        cleaned = ascii_math(text)
        if cleaned:
            self._write(f"- {cleaned}", 5.2)

    def mono_block(self, lines: list[str]):
        self.set_font("Courier", "", 8)
        self.set_fill_color(245, 245, 245)
        for line in lines:
            self.set_x(self.l_margin)
            self.multi_cell(0, 4.5, line, fill=True)
            self.set_x(self.l_margin)
        self.ln(2)
        self.set_font("Body", "", 10)

    def add_image(self, path: Path, caption: str, w: float = 178):
        if not path.exists():
            self.body(f"[Missing figure: {path.name}]")
            return
        self.ln(1)
        self.set_x(self.l_margin)
        # Cap width to usable page width
        max_w = self.w - self.l_margin - self.r_margin
        self.image(str(path), w=min(w, max_w))
        self.set_font("Body", "I", 8)
        self.set_text_color(80, 80, 80)
        self._write(ascii_math(caption), 4.5)
        self.set_text_color(0, 0, 0)
        self.ln(2)


def cover(pdf: DocPDF, title: str, subtitle_lines: list[str]):
    pdf.add_page()
    pdf.ln(28)
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Body", "B", 20)
    pdf.multi_cell(0, 10, ascii_math(title), align="C")
    pdf.set_x(pdf.l_margin)
    pdf.ln(6)
    pdf.set_font("Body", "", 11)
    for line in subtitle_lines:
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(0, 6, ascii_math(line), align="C")
    pdf.set_x(pdf.l_margin)
    pdf.ln(10)
    pdf.set_draw_color(40, 40, 40)
    y = pdf.get_y()
    pdf.line(40, y, 170, y)
    pdf.ln(10)
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Body", "I", 9)
    pdf.multi_cell(
        0,
        5,
        "Imperial College London - PCMLAI Stage 2 - Neuroxa-Labs",
        align="C",
    )
    pdf.set_x(pdf.l_margin)


def build_final_report():
    pdf = DocPDF("BBO Final Research Report — Erkan Keskin")
    pdf.alias_nb_pages()
    cover(
        pdf,
        "Bayesian Black-Box Optimisation",
        [
            "Final research report (evidence pack)",
            "Author: Erkan Keskin",
            "https://github.com/Neuroxa-Labs/Bayesian_Optimisation",
            "Status: Weeks 1-12 complete · Week 13 queries locked · portal y pending",
            "Primary method: GP (Matern + ARD) · EI / UCB · trust-region exploit",
            "Report version: v1 (pre-Week-13 results)",
        ],
    )

    pdf.add_page()
    pdf.h1("1. Objective")
    pdf.body(
        "Maximise eight unknown continuous black-box functions f_i : [0,1]^{d_i} -> R "
        "under a strict budget of one query per function per week. True formulas are withheld; "
        "only portal evaluations (x, y) are observed. Higher y is always better. "
        "The goal is not to recover the formula; it is to find high-performing x with "
        "sample-efficient sequential decisions."
    )

    pdf.h1("2. Overall summary (after Week 12)")
    rows = [
        "F1 Radiation 2D  | best 7.711e-16 | seed incumbent; late signal lobe unresolved",
        "F2 Noisy ML 2D   | best 0.776645  | strong sharp ridge",
        "F3 Drug/adverse 3D | best -0.011366 | safe local band (x3 lock)",
        "F4 Warehouse 4D  | best 0.678600  | strong late climb (Week 12)",
        "F5 Chem. yield 4D| best 3800.74   | ridge optimum (x1 climb)",
        "F6 Cake 5D       | best -0.136    | Week-10 basin; fragile",
        "F7 HP tuning 6D  | best 1.872233  | strong late climb (Week 12)",
        "F8 8-param ML 8D | best 9.872928  | strong late climb (Week 12)",
    ]
    for r in rows:
        pdf.bullet(r)
    pdf.body("Late improve counts: W8 3/8 · W9 4/8 · W10 5/8 · W11 4/8 · W12 4/8 (F4, F5, F7, F8).")

    pdf.add_image(
        REPORTS / "results_by_week.png",
        "Figure: Compact incumbent / best-so-far by week.",
        w=178,
    )
    pdf.add_image(
        REPORTS / "progress_best_so_far.png",
        "Figure: Best-so-far curves across functions.",
        w=178,
    )

    pdf.add_page()
    pdf.h1("3. Method")
    pdf.h2("3.1 Core loop")
    for b in [
        "Load per-function history from data/function_*/initial_*.npy.",
        "Fit a Matern GP with ARD length scales (multi-restart LML).",
        "Score candidates with EI or UCB; search globally and inside a trust region.",
        "Apply per-function constraints (locks, boundary penalty, anti-duplicate, F1 trust gate).",
        "Submit a six-decimal portal string; append y; repeat.",
    ]:
        pdf.bullet(b)
    pdf.body(
        "Executable code: notebooks/BBO_Capstone_Optimized.ipynb. "
        "Transparency: DATASHEET.md · MODEL_CARD.md. "
        "Technical rationale: docs/TECHNICAL_JUSTIFICATION.md."
    )

    pdf.h2("3.2 Per-function specialisations")
    for b in [
        "F1: trust gate — refuse GP exploit while labels are ~null; exploit after signal cluster.",
        "F2: WhiteKernel noise model; hard-return to sharp ridge after misses.",
        "F3: safe x3 lock near the -0.011 neighbourhood.",
        "F4 / F7 / F8: shrinking trust-region micro-steps on ARD-sensitive axes.",
        "F5: log-y GP fit; lock high x2-x4 face; climb x1.",
        "F6: hard-return to Week-10 cake centroid after failed neighbour steps.",
    ]:
        pdf.bullet(b)

    pdf.h2("3.3 What we deliberately did not do")
    pdf.body(
        "Neural nets / large ensembles were not the primary weekly decider. "
        "With n ~ 20-50 points, calibrated uncertainty matters more than flexible curve-fitting. "
        "Peer pipelines that use NN/Optuna/TuRBO as diagnostics are compatible with this view."
    )

    pdf.h1("4. Winning-query evidence")
    for b in [
        "F1 7.711e-16 — Seed (late lobe still below seed max)",
        "F2 0.776645 — Week 5 GP/EI on noisy ridge",
        "F3 -0.011366 — Week 6 local exploit + x3 discipline",
        "F4 0.678600 — Week 12 trust-region micro-step",
        "F5 3800.74 — Week 12 ridge climb (x1=0.44)",
        "F6 -0.136 — Week 10 local basin hit",
        "F7 1.872233 — Week 12 trust-region micro-step",
        "F8 9.872928 — Week 12 trust-region micro-step",
    ]:
        pdf.bullet(b)
    pdf.body(
        "Takeaway: different functions rewarded different regimes — early ridge discovery, "
        "mid-project locks, and late compressed exploit. F1 remains sparse detection; "
        "F6 shows leaving a sharp basin without evidence is expensive."
    )

    pdf.add_page()
    pdf.h1("5. Per-function findings")
    findings = [
        (
            "F1 — Radiation source (2D)",
            "Locate a hidden source; most of the map reads ~0. Incumbent y=7.711e-16 at "
            "[0.731024, 0.733000] (seed). Weeks 10-12 opened a measurable lobe near (0.64, 0.68) "
            "with readings -0.00807 -> -0.00623 -> -0.00512 (still below seed max). "
            "Unresolved absolute peak; final round stays in the signal lobe.",
            DATA / "function_1" / "analysis_F1.png",
        ),
        (
            "F2 — Noisy ML score (2D)",
            "Incumbent y=0.776645 at [0.717869, 0.020000]. Sharp ridge: nearby steps often "
            "land ~0.54 -> hard-return policy.",
            DATA / "function_2" / "analysis_F2.png",
        ),
        (
            "F3 — Drug / adverse (3D)",
            "Incumbent y=-0.011366 at [0.492581, 0.691593, 0.401000]. x3 is sensitive; "
            "lock the safe band. History has 11 weekly points in data/.",
            DATA / "function_3" / "analysis_F3.png",
        ),
        (
            "F4 — Warehouse (4D)",
            "Incumbent y=0.678600 (Week 12). After a basin is proven, micro-steps beat global jumps.",
            DATA / "function_4" / "analysis_F4.png",
        ),
        (
            "F5 — Chemical yield (4D)",
            "Incumbent y=3800.74 at [0.44, 0.98, 0.98, 0.98]. Clearest success: lock high face, "
            "climb x1 (seed ~1089 -> ~3801).",
            DATA / "function_5" / "analysis_F5.png",
        ),
        (
            "F6 — Cake recipe (5D)",
            "Incumbent y=-0.136 (Week 10). Week 11 collapse after a small off-centroid step "
            "-> hard-return rule.",
            DATA / "function_6" / "analysis_F6.png",
        ),
        (
            "F7 — Hyperparameter tuning (6D)",
            "Incumbent y=1.872233 (Week 12). Move ARD-sensitive axes only; accept slow compound gains.",
            DATA / "function_7" / "analysis_F7.png",
        ),
        (
            "F8 — Eight-parameter ML (8D)",
            "Incumbent y=9.872928 (Week 12). Trust-region ticks + boundary penalty; "
            "do not chase edge sigma artefacts.",
            DATA / "function_8" / "analysis_F8.png",
        ),
    ]
    for title, text, img in findings:
        pdf.h2(title)
        pdf.body(text)
        pdf.add_image(img, f"Figure: {title}", w=170)
        if pdf.get_y() > 220:
            pdf.add_page()

    pdf.add_page()
    pdf.h2("Cluster view (Week 12)")
    pdf.add_image(
        REPORTS / "cluster_gallery_3d.png",
        "Figure: 3D cluster gallery across functions.",
        w=178,
    )

    pdf.h1("6. Week 13 / final round (queries locked)")
    pdf.body(
        "Near-pure exploitation and recoveries. Full rationale: weeks/WEEK13_STRATEGY.md. "
        "RL framing: weeks/final_round_rl_reflection.md."
    )
    pdf.mono_block(
        [
            "F1: 0.635000-0.688000",
            "F2: 0.717870-0.020000",
            "F3: 0.492580-0.691590-0.401000",
            "F4: 0.405000-0.412000-0.354000-0.414000",
            "F5: 0.450000-0.980000-0.980000-0.980000",
            "F6: 0.441200-0.249200-0.590800-0.728700-0.131200",
            "F7: 0.074000-0.424000-0.299000-0.158000-0.346000-0.672000",
            "F8: 0.144000-0.060000-0.210000-0.050000-0.414000-0.510000-0.216000-0.917000",
        ]
    )
    for b in [
        "F1: signal-lobe micro-step",
        "F2 / F3 / F6: hard return toward historical best",
        "F4 / F7 / F8: micro from Week-12 incumbents",
        "F5: ridge continue x1=0.45",
    ]:
        pdf.bullet(b)
    pdf.body(
        "Portal y for Week 13: pending — summary table will be updated when results arrive "
        "(scripts/append_week13.py)."
    )

    pdf.h1("7. Limitations")
    for b in [
        "One query per function per week — no inner real-function line search.",
        "GP can be confidently wrong in empty regions (inflated sigma -> boundary chase).",
        "Clustered sampling can miss a distant second mode.",
        "F1 absolute best remains a near-null seed reading despite a late measurable lobe.",
        "F2 observed best may be an optimistic draw under noise.",
        "F3 weekly count in data/ is 11 (not 12); no fabricated point was added.",
    ]:
        pdf.bullet(b)

    pdf.h1("8. Related artefacts")
    for b in [
        "Approach presentation text — docs/approach_presentation.md",
        "Project reflection — weeks/project_reflection.md",
        "Successful strategies (+ Matt peer) — weeks/successful_strategies_reflection.md",
        "Visual gallery — reports/analysis/README.md",
        "Progress dashboard — reports/progress/README.md",
        "Course file map — docs/COURSE_INDEX.md",
        "Project FAQ (PDF) — docs/project_faq.pdf",
    ]:
        pdf.bullet(b)

    pdf.h1("9. Conclusion")
    pdf.body(
        "Under a one-query-per-week budget, a single interpretable GP per function, specialised "
        "with ARD, locks, trust regions and an F1 trust gate, produced clear late gains on "
        "F4/F5/F7/F8, a strong ridge on F2, a safe band on F3, and a fragile but real basin on F6. "
        "F1 remains the hardest sparse-signal case. Week 13 commits to near-pure exploitation of "
        "those validated regions. When portal results return, the overall table and winning-query "
        "section of this report will be revised in place — without changing the method narrative."
    )

    out = DOCS / "final_report.pdf"
    pdf.output(str(out))
    print(f"Wrote {out}")


def parse_faq_md(path: Path) -> list[tuple[str, str, str]]:
    """Return list of (level, kind, text) from markdown headings/paragraphs."""
    lines = path.read_text(encoding="utf-8").splitlines()
    blocks: list[tuple[str, str, str]] = []
    buf: list[str] = []
    kind = "p"

    def flush():
        nonlocal buf, kind
        text = " ".join(x.strip() for x in buf if x.strip())
        if text:
            blocks.append(("body", kind, text))
        buf = []
        kind = "p"

    for raw in lines:
        line = raw.rstrip()
        if line.startswith("# "):
            flush()
            blocks.append(("h1", "h", line[2:].strip()))
        elif line.startswith("## "):
            flush()
            blocks.append(("h2", "h", line[3:].strip()))
        elif line.startswith("### "):
            flush()
            blocks.append(("h3", "h", line[4:].strip()))
        elif line.strip() == "---":
            flush()
        elif line.startswith("|") and "---" not in line:
            # keep table rows as bullets-ish
            flush()
            cells = [c.strip() for c in line.strip("|").split("|")]
            if cells and not all(set(c) <= set("-: ") for c in cells):
                blocks.append(("body", "bullet", " | ".join(cells)))
        elif line.startswith("- "):
            flush()
            blocks.append(("body", "bullet", line[2:].strip()))
        elif re.match(r"^\d+\.\s+", line.strip()):
            flush()
            blocks.append(("body", "bullet", re.sub(r"^\d+\.\s+", "", line.strip())))
        elif not line.strip():
            flush()
        else:
            buf.append(line)
    flush()
    return blocks


def build_faq():
    md = DOCS / "project_faq.md"
    pdf = DocPDF("BBO Project FAQ — Erkan Keskin")
    pdf.alias_nb_pages()
    cover(
        pdf,
        "Bayesian Black-Box Optimisation",
        [
            "Project FAQ",
            "Author: Erkan Keskin · Neuroxa-Labs",
            "https://github.com/Neuroxa-Labs/Bayesian_Optimisation",
            "Companion to docs/final_report.pdf",
            "Version: v1 (pre-Week-13 portal results)",
        ],
    )
    pdf.add_page()
    for level, kind, text in parse_faq_md(md):
        if level == "h1":
            # skip duplicate cover title
            if text.lower().startswith("bayesian black-box"):
                continue
            pdf.h1(text)
        elif level == "h2":
            if pdf.get_y() > 250:
                pdf.add_page()
            pdf.h2(text)
        elif level == "h3":
            if pdf.get_y() > 255:
                pdf.add_page()
            pdf.h3(text)
        elif kind == "bullet":
            pdf.bullet(text)
        else:
            pdf.body(text)

    out = DOCS / "project_faq.pdf"
    pdf.output(str(out))
    print(f"Wrote {out}")


def main():
    build_final_report()
    build_faq()


if __name__ == "__main__":
    main()
