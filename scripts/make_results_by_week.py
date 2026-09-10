"""Build reports/analysis/results_by_week.png (Seed + late weeks incumbents)."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "reports" / "analysis"
OUT.mkdir(parents=True, exist_ok=True)

N_INIT = {1: 10, 2: 10, 3: 15, 4: 30, 5: 20, 6: 20, 7: 30, 8: 40}
NAME = {
    1: "Radiation", 2: "Noisy ML", 3: "Drug / adverse", 4: "Warehouse",
    5: "Chem. yield", 6: "Cake recipe", 7: "HP tuning", 8: "8-param ML",
}
DIM = {1: 2, 2: 2, 3: 3, 4: 4, 5: 4, 6: 5, 7: 6, 8: 8}


def fmt(v: float) -> str:
    av = abs(v)
    if av == 0:
        return "0"
    if av < 1e-6 or av >= 1e4:
        return f"{v:.3e}"
    if av >= 100:
        return f"{v:.0f}"
    if av >= 10:
        return f"{v:.3f}"
    if av >= 1:
        return f"{v:.3f}"
    return f"{v:.4f}"


def best_after(Y, n0, week: int) -> float:
    end = min(n0 + week, len(Y))
    return float(Y[:end].max())


def main():
    weeks = [0, 8, 9, 10, 11, 12, 13]  # 0 = seed
    labels = ["Seed", "W8", "W9", "W10", "W11", "W12", "W13"]
    col_vals = []
    for fn in range(1, 9):
        Y = np.load(DATA / f"function_{fn}" / "initial_outputs.npy").astype(float).ravel()
        n0 = N_INIT[fn]
        row = [best_after(Y, n0, w) for w in weeks]
        col_vals.append(row)

    fig, ax = plt.subplots(figsize=(11.2, 4.2))
    ax.axis("off")
    ax.set_title(
        "Best-so-far y  ·  bold = improved vs previous column",
        fontsize=12, fontweight="bold", pad=12,
    )

    cell = []
    for fn in range(1, 9):
        vals = col_vals[fn - 1]
        texts = [f"F{fn}", NAME[fn], str(DIM[fn])]
        for j, v in enumerate(vals):
            s = fmt(v)
            if j > 0 and v > vals[j - 1] + 1e-15:
                s = f"$\\mathbf{{{s}}}$"
            texts.append(s)
        cell.append(texts)

    headers = ["Fn", "Task", "D"] + labels
    table = ax.table(cellText=cell, colLabels=headers, loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(8.5)
    table.scale(1.15, 1.55)
    for (r, c), cell_obj in table.get_celld().items():
        cell_obj.set_linewidth(0.4)
        cell_obj.set_edgecolor("#cccccc")
        if r == 0:
            cell_obj.set_facecolor("#f0f2f5")
            cell_obj.set_text_props(weight="bold", fontsize=8)
        elif c <= 2:
            cell_obj.set_text_props(ha="left" if c == 1 else "center")

    out = OUT / "results_by_week.png"
    fig.savefig(out, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", out)


if __name__ == "__main__":
    main()
