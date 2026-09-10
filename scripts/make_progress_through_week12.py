"""Rebuild reports/progress through the latest completed weekly round.

Reads data/function_*/initial_*.npy and writes:
  - progress_week{N}.png              (best-y bars for each week with data)
  - progress_week12_report.png        (late-round incumbent table)
  - bbo_progress_report.png / .jpg    (dashboard summary image)
  - bbo_progress_report.html          (interactive log through latest week)
  - README.md                         (folder guide)

Run from repo root:
  python scripts/make_progress_through_week12.py
"""
from __future__ import annotations

import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.gridspec import GridSpec

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "reports" / "progress"
OUT.mkdir(parents=True, exist_ok=True)

N_INIT = {1: 10, 2: 10, 3: 15, 4: 30, 5: 20, 6: 20, 7: 30, 8: 40}
NAME = {
    1: "Radiation",
    2: "Noisy ML",
    3: "Drug / adverse",
    4: "Warehouse",
    5: "Chem. yield",
    6: "Cake recipe",
    7: "HP tuning",
    8: "8-param ML",
}
DIM = {1: 2, 2: 2, 3: 3, 4: 4, 5: 4, 6: 5, 7: 6, 8: 8}


def load_fn(fn: int):
    X = np.load(DATA / f"function_{fn}" / "initial_inputs.npy").astype(float)
    Y = np.load(DATA / f"function_{fn}" / "initial_outputs.npy").astype(float).ravel()
    return X, Y


def max_weeks() -> int:
    return max(len(load_fn(fn)[1]) - N_INIT[fn] for fn in range(1, 9))


def week_row(fn: int, week: int):
    """Return dict for one function at one weekly round, or None if missing."""
    X, Y = load_fn(fn)
    n0 = N_INIT[fn]
    i = n0 + week - 1
    if i >= len(Y):
        return None
    prev = float(Y[:i].max()) if i else float("-inf")
    y = float(Y[i])
    return {
        "fn": fn,
        "name": NAME[fn],
        "dim": DIM[fn],
        "x": X[i],
        "y": y,
        "prev": prev,
        "improved": y > prev + 1e-15,
        "best_after": float(Y[: i + 1].max()),
    }


def improved_count(week: int) -> int:
    rows = [week_row(fn, week) for fn in range(1, 9)]
    return sum(1 for r in rows if r and r["improved"])


def fmt(v: float) -> str:
    a = abs(v)
    if a != 0 and a < 1e-3:
        return f"{v:.3e}"
    if a >= 1000:
        return f"{v:.1f}"
    if a >= 10:
        return f"{v:.3f}"
    return f"{v:.4f}"


def make_week_bar(week: int, latest: int):
    labels, bests, colors = [], [], []
    for fn in range(1, 9):
        _, Y = load_fn(fn)
        n0 = N_INIT[fn]
        end = min(n0 + week, len(Y))
        b = float(Y[:end].max())
        labels.append(f"F{fn}")
        bests.append(b)
        row = week_row(fn, week)
        colors.append("#00b894" if row and row["improved"] else "#636e72")

    # Split F5 (large yield scale) so other functions remain visible
    fig, (ax_a, ax_b) = plt.subplots(
        1, 2, figsize=(11, 4.0), gridspec_kw={"width_ratios": [3.2, 1.0]},
    )
    idx_small = [i for i in range(8) if i != 4]
    ax_a.bar(
        [labels[i] for i in idx_small],
        [bests[i] for i in idx_small],
        color=[colors[i] for i in idx_small],
        edgecolor="white",
    )
    ax_a.set_title(f"Best y after Week {week} (excl. F5)")
    ax_a.set_ylabel("best y")
    ax_a.grid(axis="y", alpha=0.3)
    ax_a.axhline(0, color="#bbb", lw=0.8)
    for i in idx_small:
        ax_a.text(labels[i], bests[i], f" {fmt(bests[i])}", va="bottom" if bests[i] >= 0 else "top",
                  ha="center", fontsize=6.5, rotation=90)

    ax_b.bar(["F5"], [bests[4]], color=[colors[4]], edgecolor="white")
    ax_b.set_title("F5 yield")
    ax_b.set_ylabel("best y")
    ax_b.grid(axis="y", alpha=0.3)
    ax_b.text(0, bests[4], f" {fmt(bests[4])}", va="bottom", ha="center", fontsize=8)

    fig.suptitle(
        f"Best observed outputs — Week {week}" + (" (latest)" if week == latest else ""),
        fontsize=11, y=1.02,
    )
    plt.tight_layout()
    out = OUT / f"progress_week{week}.png"
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", out.name)


def make_late_report_table(latest: int):
    weeks = [w for w in range(max(1, latest - 4), latest + 1)]
    col_labels = ["Fn", "Task"] + [f"W{w}" for w in weeks] + ["Δ late"]
    cell = []
    for fn in range(1, 9):
        _, Y = load_fn(fn)
        n0 = N_INIT[fn]
        vals = []
        for w in weeks:
            end = min(n0 + w, len(Y))
            vals.append(float(Y[:end].max()))
        early = float(Y[: min(n0 + weeks[0] - 1, len(Y))].max()) if weeks[0] > 1 else float(Y[:n0].max())
        delta = vals[-1] - early
        row = [f"F{fn}", NAME[fn]] + [fmt(v) for v in vals] + [fmt(delta)]
        cell.append(row)

    fig, ax = plt.subplots(figsize=(10.5, 3.2))
    ax.axis("off")
    ax.set_title(
        f"Incumbent y — Weeks {weeks[0]}–{latest} (progress folder current through Week {latest})",
        fontsize=11, pad=10,
    )
    table = ax.table(cellText=cell, colLabels=col_labels, loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1.0, 1.35)
    for (r, c), cell_obj in table.get_celld().items():
        cell_obj.set_linewidth(0.4)
        cell_obj.set_edgecolor("#ccc")
        if r == 0:
            cell_obj.set_facecolor("#f0f2f5")
            cell_obj.set_text_props(weight="bold")
    out = OUT / f"progress_week{latest}_report.png"
    fig.savefig(out, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", out.name)


def make_dashboard_image(latest: int):
    # summary cards for weeks 1..latest
    n_cards = latest
    fig = plt.figure(figsize=(14, 3.8 + 0.55 * ((latest + 1) // 2)), facecolor="white")
    gs = GridSpec(3, 1, figure=fig, height_ratios=[0.7, 0.9, 2.2], hspace=0.35)

    ax0 = fig.add_subplot(gs[0])
    ax0.axis("off")
    ax0.text(0.0, 0.85, "BBO Main Progress Report", fontsize=18, fontweight="bold",
             color="#1a1a2e", transform=ax0.transAxes, va="top")
    ax0.text(
        0.0, 0.35,
        f"Imperial College PCMLAI  ·  through Week {latest}  ·  Weeks 1–{latest} complete  ·  "
        "GP (Matérn + ARD) + EI/UCB  ·  Neuroxa-Labs/Bayesian_Optimisation",
        fontsize=9, color="#636e72", transform=ax0.transAxes, va="top",
    )

    ax1 = fig.add_subplot(gs[1])
    ax1.axis("off")
    for i, w in enumerate(range(1, latest + 1)):
        n = improved_count(w)
        x = (i % 12) / 12.0
        y = 0.55 if i < 12 else 0.05
        if latest > 12:
            x = i / max(latest, 1)
            y = 0.35
        rect = mpatches.FancyBboxPatch(
            (x + 0.005, y), 0.075, 0.4, boxstyle="round,pad=0.01",
            facecolor="#f8f9fa", edgecolor="#e0e0e0", transform=ax1.transAxes,
        )
        ax1.add_patch(rect)
        ax1.text(x + 0.042, y + 0.26, str(n), ha="center", fontsize=11, fontweight="bold",
                 color="#00b894", transform=ax1.transAxes)
        ax1.text(x + 0.042, y + 0.08, f"W{w}", ha="center", fontsize=7, color="#636e72",
                 transform=ax1.transAxes)

    # bests table
    ax2 = fig.add_subplot(gs[2])
    ax2.axis("off")
    headers = ["Fn", "Task", "Seed", "W8", "W9", "W10", "W11", "W12", "W13"]
    rows = []
    for fn in range(1, 9):
        _, Y = load_fn(fn)
        n0 = N_INIT[fn]
        def b(w):
            end = min(n0 + w, len(Y))
            return float(Y[:end].max())
        rows.append([
            f"F{fn}", NAME[fn],
            fmt(b(0)), fmt(b(8)), fmt(b(9)), fmt(b(10)), fmt(b(11)), fmt(b(12)), fmt(b(13)),
        ])
    table = ax2.table(cellText=rows, colLabels=headers, loc="upper center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1.15, 1.4)
    for (r, c), cell in table.get_celld().items():
        cell.set_linewidth(0.4)
        cell.set_edgecolor("#ccc")
        if r == 0:
            cell.set_facecolor("#f0f2f5")
            cell.set_text_props(weight="bold")

    png = OUT / "bbo_progress_report.png"
    jpg = OUT / "bbo_progress_report.jpg"
    fig.savefig(png, dpi=160, bbox_inches="tight", facecolor="white")
    fig.savefig(jpg, dpi=160, bbox_inches="tight", facecolor="white", pil_kwargs={"quality": 92})
    plt.close(fig)
    print("wrote", png.name, jpg.name)


def make_html(latest: int):
    # improve chips
    chips = []
    for w in range(1, latest + 1):
        n = improved_count(w)
        chips.append(
            f'<div class="sc"><div class="sc-n g">{n}</div><div class="sc-l">Week {w} improved</div></div>'
        )

    # per-week tables W1..latest
    week_sections = []
    for w in range(1, latest + 1):
        rows_html = []
        for fn in range(1, 9):
            r = week_row(fn, w)
            if r is None:
                rows_html.append(
                    f'<tr class="pend"><td class="fn">F{fn}<span class="sub">{NAME[fn]}</span></td>'
                    f'<td colspan="5">No observation for this week in data/</td></tr>'
                )
                continue
            cls = "imp" if r["improved"] else "wor"
            delta = r["y"] - r["prev"]
            xstr = "-".join(f"{v:.6f}" for v in r["x"])
            rows_html.append(
                f'<tr class="{cls}"><td class="fn">F{fn}<span class="sub">{r["name"]} · {r["dim"]}D</span></td>'
                f'<td class="r">{fmt(r["prev"])}</td>'
                f'<td class="r" style="font-size:10px">{xstr}</td>'
                f'<td class="r">{fmt(r["y"])}</td>'
                f'<td class="r">{"+" if delta >= 0 else ""}{fmt(delta)}</td>'
                f'<td>{"UP" if r["improved"] else "—"}</td></tr>'
            )
        week_sections.append(
            f"""
<div class="card">
  <div class="week-lbl">Week {w} — results ({improved_count(w)}/8 improved)</div>
  <table>
    <thead><tr>
      <th>Function</th><th class="r">Best before</th><th class="r">Query x</th>
      <th class="r">Actual y</th><th class="r">Δ</th><th>New best?</th>
    </tr></thead>
    <tbody>
      {"".join(rows_html)}
    </tbody>
  </table>
</div>"""
        )

    # current bests
    best_bits = []
    for fn in range(1, 9):
        _, Y = load_fn(fn)
        best_bits.append(f"F{fn} {fmt(float(Y.max()))}")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>BBO Progress Report — through Week {latest}</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:12px;background:#f0f2f5;color:#2d3436;padding:20px;line-height:1.45;}}
.wrap{{max-width:1100px;margin:0 auto;}}
.card{{background:white;border-radius:10px;padding:20px;border:1px solid #e0e0e0;margin-bottom:16px;}}
.hdr{{margin-bottom:16px;border-bottom:1px solid #eee;padding-bottom:12px;}}
.hdr h1{{font-size:18px;font-weight:700;margin-bottom:4px;color:#1a1a2e;}}
.hdr p{{font-size:11px;color:#636e72;}}
.hdr a{{color:#2d6dc7;text-decoration:none;}}
.sum{{display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap;}}
.sc{{background:#f8f9fa;border-radius:6px;padding:10px 14px;text-align:center;border:1px solid #eee;min-width:78px;}}
.sc-n{{font-size:20px;font-weight:700;}}.sc-n.g{{color:#00b894;}}
.sc-l{{font-size:9px;color:#636e72;margin-top:2px;}}
.week-lbl{{font-size:10px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#636e72;padding:8px 0 4px;border-bottom:1px solid #eee;margin-bottom:8px;}}
table{{width:100%;border-collapse:collapse;margin-bottom:8px;font-size:11px;}}
th{{background:#f8f9fa;font-weight:600;font-size:9px;color:#636e72;text-transform:uppercase;padding:6px 8px;border-bottom:1px solid #e0e0e0;text-align:left;}}
th.r,td.r{{text-align:right;font-variant-numeric:tabular-nums;font-family:ui-monospace,monospace;}}
td{{padding:6px 8px;border-bottom:1px solid #f0f0f0;vertical-align:middle;}}
tr.imp td{{background:#f0faf0;}}
tr.wor td{{background:#fffaf8;}}
tr.pend td{{color:#636e72;}}
.fn{{font-weight:600;}}.sub{{display:block;font-size:9px;color:#636e72;font-weight:400;}}
.note{{font-size:11px;color:#636e72;background:#f8f9fa;border-left:3px solid #2d6dc7;padding:10px 12px;border-radius:0 6px 6px 0;margin:12px 0;}}
img{{width:100%;border-radius:6px;border:1px solid #e0e0e0;margin-top:8px;}}
.img-row{{display:grid;grid-template-columns:1fr 1fr;gap:12px;}}
@media(max-width:700px){{.img-row{{grid-template-columns:1fr;}}}}
</style>
</head>
<body>
<div class="wrap">

<div class="card hdr">
  <h1>BBO Main Progress Report</h1>
  <p>
    Imperial College PCMLAI · through <strong>Week {latest}</strong> ·
    <a href="https://github.com/Neuroxa-Labs/Bayesian_Optimisation">GitHub</a> ·
    <a href="../../README.md">README</a> ·
    <a href="../analysis/README.md">Visual gallery</a> ·
    <a href="../../weeks/WEEK13_STRATEGY.md">Week 13 queries</a>
  </p>
  <p style="margin-top:6px;">
    Eight black-box tasks (2D–8D). One query per function per week.
    Surrogate: Gaussian Process (Matérn + ARD) with EI / UCB and trust-region exploit.
  </p>
</div>

<div class="card" style="border-left:4px solid #2d6dc7;">
  <div class="week-lbl">Status</div>
  <p class="note" style="margin:0;">
    Data-driven rebuild through <strong>Week {latest}</strong>.
    Current bests: {" · ".join(best_bits)}.
    Capstone weekly rounds complete through Week {latest}.
    Markdown gallery (renders on GitHub): <a href="../analysis/README.md">reports/analysis/README.md</a>.
  </p>
</div>

<div class="card">
  <div class="sum">
    {"".join(chips)}
  </div>
</div>

<div class="card">
  <div class="week-lbl">Dashboard preview</div>
  <a href="bbo_progress_report.png"><img src="bbo_progress_report.png" alt="BBO progress dashboard"></a>
  <div class="img-row" style="margin-top:12px;">
    <div>
      <div class="week-lbl">Latest week bars</div>
      <a href="progress_week{latest}.png"><img src="progress_week{latest}.png" alt="Week {latest} bests"></a>
    </div>
    <div>
      <div class="week-lbl">Late incumbent table</div>
      <a href="progress_week{latest}_report.png"><img src="progress_week{latest}_report.png" alt="Late report table"></a>
    </div>
  </div>
</div>

{"".join(week_sections)}

<div class="card">
  <div class="week-lbl">Archive — earlier weekly snapshots</div>
  <p class="note">Weeks 1–7 snapshot images remain in this folder (<code>progress_weekN.png</code> / <code>_report.png</code>) for audit. This HTML is the live log through Week {latest}.</p>
</div>

</div>
</body>
</html>
"""
    out = OUT / "bbo_progress_report.html"
    out.write_text(html, encoding="utf-8")
    print("wrote", out.name)


def make_readme(latest: int):
    lines = [
        "# Progress reports",
        "",
        f"Rebuilt from `data/function_*/` through **Week {latest}**.",
        "",
        "| File | Role |",
        "|------|------|",
        f"| [`bbo_progress_report.html`](bbo_progress_report.html) | Interactive log (Weeks 1–{latest}) — open locally |",
        "| [`bbo_progress_report.png`](bbo_progress_report.png) | Dashboard summary image |",
        f"| [`progress_week{latest}.png`](progress_week{latest}.png) | Best-y bars after Week {latest} |",
        f"| [`progress_week{latest}_report.png`](progress_week{latest}_report.png) | Late incumbent table |",
        "| `progress_weekN.png` | Per-week bar charts (regenerated for available weeks) |",
        "",
        "GitHub does not execute HTML. For gallery PNGs that render online, also see "
        "[`../analysis/README.md`](../analysis/README.md).",
        "",
        "Regenerate:",
        "",
        "```bash",
        "python scripts/make_progress_through_week12.py",
        "```",
        "",
    ]
    (OUT / "README.md").write_text("\n".join(lines), encoding="utf-8")
    print("wrote README.md")


def main():
    latest = max_weeks()
    print(f"latest completed weekly round in data/: Week {latest}")
    for w in range(1, latest + 1):
        # only emit bar chart if at least one function has that week
        if any(week_row(fn, w) for fn in range(1, 9)):
            make_week_bar(w, latest)
    make_late_report_table(latest)
    make_dashboard_image(latest)
    make_html(latest)
    make_readme(latest)
    print("progress folder refresh done.")


if __name__ == "__main__":
    main()
