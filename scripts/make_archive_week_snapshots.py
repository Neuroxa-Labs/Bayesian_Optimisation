"""Regenerate reports/analysis/archive weekly snapshots from data/.

For each function and each completed week, write:
  archive/function_{fn}_week{w}_analysis.png

Uses history truncated to seed + week (so Week 8 plots do not leak later points).
"""
from __future__ import annotations

import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel as C
from sklearn.gaussian_process.kernels import Matern, WhiteKernel

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "reports" / "analysis" / "archive"
OUT.mkdir(parents=True, exist_ok=True)

N_INIT = {1: 10, 2: 10, 3: 15, 4: 30, 5: 20, 6: 20, 7: 30, 8: 40}
NAME = {
    1: "Radiation", 2: "Noisy ML", 3: "Drug / adverse", 4: "Warehouse",
    5: "Chem. yield", 6: "Cake recipe", 7: "HP tuning", 8: "8-param ML",
}
CFG = {
    1: dict(a=1e-12, nu=0.5, white=False),
    2: dict(a=1e-8, nu=2.5, white=True),
    3: dict(a=1e-6, nu=1.5, white=False),
    4: dict(a=1e-4, nu=2.5, white=False),
    5: dict(a=1e-6, nu=2.5, white=False),
    6: dict(a=1e-6, nu=2.5, white=False),
    7: dict(a=1e-6, nu=2.5, white=False),
    8: dict(a=1e-5, nu=1.5, white=False),
}


def load(fn: int):
    X = np.load(DATA / f"function_{fn}" / "initial_inputs.npy").astype(float)
    Y = np.load(DATA / f"function_{fn}" / "initial_outputs.npy").astype(float).ravel()
    return X, Y


def fit_ls(X, Y, fn: int):
    c = CFG[fn]
    y = Y.copy()
    if y.max() > 100:
        y = np.log1p(np.clip(y, 0, None))
    d = X.shape[1]
    var = np.var(X, axis=0)
    var[var < 1e-6] = 0.1
    k = C(1.0, (1e-3, 1e3)) * Matern(
        length_scale=np.sqrt(var), length_scale_bounds=(1e-2, 10.0), nu=c["nu"]
    )
    if c["white"]:
        k = k + WhiteKernel(1e-3, (1e-8, 1e-1))
    gp = GaussianProcessRegressor(
        kernel=k, alpha=c["a"], n_restarts_optimizer=1,
        normalize_y=True, random_state=42,
    )
    try:
        gp.fit(X, y)
        for key, v in gp.kernel_.get_params(deep=True).items():
            if key.endswith("length_scale") and not key.endswith("bounds"):
                return np.atleast_1d(np.asarray(v, dtype=float))
    except Exception:
        pass
    return np.ones(d)


def fmt(v: float) -> str:
    a = abs(v)
    if a != 0 and a < 1e-3:
        return f"{v:.3e}"
    if a >= 1000:
        return f"{v:.1f}"
    return f"{v:.4f}"


def make_snapshot(fn: int, week: int, X: np.ndarray, Y: np.ndarray):
    n0 = N_INIT[fn]
    end = n0 + week
    if end > len(Y) or week < 1:
        return False
    Xw, Yw = X[:end], Y[:end]
    d = Xw.shape[1]
    ls = fit_ls(Xw, Yw, fn)
    order = np.argsort(ls)
    d0, d1 = int(order[0]), int(order[1] if d > 1 else 0)
    best_i = int(np.argmax(Yw))
    fb = float(Yw.max())
    run = np.maximum.accumulate(Yw)

    fig, axes = plt.subplots(2, 2, figsize=(9.5, 7.0))
    fig.suptitle(
        f"F{fn} · {NAME[fn]} · Week {week} snapshot  (n={len(Yw)}, best={fmt(fb)})",
        fontsize=12, fontweight="bold",
    )

    ax = axes[0, 0]
    colors = ["#7fbf7f"] * n0 + ["#e67e22"] * week
    colors = colors[: len(Yw)]
    colors[best_i] = "#3b7dd8"
    ax.bar(np.arange(len(Yw)), Yw, color=colors)
    ax.axvline(n0 - 0.5, ls=":", color="black", alpha=0.5)
    ax.set_title("Observed y (blue=best · orange=weekly)")
    ax.set_xlabel("obs #")
    ax.grid(axis="y", alpha=0.25)

    ax = axes[0, 1]
    ax.plot(run, color="#00b894", lw=2, label="best so far")
    ax.plot(Yw, "o", ms=3, color="#888", label="y")
    ax.axvline(n0 - 0.5, ls=":", color="black", alpha=0.5)
    ax.set_title("Best-so-far")
    ax.legend(fontsize=7)
    ax.grid(alpha=0.25)

    ax = axes[1, 0]
    cols = ["#e06666" if v >= 4.5 else ("#f2b56b" if v <= 0.5 else "#7fbf7f") for v in ls]
    ax.bar([f"x{i+1}" for i in range(d)], ls, color=cols)
    ax.set_title("ARD length scales at this week")
    ax.grid(axis="y", alpha=0.25)

    ax = axes[1, 1]
    ax.scatter(Xw[:n0, d0], Xw[:n0, d1], c="white", edgecolors="black", s=22, label="seed")
    ax.scatter(Xw[n0:, d0], Xw[n0:, d1], c="#e67e22", edgecolors="black", s=36, label="weekly")
    ax.scatter([Xw[best_i, d0]], [Xw[best_i, d1]], marker="*", c="gold",
               edgecolors="black", s=180, label="best", zorder=5)
    if week >= 1:
        ax.scatter([Xw[-1, d0]], [Xw[-1, d1]], marker="X", c="red", s=80, label=f"W{week}", zorder=6)
    ax.set_xlabel(f"x{d0+1}")
    ax.set_ylabel(f"x{d1+1}")
    ax.set_title(f"Inputs on top ARD axes (x{d0+1}, x{d1+1})")
    ax.legend(fontsize=7, loc="best")
    ax.grid(alpha=0.25)

    out = OUT / f"function_{fn}_week{week}_analysis.png"
    fig.tight_layout()
    fig.savefig(out, dpi=130, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return True


def write_readme(latest: int, counts: dict):
    lines = [
        "# Weekly analysis archive",
        "",
        f"Per-function diagnostic snapshots regenerated from `data/function_*/` through **Week {latest}**.",
        "Each file uses only the history available **at that week** (no future leakage).",
        "",
        "| Pattern | Meaning |",
        "|---------|---------|",
        "| `function_{N}_week{W}_analysis.png` | Function N after weekly round W |",
        "",
        "## Coverage",
        "",
        "| Fn | Weeks present |",
        "|----|---------------|",
    ]
    for fn in range(1, 9):
        ws = counts.get(fn, [])
        lines.append(f"| F{fn} {NAME[fn]} | {', '.join(str(w) for w in ws) if ws else '—'} |")
    lines += [
        "",
        "**Current (Week-12) gallery** (cluster hulls + best-so-far): [`../README.md`](../README.md).",
        "",
        "**Current 9-panel deep dive** per function: `data/function_N/analysis_FN.png`.",
        "",
        "Regenerate this archive:",
        "",
        "```bash",
        "python scripts/make_archive_week_snapshots.py",
        "```",
        "",
    ]
    (OUT / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    # remove stale week2-6 only files by regenerating all available weeks
    counts = {fn: [] for fn in range(1, 9)}
    latest = 0
    for fn in range(1, 9):
        X, Y = load(fn)
        n_weeks = len(Y) - N_INIT[fn]
        latest = max(latest, n_weeks)
        for w in range(1, n_weeks + 1):
            ok = make_snapshot(fn, w, X, Y)
            if ok:
                counts[fn].append(w)
                print(f"wrote function_{fn}_week{w}_analysis.png")
    write_readme(latest, counts)
    print(f"archive refresh done through Week {latest}")


if __name__ == "__main__":
    main()
