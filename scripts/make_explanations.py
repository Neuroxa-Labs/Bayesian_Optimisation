"""Generate EXPLANATION_F*.md for each function from the full .npy history."""
from __future__ import annotations

import warnings
from pathlib import Path

import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel as C
from sklearn.gaussian_process.kernels import Matern, WhiteKernel

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = ROOT / "data"

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
NARR = {
    1: dict(
        world="You are sweeping a 2-D field to locate a hidden radioactive source with a Geiger counter.",
        x="the (x1, x2) position on the map",
        y="the counter reading (higher = closer to the source)",
        goal="find the position with the strongest reading (the hidden source).",
        why="Almost everywhere reads ~0. After a long null phase near (0.73, 0.73), a peer-supported "
            "signal lobe near (0.64, 0.68) produced measurable readings; late weeks stay inside that lobe.",
        lesson="A zero is elimination, not proof the source is elsewhere. Once a real signal cluster "
               "appears, exploit it; do not keep polishing a null basin.",
    ),
    2: dict(
        world="You are tuning a machine-learning model whose validation log-likelihood is measured with noise.",
        x="2 model settings",
        y="a noisy log-likelihood score (higher = better)",
        goal="maximise the (noisy) log-likelihood.",
        why="EI with a White noise kernel. The historical peak (~0.777) sits on a sharp ridge; "
            "late returns often land ~0.54 when the step is slightly off.",
        lesson="Treat noise as noise, but also respect razor ridges: hard-return toward the incumbent "
               "when neighbour steps keep missing.",
    ),
    3: dict(
        world="A drug-development lab mixes 3 chemical components and measures a side-effect score.",
        x="the 3 component ratios (x1, x2, x3)",
        y="the negative side effect (y near 0 = safe, very negative = harmful)",
        goal="minimise side effects, i.e. push y as close to 0 as possible (we maximise y = -(side effect)).",
        why="x3 is sensitive; keep it locked in a safe band and take local steps around the -0.011 neighbourhood.",
        lesson="Small length-scale dimensions need small steps. Boundary jumps early on taught that lesson.",
    ),
    4: dict(
        world="You are placing items in a warehouse; 4 factors control how efficient the layout is.",
        x="4 placement factors",
        y="an efficiency score (higher = better)",
        goal="maximise warehouse efficiency.",
        why="After early exploration mapped a useful basin, late weeks use tight trust-region micro-steps.",
        lesson="Multimodal spaces need breadth first, then local climb once a basin proves real.",
    ),
    5: dict(
        world="You are optimising a chemical reaction's yield; 4 process settings control the output.",
        x="4 process settings",
        y="the reaction yield (higher = better)",
        goal="maximise the yield along a ridge.",
        why="Lock the high x2–x4 face and climb x1 (log-y GP fit). This produced a sustained yield run into the late weeks.",
        lesson="Exploitation must keep producing NEW information along the sensitive axis — not re-query the same point.",
    ),
    6: dict(
        world="You are perfecting a cake recipe defined by 5 ingredient amounts; a judge scores how bad it is.",
        x="5 ingredient amounts",
        y="the negative badness (y near 0 = great cake)",
        goal="minimise badness, i.e. push y toward 0 (we maximise y = -(badness)).",
        why="A sharp interior basin. Week 10 set the incumbent; a small off-centroid step collapsed the score — "
            "later weeks hard-return toward that centroid.",
        lesson="Nearby is not enough on a sharp basin. After a failed neighbour, return hard to the proven mode.",
    ),
    7: dict(
        world="You are tuning 6 hyperparameters of a machine-learning model.",
        x="6 hyperparameters",
        y="a validation score (higher = better)",
        goal="maximise the validation score.",
        why="Local EI around the late peak; move ARD-sensitive axes and leave flat ones alone.",
        lesson="In 6-D, patience and small local gains accumulate better than global jumps late in the budget.",
    ),
    8: dict(
        world="You are optimising a complex ML model with 8 parameters.",
        x="8 parameters",
        y="a model score (higher = better)",
        goal="maximise the score in a large 8-D space.",
        why="Expect slow late gains. Trust-region steps on ARD-sensitive dims with a boundary penalty.",
        lesson="In 8-D, steady micro-improvements are success; do not chase edge uncertainty artefacts.",
    ),
}


def fit(X, Y, c):
    y = Y.astype(float).copy()
    if y.max() > 100:
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


def lscales(gp):
    for k, v in gp.kernel_.get_params(deep=True).items():
        if k.endswith("length_scale") and not k.endswith("bounds"):
            return np.atleast_1d(np.asarray(v, dtype=float))
    return np.ones(1)


def f(v):
    a = abs(float(v))
    return f"{v:.3e}" if (a != 0 and (a < 1e-3 or a >= 1e4)) else f"{float(v):.4f}"


def vec(x):
    return "[" + ", ".join(f(v) for v in x) + "]"


for fn, c in CFG.items():
    dim, n0 = c["dim"], c["n"]
    X = np.load(DATA_ROOT / f"function_{fn}" / "initial_inputs.npy").astype(float)
    Y = np.load(DATA_ROOT / f"function_{fn}" / "initial_outputs.npy").astype(float).ravel()
    n_weeks = max(0, len(Y) - n0)
    gp = fit(X, Y, c)
    ls = lscales(gp)
    cur_best = float(Y.max())
    bi = int(np.argmax(Y))
    bx = X[bi]
    seed_best = float(Y[:n0].max()) if n0 else float("nan")
    nr = NARR[fn]

    order = np.argsort(Y)[::-1]
    rows = []
    for r in list(order[:3]) + list(order[-2:]):
        tag = "BEST" if r == bi else ("WORST" if r == order[-1] else "")
        rows.append("| " + " | ".join([str(r + 1)] + [f(v) for v in X[r]] + [f(Y[r]), tag]) + " |")

    ls_lines = []
    for i in range(dim):
        v = float(ls[i])
        if v >= 4.5:
            tag = "**degenerate** — little effect (GP effectively locks it)"
        elif v <= 0.5:
            tag = "**very sensitive** — small changes move y a lot"
        else:
            tag = "moderate influence"
        ls_lines.append(f"- `x{i+1}`: length-scale = {f(v)} → {tag}")

    xheaders = " | ".join(f"x{i+1}" for i in range(dim))
    week_sections = []
    summary_rows = [f"| Best before W1 | {f(seed_best)} |"]
    for w in range(n_weeks):
        i = n0 + w
        prev = float(Y[:i].max())
        improved = float(Y[i]) > prev + 1e-12
        week_sections.append(
            f"## {5 + w}. Week {w + 1} — what we sent and what happened\n\n"
            f"- **Sent:** x = {vec(X[i])}\n"
            f"- **Received:** y = {f(Y[i])}\n"
            f"- **Outcome:** "
            + (
                f"**IMPROVED** over the previous best ({f(prev)})"
                if improved
                else f"did **not** improve over the previous best ({f(prev)})"
            )
            + ".\n"
        )
        summary_rows.append(
            f"| Week {w + 1} result | {f(Y[i])} "
            f"({'improved' if improved else 'no improvement'}) |"
        )
    summary_rows.append(f"| Current best (through Week {n_weeks}) | {f(cur_best)} |")

    acq = c["m"] + (f" (k={c['k']})" if c["k"] else "")
    doc = f"""# F{fn} — {NAME[fn]} ({dim}-D)

## 1. The big picture

**Real world:** {nr['world']}

- **x** = {nr['x']}
- **y** = {nr['y']}
- **Goal:** {nr['goal']}
- **Constraint:** one query per function per week (Stage 2 budget).

This is a **black box**: we never see the formula, only input → output. Bayesian optimisation
(GP + acquisition) is designed for exactly that setting.

## 2. Data so far ({n0} seed points + {n_weeks} weekly queries = {len(Y)} observations)

| # | {xheaders} | y | note |
|---|{"|".join(["---"] * dim)}|---|---|
{chr(10).join(rows)}

- **Best so far:** y = {f(cur_best)} at x = {vec(bx)}

## 3. What the GP learned (ARD length scales)

{chr(10).join(ls_lines)}

## 4. Acquisition / late policy: **{acq}**

{nr['why']}

{chr(10).join(week_sections)}
## {5 + n_weeks}. The lesson

{nr['lesson']}

## {6 + n_weeks}. Summary

| | Value |
|---|---|
| Real-world task | {NAME[fn]} |
| Dimensions | {dim} |
| Acquisition | {acq} (Matérn ν={c['nu']}) |
{chr(10).join(summary_rows)}

*See `analysis_F{fn}.png` in this folder for the 9-panel visual analysis (regenerated through Week {n_weeks}).*
"""
    out = DATA_ROOT / f"function_{fn}" / f"EXPLANATION_F{fn}.md"
    out.write_text(doc, encoding="utf-8")
    print(f"F{fn}: wrote {out.relative_to(ROOT)} (weeks={n_weeks})")

print("All explanation docs done.")
