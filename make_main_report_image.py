"""Render the main BBO progress report as a high-resolution PNG/JPG image."""
import warnings
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

warnings.filterwarnings("ignore")
ROOT = Path(__file__).parent

META = {
    1: ("Radiation Detection", 2, "COV", "0.5"),
    2: ("Noisy ML Log-Lik", 2, "EI", "2.5"),
    3: ("Drug Side-Effects", 3, "UCB", "1.5"),
    4: ("Warehouse Placement", 4, "UCB", "2.5"),
    5: ("Chemical Yield", 4, "UCB", "2.5"),
    6: ("Cake Recipe", 5, "EI", "2.5"),
    7: ("ML Hyperparameters", 6, "EI", "2.5"),
    8: ("8-Param ML Model", 8, "UCB", "1.5"),
}

W1 = [
    (1, 7.71e-16, 0.00109, 4.85e-214, [0.0126, 10]),
    (2, 0.6112, 0.0150, 0.4898, [0.0717, 10]),
    (3, -0.0348, 0.1448, -0.1685, [10, 2.58, 0.0736]),
    (4, -4.0255, 0.6343, 0.2575, [1.838, 1.628, 1.846, 1.789]),
    (5, 1088.86, 1617.8, 2497.32, [10, 9.319, 0.762, 0.426]),
    (6, -0.7143, 0.4907, -0.4775, [0.601, 1.091, 1.317, 1.506, 1.131]),
    (7, 1.3650, 0.0296, 1.4506, [1.056, 10, 10, 0.359, 0.195, 0.245]),
    (8, 9.5985, 10.599, 9.7956, [3.573, 5.687, 2.643, 9.045, 10, 7.201, 3.709, 10]),
]

W2 = [
    (1, 7.71e-16, 0.27, [0.421062, 0.463562], -0.006627, [0.0123, 10]),
    (2, 0.6112, 0.0126, [0.734317, 0.926564], 0.5706, [0.0691, 10]),
    (3, -0.0348, 0.12, [0.492581, 0.691593, 0.401268], -0.0203, [10, 2.54, 0.0713]),
    (4, 0.2575, 1.365, [0.460385, 0.434644, 0.203056, 0.431758], -3.306, [1.600, 1.458, 1.634, 1.462]),
    (5, 2497.32, 2530.8, [0.074189, 0.696480, 0.980000, 0.980000], 1811.06, [10, 10, 1.146, 0.328]),
    (6, -0.4775, 0.0538, [0.517086, 0.282151, 0.771390, 0.980000, 0.207535], -0.5782, [0.538, 0.981, 1.15, 1.247, 0.997]),
    (7, 1.4506, 0.0182, [0.020000, 0.491672, 0.247422, 0.214597, 0.377195, 0.806097], 1.2983, [1.06, 10, 10, 0.378, 0.22, 0.251]),
    (8, 9.7956, 10.31, [0.070000, 0.070000, 0.020000, 0.038786, 0.403935, 0.070000, 0.070000, 0.893085],
     9.6374, [3.6, 5.703, 2.663, 9.301, 10, 7.346, 3.75, 10]),
]


def fmt(v):
    if v is None:
        return "pending"
    a = abs(v)
    if a < 1e-100:
        return "~0"
    if a >= 10000:
        return f"{v:.0f}"
    if a >= 10:
        return f"{v:.2f}"
    if a < 0.001:
        return f"{v:.2e}"
    return f"{v:.4f}"


def ls_str(ls, max_pips=8):
    parts = []
    for i, v in enumerate(ls[:max_pips]):
        if v >= 4.5:
            c = "D"
        elif v < 0.2:
            c = "S"
        else:
            c = "N"
        parts.append(f"x{i+1}:{v:.2f}{c}")
    return " ".join(parts)


def draw_table(ax, title, rows, week2=False):
    ax.axis("off")
    ax.set_title(title, loc="left", fontsize=11, fontweight="bold", color="#444", pad=8)

    if week2:
        cols = ["Fn", "Task", "AF", "nu", "Best", "Acq", "Query x", "Result", "Delta", "Length scales"]
        colw = [0.04, 0.14, 0.05, 0.04, 0.08, 0.07, 0.22, 0.07, 0.07, 0.22]
    else:
        cols = ["Fn", "Task", "AF", "nu", "Best", "Acq", "Result", "Delta", "Length scales"]
        colw = [0.04, 0.15, 0.05, 0.04, 0.09, 0.08, 0.09, 0.08, 0.38]

    cell_text = []
    cell_colors = []
    for row in rows:
        fn = row[0]
        name, dim, af, nu = META[fn]
        best, acq = row[1], row[2]
        if week2:
            xq, actual, ls = row[3], row[4], row[5]
            imp = actual - best if actual is not None else None
        else:
            actual, ls = row[3], row[4]
            imp = actual - best
        if week2 and actual is None:
            xstr = " ".join(f"{v:.3f}" for v in xq)
            delta = "pending"
            result = "pending"
            bg = "#fffde7"
        elif week2:
            xstr = " ".join(f"{v:.3f}" for v in xq)
            delta = ("+" if imp > 0 else "") + fmt(imp)
            result = fmt(actual)
            bg = "#e8f8f0" if imp > 0 else "#fdecea"
        else:
            xstr = ""
            delta = ("+" if imp > 0 else "") + fmt(imp)
            result = fmt(actual)
            bg = "#e8f8f0" if imp > 0 else "#fdecea"

        base = [f"F{fn}", f"{name}\n({dim}D)", af, nu, fmt(best), fmt(acq)]
        if week2:
            base += [xstr, result, delta, ls_str(ls)]
        else:
            base += [result, delta, ls_str(ls)]
        cell_text.append(base)
        cell_colors.append([bg] * len(cols))

    tbl = ax.table(cellText=cell_text, colLabels=cols, cellColours=cell_colors,
                   loc="center", cellLoc="center", colWidths=colw)
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(7.2)
    tbl.scale(1.0, 1.55)
    for (r, c), cell in tbl.get_celld().items():
        if r == 0:
            cell.set_text_props(fontweight="bold", color="#555")
            cell.set_facecolor("#f0f2f5")
        if c == 0:
            cell.set_text_props(fontweight="bold")


fig = plt.figure(figsize=(18, 22), facecolor="white")
gs = GridSpec(5, 1, figure=fig, height_ratios=[0.8, 0.6, 1.1, 1.3, 0.35], hspace=0.35)

# Header
ax0 = fig.add_subplot(gs[0])
ax0.axis("off")
ax0.text(0.0, 0.95, "BBO Main Progress Report", fontsize=20, fontweight="bold", color="#1a1a2e",
         transform=ax0.transAxes, va="top")
ax0.text(0.0, 0.72, "Imperial College PCMLAI  |  Cohort IMP-PCMLAI-26-02  |  8 real-world black-box functions  |  13 weeks",
         fontsize=10, color="#636e72", transform=ax0.transAxes, va="top")
ax0.text(0.0, 0.52,
         "Gaussian Process surrogate + per-function acquisition (UNC / UCB / EI). "
         "One expensive query per function per week.",
         fontsize=9.5, color="#636e72", transform=ax0.transAxes, va="top", wrap=True)

# Summary cards
ax1 = fig.add_subplot(gs[1])
ax1.axis("off")
cards = [("5", "Week 1\nimproved", "#00b894"),
         ("1", "Week 2\nimproved", "#00b894"),
         ("7", "Week 2\nworsened", "#e17055"),
         ("1", "No signal\n(F1)", "#636e72"),
         ("8", "Week 3\nready", "#2d6dc7")]
for i, (num, lbl, col) in enumerate(cards):
    x = 0.02 + i * 0.19
    rect = mpatches.FancyBboxPatch((x, 0.15), 0.16, 0.7, boxstyle="round,pad=0.02",
                                   facecolor="#f8f9fa", edgecolor="#e0e0e0", transform=ax1.transAxes)
    ax1.add_patch(rect)
    ax1.text(x + 0.08, 0.62, num, ha="center", va="center", fontsize=18, fontweight="bold",
             color=col, transform=ax1.transAxes)
    ax1.text(x + 0.08, 0.32, lbl, ha="center", va="center", fontsize=8, color="#636e72",
             transform=ax1.transAxes)

# Week 1 table
ax2 = fig.add_subplot(gs[2])
draw_table(ax2, "ITERATION 1 — Week 1 (results received)", W1, week2=False)

# Week 2 table
ax3 = fig.add_subplot(gs[3])
draw_table(ax3, "ITERATION 2 — Week 2 (results received)", W2, week2=True)

# Legend
ax4 = fig.add_subplot(gs[4])
ax4.axis("off")
legend_items = [
    ("#e17055", "Degenerate ls >= 4.5 (D)"),
    ("#fdcb6e", "Sensitive ls < 0.2 (S)"),
    ("#55efc4", "Normal (N)"),
    ("#e8f8f0", "Improved row"),
    ("#fdecea", "Worsened row"),
    ("#fffde7", "Pending (Week 2)"),
]
for i, (col, txt) in enumerate(legend_items):
    ax4.add_patch(mpatches.Rectangle((0.02 + i * 0.16, 0.35), 0.025, 0.35, facecolor=col,
                                     edgecolor="#ccc", transform=ax4.transAxes))
    ax4.text(0.05 + i * 0.16, 0.52, txt, fontsize=8, color="#636e72", va="center",
             transform=ax4.transAxes)
ax4.text(0.02, 0.05, "Full interactive report: bbo_progress_report.html  |  GitHub: Neuroxa-Labs/Bayesian_Optimisation",
         fontsize=8.5, color="#2d6dc7", transform=ax4.transAxes)

png = ROOT / "bbo_progress_report.png"
jpg = ROOT / "bbo_progress_report.jpg"
fig.savefig(png, dpi=160, bbox_inches="tight", facecolor="white")
fig.savefig(jpg, dpi=160, bbox_inches="tight", facecolor="white", pil_kwargs={"quality": 92})
plt.close(fig)
print(f"Saved {png.name} and {jpg.name}")
