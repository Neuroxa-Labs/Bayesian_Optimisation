"""Comprehensive per-function BBO analysis figures (one PNG per function).

Each figure has 9 panels: observed Y values, kernel length scales, strategy/GP
config, GP mean / uncertainty / acquisition heatmaps over the two most
sensitive dimensions, a 1-D sensitivity slice, the Week 1 -> Week 2 decision,
and the observation history. English labels, high resolution, spaced layout.
"""
import warnings
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.stats import norm
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel as C
from sklearn.gaussian_process.kernels import Matern, WhiteKernel

warnings.filterwarnings("ignore")
ROOT = Path(__file__).parent

CFG = {
    1: dict(dim=2, n=10, a=1e-12, nu=0.5, white=False, m="UNC", k=None),
    2: dict(dim=2, n=10, a=1e-8, nu=2.5, white=True, m="EI", k=None),
    3: dict(dim=3, n=15, a=1e-6, nu=1.5, white=False, m="UCB", k=2.576),
    4: dict(dim=4, n=30, a=1e-4, nu=2.5, white=False, m="UCB", k=3.0),
    5: dict(dim=4, n=20, a=1e-6, nu=2.5, white=False, m="UCB", k=1.0),
    6: dict(dim=5, n=20, a=1e-6, nu=2.5, white=False, m="EI", k=None),
    7: dict(dim=6, n=30, a=1e-6, nu=2.5, white=False, m="EI", k=None),
    8: dict(dim=8, n=40, a=1e-5, nu=1.5, white=False, m="UCB", k=2.576),
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

# Real-world framing: goal / what x and y mean / why this acquisition
STORY = {
    1: ("Locate a hidden radiation source on a 2-D map.",
        "x = (position); y = counter reading. Sharp, sparse peak: almost everywhere reads 0.",
        "UNCERTAINTY: no signal yet, so scan the least-explored gaps until a non-zero reading appears."),
    2: ("Tune a noisy machine-learning model's log-likelihood.",
        "x = 2 settings; y = noisy log-likelihood (higher is better).",
        "EI + White kernel: noise-robust; balances probability and size of improvement."),
    3: ("Minimise adverse drug reactions by mixing 3 components.",
        "x = component ratios; y = -(side effect). y near 0 = good.",
        "UCB k=2.576: 15 points are sparse in 3-D, keep exploring while tracking promising regions."),
    4: ("Optimise warehouse item placement (4 factors).",
        "x = 4 placement factors; y = efficiency score.",
        "UCB k=3.0 (highest): many local optima, so explore widely before committing."),
    5: ("Maximise chemical reaction yield (single broad peak).",
        "x = 4 process settings; y = yield.",
        "UCB explore->exploit: once the signal is found, climb the peak aggressively."),
    6: ("Find the best cake recipe (5 ingredients).",
        "x = 5 ingredient amounts; y = -(badness). y near 0 = good.",
        "EI: balanced improvement search in 5-D toward 0."),
    7: ("Tune 6 hyperparameters of an ML model.",
        "x = 6 hyperparameters; y = validation score.",
        "EI: measured explore/exploit balance in high dimension."),
    8: ("Optimise an 8-parameter ML model.",
        "x = 8 parameters; y = score.",
        "UCB k=2.576: huge 8-D space, keep broad exploration while tracking high-score regions."),
}

WK1_X = {
    1: [0.196386, 0.970701], 2: [0.694835, 0.926564],
    3: [0.492581, 0.020000, 0.648182],
    4: [0.403955, 0.407959, 0.338079, 0.437525],
    5: [0.224189, 0.846480, 0.980000, 0.980000],
    6: [0.465618, 0.243059, 0.577549, 0.980000, 0.020000],
    7: [0.020000, 0.491672, 0.247422, 0.217425, 0.377957, 0.746469],
    8: [0.020000, 0.020000, 0.188724, 0.038786, 0.403935, 0.486768, 0.020000, 0.893085],
}
WK1_Y = {
    1: 4.846319514951174e-214, 2: 0.4898172329737405, 3: -0.16845658599408186,
    4: 0.2574881015382826, 5: 2497.315519875975, 6: -0.47754451531418857,
    7: 1.4506493171190014, 8: 9.795587212017,
}
WK2_X = {
    1: [0.980000, 0.035116], 2: [0.734317, 0.926564],
    3: [0.492581, 0.020000, 0.020000],
    4: [0.460385, 0.434644, 0.203056, 0.431758],
    5: [0.074189, 0.696480, 0.980000, 0.980000],
    6: [0.517086, 0.282151, 0.771390, 0.980000, 0.207535],
    7: [0.020000, 0.491672, 0.247422, 0.214597, 0.377195, 0.806097],
    8: [0.020000, 0.020000, 0.020000, 0.038786, 0.403935, 0.980000, 0.020000, 0.893085],
}


def fit(X, Y, c):
    var = np.var(X, axis=0); var[var < 1e-6] = 0.1
    mk = Matern(length_scale=np.sqrt(var), length_scale_bounds=(1e-2, 10.0), nu=c["nu"])
    k = C(1.0, (1e-3, 1e3)) * mk
    if c["white"]:
        k = k + WhiteKernel(1e-3, (1e-8, 1e-1))
    gp = GaussianProcessRegressor(kernel=k, alpha=c["a"], n_restarts_optimizer=10,
                                  normalize_y=True, random_state=42)
    gp.fit(X, Y)
    return gp


def length_scales(gp):
    for k, v in gp.kernel_.get_params(deep=True).items():
        if k.endswith("length_scale") and not k.endswith("bounds"):
            return np.atleast_1d(np.asarray(v, dtype=float))
    return None


def acq_grid(gp, G, m, k, fb):
    mu, sg = gp.predict(G, return_std=True)
    if m == "UCB":
        return mu + (k or 0.0) * sg
    if m == "UNC":
        return sg
    s = np.maximum(sg, 1e-12); z = (mu - fb) / s
    return np.maximum((mu - fb) * norm.cdf(z) + s * norm.pdf(z), 0.0)


def fmt(v):
    a = abs(v)
    if a != 0 and (a < 1e-3 or a >= 1e4):
        return f"{v:.2e}"
    return f"{v:.3f}"


def make_figure(fn):
    c = CFG[fn]
    dim, n0 = c["dim"], c["n"]
    X = np.load(ROOT / f"function_{fn}" / "initial_inputs.npy")[: n0 + 1]
    Y = np.load(ROOT / f"function_{fn}" / "initial_outputs.npy")[: n0 + 1]
    gp = fit(X, Y, c)
    ls = length_scales(gp)
    fb = float(Y.max())
    best_i = int(np.argmax(Y))
    best_x = X[best_i]
    w1x, w1y, w2x = np.array(WK1_X[fn]), WK1_Y[fn], np.array(WK2_X[fn])

    # two most sensitive dims (smallest length scale)
    order = np.argsort(ls)
    d0, d1 = (order[0], order[1]) if dim >= 2 else (0, 0)

    fig = plt.figure(figsize=(20, 13.5))
    gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.42, wspace=0.28,
                           left=0.05, right=0.97, top=0.9, bottom=0.06)
    fig.suptitle(f"F{fn}  -  {NAME[fn]}  ({dim}-D)\nLearn from scratch: Data -> GP -> Acquisition -> Week 1 -> Week 2",
                 fontsize=17, fontweight="bold")

    # Panel 1: Y values bar chart
    ax = fig.add_subplot(gs[0, 0])
    idx = np.arange(len(Y))
    colors = ["#7fbf7f" if y >= np.percentile(Y, 66) else
              ("#f2b56b" if y >= np.percentile(Y, 33) else "#e06666") for y in Y]
    colors[best_i] = "#3b7dd8"
    colors[-1] = "#9b59b6"  # week 1 point (last)
    ax.bar(idx, Y, color=colors)
    ax.axhline(fb, ls="--", color="green", lw=1, alpha=0.6)
    ax.set_title("(1) Observed y values\n(blue=best, purple=Week1)", fontsize=11, fontweight="bold")
    ax.set_xlabel("observation #"); ax.set_ylabel("y")
    ax.grid(alpha=0.25, axis="y")

    # Panel 2: kernel length scales
    ax = fig.add_subplot(gs[0, 1])
    lsc = ["#e06666" if v >= 4.5 else ("#f2b56b" if v <= 0.5 else "#7fbf7f") for v in ls]
    ax.bar([f"x{i+1}" for i in range(dim)], ls, color=lsc)
    ax.axhline(4.5, ls="--", color="red", lw=1, label="degenerate (>=4.5)")
    ax.axhline(0.5, ls=":", color="orange", lw=1, label="sensitive (<=0.5)")
    for i, v in enumerate(ls):
        ax.text(i, v, f"{v:.2f}", ha="center", va="bottom", fontsize=8)
    ax.set_title("(2) Kernel length scales\n(how the GP sees each dimension)", fontsize=11, fontweight="bold")
    ax.set_ylabel("length scale"); ax.legend(fontsize=7); ax.grid(alpha=0.25, axis="y")

    # Panel 3: strategy / GP config text
    ax = fig.add_subplot(gs[0, 2]); ax.axis("off")
    goal, mean_, why = STORY[fn]
    deg = [i + 1 for i in range(dim) if ls[i] >= 4.5]
    sens = [i + 1 for i in range(dim) if ls[i] <= 0.5]
    txt = (f"STRATEGY & GP CONFIG\n"
           f"--------------------------------\n"
           f"Real world : {goal}\n"
           f"Meaning    : {mean_}\n\n"
           f"GP kernel  : Matern nu={c['nu']}, alpha={c['a']:g}\n"
           f"{'White kernel for noise' if c['white'] else ''}\n"
           f"Acquisition: {c['m']}" + (f" (k={c['k']})" if c['k'] else "") + "\n"
           f"Why        : {why}\n\n"
           f"Current best y = {fmt(fb)}\n"
           f"at x = [{', '.join(fmt(v) for v in best_x)}]\n\n"
           f"Degenerate dims (ignored): {deg if deg else 'none'}\n"
           f"Sensitive dims (careful) : {sens if sens else 'none'}")
    ax.text(0.0, 1.0, txt, va="top", ha="left", fontsize=9.0, family="monospace",
            transform=ax.transAxes, wrap=True)

    # Heatmap grid over (d0, d1)
    res = 60
    g = np.linspace(0.02, 0.98, res)
    G1, G2 = np.meshgrid(g, g)
    base = np.tile(best_x, (res * res, 1)).astype(float)
    base[:, d0] = G1.ravel(); base[:, d1] = G2.ravel()
    mu_g, sg_g = gp.predict(base, return_std=True)
    acq_g = acq_grid(gp, base, c["m"], c["k"], fb)

    def overlay(ax):
        ax.scatter(X[:, d0], X[:, d1], c="white", edgecolors="black", s=28, label="data", zorder=3)
        ax.scatter([best_x[d0]], [best_x[d1]], marker="*", c="gold", edgecolors="black",
                   s=260, label="best", zorder=5)
        ax.scatter([w1x[d0]], [w1x[d1]], marker="X", c="red", s=130, label="Week1", zorder=5)
        ax.scatter([w2x[d0]], [w2x[d1]], marker="^", c="cyan", edgecolors="black",
                   s=150, label="Week2", zorder=5)
        ax.set_xlabel(f"x{d0+1}"); ax.set_ylabel(f"x{d1+1}")

    titles = [("(4) GP mean (prediction)", mu_g, "viridis"),
              ("(5) GP uncertainty (sigma)", sg_g, "magma"),
              ("(6) Acquisition surface", acq_g, "cividis")]
    for j, (ttl, Z, cmap) in enumerate(titles):
        ax = fig.add_subplot(gs[1, j])
        cf = ax.contourf(G1, G2, Z.reshape(res, res), levels=25, cmap=cmap)
        plt.colorbar(cf, ax=ax, fraction=0.046, pad=0.04)
        overlay(ax)
        extra = f"  (other dims fixed at best)" if dim > 2 else ""
        ax.set_title(ttl + f"\nx{d0+1} vs x{d1+1}" + extra, fontsize=10.5, fontweight="bold")
        if j == 0:
            ax.legend(fontsize=7, loc="upper right")

    # Panel 7: sensitivity slice along most sensitive dim d0
    ax = fig.add_subplot(gs[2, 0])
    line = np.tile(best_x, (200, 1)).astype(float)
    gg = np.linspace(0.02, 0.98, 200)
    line[:, d0] = gg
    mu_l, sg_l = gp.predict(line, return_std=True)
    ax.plot(gg, mu_l, color="#3b7dd8", label="GP mean")
    ax.fill_between(gg, mu_l - 1.96 * sg_l, mu_l + 1.96 * sg_l, color="#3b7dd8", alpha=0.18,
                    label="95% band")
    ax.axvline(best_x[d0], ls="--", color="gold", label="best")
    ax.axvline(w1x[d0], ls=":", color="red", label="Week1")
    ax.axvline(w2x[d0], ls="-.", color="cyan", label="Week2")
    ax.set_title(f"(7) Sensitivity along x{d0+1}\n(most sensitive dim)", fontsize=11, fontweight="bold")
    ax.set_xlabel(f"x{d0+1}"); ax.set_ylabel("GP mean y"); ax.legend(fontsize=7); ax.grid(alpha=0.25)

    # Panel 8: Week1 -> Week2 decision text
    ax = fig.add_subplot(gs[2, 1]); ax.axis("off")
    improved = w1y > float(Y[:-1].max())
    mu_w2, sg_w2 = gp.predict(w2x.reshape(1, -1), return_std=True)
    txt2 = (f"WEEK 1 -> WEEK 2 DECISION\n"
            f"--------------------------------\n"
            f"Week 1 sent : [{', '.join(fmt(v) for v in w1x)}]\n"
            f"Week 1 got  : y = {fmt(w1y)}\n"
            f"Result      : {'IMPROVED' if improved else 'did not improve'} "
            f"(prev best {fmt(float(Y[:-1].max()))})\n\n"
            f"Week 2 plan : [{', '.join(fmt(v) for v in w2x)}]\n"
            f"GP expects  : mu={fmt(float(mu_w2[0]))}, sigma={fmt(float(sg_w2[0]))}\n\n"
            f"Reasoning   :\n{STORY[fn][2]}")
    ax.text(0.0, 1.0, txt2, va="top", ha="left", fontsize=9.2, family="monospace",
            transform=ax.transAxes, wrap=True)

    # Panel 9: observation history
    ax = fig.add_subplot(gs[2, 2])
    running = np.maximum.accumulate(Y)
    ax.plot(idx, Y, "o-", color="#888", ms=4, label="y per query")
    ax.plot(idx, running, color="green", lw=2, label="best so far")
    ax.scatter([len(Y) - 1], [Y[-1]], marker="X", c="red", s=120, zorder=5, label="Week1 result")
    ax.set_title("(9) Observation history", fontsize=11, fontweight="bold")
    ax.set_xlabel("observation #"); ax.set_ylabel("y"); ax.legend(fontsize=7); ax.grid(alpha=0.25)

    out = ROOT / f"function_{fn}" / f"analysis_F{fn}.png"
    fig.savefig(out, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"F{fn}: saved {out.relative_to(ROOT)} | best={fmt(fb)} | W2 mu={fmt(float(mu_w2[0]))}")


for fn in range(1, 9):
    make_figure(fn)
print("All analysis figures done.")
