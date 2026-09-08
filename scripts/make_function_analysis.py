"""Comprehensive per-function BBO analysis figures (one PNG per function).

Uses the full evaluation history in data/function_*/initial_*.npy
(initial seed + weekly queries through the latest completed round).
"""
from __future__ import annotations

import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from scipy.stats import norm
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel as C
from sklearn.gaussian_process.kernels import Matern, WhiteKernel

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = ROOT / "data"

# n = initial seed size (weekly queries start after this index)
CFG = {
    1: dict(dim=2, n=10, a=1e-12, nu=0.5, white=False, m="EI", k=None),
    2: dict(dim=2, n=10, a=1e-8, nu=2.5, white=True, m="EI", k=None),
    3: dict(dim=3, n=15, a=1e-6, nu=1.5, white=False, m="EI", k=None),
    4: dict(dim=4, n=30, a=1e-4, nu=2.5, white=False, m="UCB", k=1.5),
    5: dict(dim=4, n=20, a=1e-6, nu=2.5, white=False, m="EI", k=None),
    6: dict(dim=5, n=20, a=1e-6, nu=2.5, white=False, m="EI", k=None),
    7: dict(dim=6, n=30, a=1e-6, nu=2.5, white=False, m="EI", k=None),
    8: dict(dim=8, n=40, a=1e-5, nu=1.5, white=False, m="UCB", k=1.5),
}

NAME = {
    1: "Radiation Source Detection",
    2: "Noisy ML Log-Likelihood",
    3: "Drug Discovery - Adverse Reactions",
    4: "Warehouse Placement",
    5: "Chemical Yield Optimisation",
    6: "Cake Recipe Optimisation",
    7: "ML Hyperparameter Tuning",
    8: "8-Parameter ML Model Optimisation",
}

STORY = {
    1: ("Locate a hidden radiation source on a 2-D map.",
        "x = (position); y = counter reading. Sharp, sparse peak: almost everywhere reads 0.",
        "Trust-gated exploit once a non-null signal lobe appears near (0.64, 0.68)."),
    2: ("Tune a noisy machine-learning model's log-likelihood.",
        "x = 2 settings; y = noisy log-likelihood (higher is better).",
        "EI + White kernel; late weeks return toward the sharp 0.777 ridge."),
    3: ("Minimise adverse drug reactions by mixing 3 components.",
        "x = component ratios; y = -(side effect). y near 0 = good.",
        "Safe x3 lock + local EI around the -0.011 neighbourhood."),
    4: ("Optimise warehouse item placement (4 factors).",
        "x = 4 placement factors; y = efficiency score.",
        "Trust-region micro-steps around the late incumbent."),
    5: ("Maximise chemical reaction yield (single ridge).",
        "x = 4 process settings; y = yield.",
        "Lock high x2-x4 face; climb x1 along the ridge (log-y GP fit)."),
    6: ("Find the best cake recipe (5 ingredients).",
        "x = 5 ingredient amounts; y = -(badness). y near 0 = good.",
        "Hard-return to Week-10 basin after failed neighbour steps."),
    7: ("Tune 6 hyperparameters of an ML model.",
        "x = 6 hyperparameters; y = validation score.",
        "Local EI around the late peak; move sensitive ARD axes only."),
    8: ("Optimise an 8-parameter ML model.",
        "x = 8 parameters; y = score.",
        "Slow late gains via small trust-region steps in ARD-sensitive dims."),
}

WEEK_MARKERS = [
    ("o", "#9b59b6"), ("^", "#00bcd4"), ("D", "#ff9800"), ("P", "#8bc34a"),
    ("s", "#e91e63"), ("v", "#795548"), ("*", "#607d8b"), ("X", "#3f51b5"),
    ("h", "#009688"), ("p", "#cddc39"), ("<", "#ff5722"), (">", "#673ab7"),
]


def fit(X, Y, c):
    y = Y.astype(float).copy()
    if y.max() > 100:  # F5-scale stabilisation
        y = np.log1p(np.clip(y, 0, None))
    var = np.var(X, axis=0)
    var[var < 1e-6] = 0.1
    mk = Matern(length_scale=np.sqrt(var), length_scale_bounds=(1e-2, 10.0), nu=c["nu"])
    k = C(1.0, (1e-3, 1e3)) * mk
    if c["white"]:
        k = k + WhiteKernel(1e-3, (1e-8, 1e-1))
    gp = GaussianProcessRegressor(
        kernel=k, alpha=c["a"], n_restarts_optimizer=3,
        normalize_y=True, random_state=42,
    )
    gp.fit(X, y)
    return gp


def length_scales(gp):
    for k, v in gp.kernel_.get_params(deep=True).items():
        if k.endswith("length_scale") and not k.endswith("bounds"):
            return np.atleast_1d(np.asarray(v, dtype=float))
    return None


def acq_grid(gp, G, m, k, fb_fit):
    mu, sg = gp.predict(G, return_std=True)
    if m == "UCB":
        return mu + (k or 0.0) * sg
    if m == "UNC":
        return sg
    s = np.maximum(sg, 1e-12)
    z = (mu - fb_fit) / s
    return np.maximum((mu - fb_fit) * norm.cdf(z) + s * norm.pdf(z), 0.0)


def fmt(v):
    a = abs(v)
    if a != 0 and (a < 1e-3 or a >= 1e4):
        return f"{v:.2e}"
    return f"{v:.3f}"


def make_figure(fn: int):
    c = CFG[fn]
    dim, n0 = c["dim"], c["n"]
    X = np.load(DATA_ROOT / f"function_{fn}" / "initial_inputs.npy").astype(float)
    Y = np.load(DATA_ROOT / f"function_{fn}" / "initial_outputs.npy").astype(float).ravel()
    assert len(X) == len(Y)
    n_weeks = max(0, len(Y) - n0)
    last_week = n_weeks  # completed weekly rounds in the arrays

    gp = fit(X, Y, c)
    ls = length_scales(gp)
    fb = float(Y.max())
    best_i = int(np.argmax(Y))
    best_x = X[best_i]

    y_fit = Y.copy()
    if y_fit.max() > 100:
        y_fit = np.log1p(np.clip(y_fit, 0, None))
    fb_fit = float(y_fit.max())

    order = np.argsort(ls)
    d0, d1 = (int(order[0]), int(order[1])) if dim >= 2 else (0, 0)

    fig = plt.figure(figsize=(20, 13.5))
    gs = gridspec.GridSpec(
        3, 3, figure=fig, hspace=0.42, wspace=0.28,
        left=0.05, right=0.97, top=0.9, bottom=0.06,
    )
    fig.suptitle(
        f"F{fn}  ·  {NAME[fn]}  ({dim}-D)\n"
        f"Full history through Week {last_week}  ·  n={len(Y)}  ·  best y={fmt(fb)}",
        fontsize=17, fontweight="bold",
    )

    # (1) Observed y
    ax = fig.add_subplot(gs[0, 0])
    idx = np.arange(len(Y))
    colors = []
    for i, y in enumerate(Y):
        if i == best_i:
            colors.append("#3b7dd8")
        elif i >= n0:
            colors.append(WEEK_MARKERS[(i - n0) % len(WEEK_MARKERS)][1])
        elif y >= np.percentile(Y, 66):
            colors.append("#7fbf7f")
        elif y >= np.percentile(Y, 33):
            colors.append("#f2b56b")
        else:
            colors.append("#e06666")
    ax.bar(idx, Y, color=colors)
    ax.axhline(fb, ls="--", color="green", lw=1, alpha=0.6)
    ax.axvline(n0 - 0.5, ls=":", color="black", alpha=0.5)
    ax.set_title(f"(1) Observed y\n(blue=best · weekly queries coloured · left of line=seed)",
                 fontsize=11, fontweight="bold")
    ax.set_xlabel("observation #")
    ax.set_ylabel("y")
    ax.grid(alpha=0.25, axis="y")

    # (2) length scales
    ax = fig.add_subplot(gs[0, 1])
    lsc = ["#e06666" if v >= 4.5 else ("#f2b56b" if v <= 0.5 else "#7fbf7f") for v in ls]
    ax.bar([f"x{i+1}" for i in range(dim)], ls, color=lsc)
    ax.axhline(4.5, ls="--", color="red", lw=1, label="degenerate (>=4.5)")
    ax.axhline(0.5, ls=":", color="orange", lw=1, label="sensitive (<=0.5)")
    for i, v in enumerate(ls):
        ax.text(i, v, f"{v:.2f}", ha="center", va="bottom", fontsize=8)
    ax.set_title("(2) Kernel length scales (ARD)", fontsize=11, fontweight="bold")
    ax.set_ylabel("length scale")
    ax.legend(fontsize=7)
    ax.grid(alpha=0.25, axis="y")

    # (3) strategy text
    ax = fig.add_subplot(gs[0, 2])
    ax.axis("off")
    goal, mean_, why = STORY[fn]
    deg = [i + 1 for i in range(dim) if ls[i] >= 4.5]
    sens = [i + 1 for i in range(dim) if ls[i] <= 0.5]
    late = Y[n0:] if n_weeks else np.array([])
    late_best = float(late.max()) if len(late) else float("nan")
    txt = (
        f"STRATEGY & STATUS\n"
        f"--------------------------------\n"
        f"Real world : {goal}\n"
        f"Meaning    : {mean_}\n\n"
        f"GP kernel  : Matern nu={c['nu']}, alpha={c['a']:g}"
        f"{' + WhiteKernel' if c['white'] else ''}\n"
        f"Acquisition: {c['m']}" + (f" (k={c['k']})" if c['k'] else "") + "\n"
        f"Policy     : {why}\n\n"
        f"Observations: {len(Y)}  (seed {n0} + {n_weeks} weeks)\n"
        f"Best y      : {fmt(fb)}\n"
        f"at x = [{', '.join(fmt(v) for v in best_x)}]\n"
        f"Best among weekly queries: {fmt(late_best) if len(late) else 'n/a'}\n\n"
        f"Degenerate dims: {deg if deg else 'none'}\n"
        f"Sensitive dims : {sens if sens else 'none'}"
    )
    ax.text(0.0, 1.0, txt, va="top", ha="left", fontsize=9.0, family="monospace",
            transform=ax.transAxes, wrap=True)

    # Heatmaps over (d0, d1)
    res = 60
    g = np.linspace(0.02, 0.98, res)
    G1, G2 = np.meshgrid(g, g)
    base = np.tile(best_x, (res * res, 1)).astype(float)
    base[:, d0] = G1.ravel()
    base[:, d1] = G2.ravel()
    mu_g, sg_g = gp.predict(base, return_std=True)
    acq_g = acq_grid(gp, base, c["m"], c["k"], fb_fit)

    def overlay(ax):
        ax.scatter(X[:n0, d0], X[:n0, d1], c="white", edgecolors="black", s=22,
                   label="seed", zorder=3)
        show_from = max(0, n_weeks - 8)  # last 8 weeks markers to avoid clutter
        for w in range(show_from, n_weeks):
            i = n0 + w
            mk, col = WEEK_MARKERS[w % len(WEEK_MARKERS)]
            ax.scatter([X[i, d0]], [X[i, d1]], marker=mk, c=col, edgecolors="black",
                       s=110, zorder=5, label=f"W{w+1}")
        ax.scatter([best_x[d0]], [best_x[d1]], marker="*", c="gold", edgecolors="black",
                   s=280, label="best", zorder=6)
        ax.set_xlabel(f"x{d0+1}")
        ax.set_ylabel(f"x{d1+1}")

    for j, (ttl, Z, cmap) in enumerate([
        ("(4) GP mean", mu_g, "viridis"),
        ("(5) GP uncertainty", sg_g, "magma"),
        ("(6) Acquisition", acq_g, "cividis"),
    ]):
        ax = fig.add_subplot(gs[1, j])
        cf = ax.contourf(G1, G2, Z.reshape(res, res), levels=25, cmap=cmap)
        plt.colorbar(cf, ax=ax, fraction=0.046, pad=0.04)
        overlay(ax)
        extra = "  (other dims @ best)" if dim > 2 else ""
        ax.set_title(f"{ttl}\nx{d0+1} vs x{d1+1}{extra}", fontsize=10.5, fontweight="bold")
        if j == 0:
            ax.legend(fontsize=6, loc="best", ncol=2)

    # (7) sensitivity slice
    ax = fig.add_subplot(gs[2, 0])
    line = np.tile(best_x, (200, 1)).astype(float)
    gg = np.linspace(0.02, 0.98, 200)
    line[:, d0] = gg
    mu_l, sg_l = gp.predict(line, return_std=True)
    ax.plot(gg, mu_l, color="#3b7dd8", label="GP mean")
    ax.fill_between(gg, mu_l - 1.96 * sg_l, mu_l + 1.96 * sg_l, color="#3b7dd8",
                     alpha=0.18, label="95% band")
    ax.axvline(best_x[d0], ls="--", color="gold", label="best")
    if n_weeks:
        ax.axvline(X[-1, d0], ls=":", color="red", label=f"W{last_week}")
    ax.set_title(f"(7) Sensitivity along x{d0+1}", fontsize=11, fontweight="bold")
    ax.set_xlabel(f"x{d0+1}")
    ax.set_ylabel("GP mean (fit scale)")
    ax.legend(fontsize=7)
    ax.grid(alpha=0.25)

    # (8) late-round summary
    ax = fig.add_subplot(gs[2, 1])
    ax.axis("off")
    lines = [f"LATE ROUNDS (through Week {last_week})", "-" * 32]
    if n_weeks:
        show = list(range(max(0, n_weeks - 6), n_weeks))  # last 6 weeks
        for w in show:
            i = n0 + w
            prev = float(Y[:i].max()) if i else float("-inf")
            flag = "UP" if Y[i] > prev + 1e-12 else "—"
            lines.append(f"W{w+1:02d}  y={fmt(float(Y[i])):>10s}  [{flag}]")
        lines.append("")
        lines.append(f"Incumbent: y={fmt(fb)}")
        lines.append(f"x=[{', '.join(fmt(v) for v in best_x)}]")
    else:
        lines.append("No weekly queries yet.")
    ax.text(0.0, 1.0, "\n".join(lines), va="top", ha="left", fontsize=9.5,
            family="monospace", transform=ax.transAxes)

    # (9) best-so-far history
    ax = fig.add_subplot(gs[2, 2])
    running = np.maximum.accumulate(Y)
    ax.plot(idx, Y, "o-", color="#888", ms=3, label="y per query")
    ax.plot(idx, running, color="green", lw=2, label="best so far")
    ax.axvline(n0 - 0.5, ls=":", color="black", alpha=0.5)
    for w in range(n_weeks):
        i = n0 + w
        mk, col = WEEK_MARKERS[w % len(WEEK_MARKERS)]
        ax.scatter([i], [Y[i]], marker=mk, c=col, s=70, zorder=5)
    ax.set_title("(9) Observation history (markers = weekly)", fontsize=11, fontweight="bold")
    ax.set_xlabel("observation #")
    ax.set_ylabel("y")
    ax.legend(fontsize=7)
    ax.grid(alpha=0.25)

    out = DATA_ROOT / f"function_{fn}" / f"analysis_F{fn}.png"
    fig.savefig(out, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"F{fn}: saved {out.relative_to(ROOT)} | n={len(Y)} weeks={n_weeks} best={fmt(fb)}")


if __name__ == "__main__":
    for fn in range(1, 9):
        make_figure(fn)
    print("All analysis figures done.")
