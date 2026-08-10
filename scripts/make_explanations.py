"""Generate a detailed, learn-from-scratch English explanation (EXPLANATION_F*.md)
for each function, grounded in the real fitted-GP numbers and the Week 1 / Week 2 data."""
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
    1: dict(dim=2, n=10, a=1e-12, nu=0.5, white=False, m="COVERAGE", k=None),
    2: dict(dim=2, n=10, a=1e-8, nu=2.5, white=True, m="EI", k=None),
    3: dict(dim=3, n=15, a=1e-6, nu=1.5, white=False, m="UCB", k=2.576),
    4: dict(dim=4, n=30, a=1e-4, nu=2.5, white=False, m="UCB", k=3.0),
    5: dict(dim=4, n=20, a=1e-6, nu=2.5, white=False, m="UCB", k=1.0),
    6: dict(dim=5, n=20, a=1e-6, nu=2.5, white=False, m="EI", k=None),
    7: dict(dim=6, n=30, a=1e-6, nu=2.5, white=False, m="EI", k=None),
    8: dict(dim=8, n=40, a=1e-5, nu=1.5, white=False, m="UCB", k=2.576),
}
NAME = {1: "Radiation Source Detection", 2: "Noisy ML Log-Likelihood",
        3: "Drug Discovery - Adverse Reactions", 4: "Warehouse Placement",
        5: "Chemical Yield Optimisation", 6: "Cake Recipe Optimisation",
        7: "ML Hyperparameter Tuning", 8: "8-Parameter ML Model Optimisation"}

NARR = {
    1: dict(world="You are sweeping a 2-D field to locate a hidden radioactive source with a Geiger counter.",
            x="the (x1, x2) position on the map", y="the counter reading (higher = closer to the source)",
            goal="find the position with the strongest reading (the hidden source).",
            why="The peak is sharp and sparse: almost every reading is 0. With no signal, use **coverage-based exploration** (farthest from existing points) plus a boundary penalty - GP uncertainty at box edges is misleading.",
            lesson="A zero is not failure - it is elimination. Avoid boundary artefacts; scan the largest interior gaps. nu=0.5 models a rough, spiky surface."),
    2: dict(world="You are tuning a machine-learning model whose validation log-likelihood is measured with noise.",
            x="2 model settings", y="a noisy log-likelihood score (higher = better)",
            goal="maximise the (noisy) log-likelihood.",
            why="Because the signal is noisy, a single low reading does not mean a region is bad. **EI with a White noise kernel** is robust: it weighs both the probability and the size of an improvement, and the White kernel absorbs measurement noise so the GP is not fooled by it.",
            lesson="Treat noise as noise. Do not abandon a promising region after one unlucky sample - keep sampling near the known-good area."),
    3: dict(world="A drug-development lab mixes 3 chemical components and measures a side-effect score.",
            x="the 3 component ratios (x1, x2, x3)", y="the negative side effect (y near 0 = safe, very negative = harmful)",
            goal="minimise side effects, i.e. push y as close to 0 as possible (we maximise y = -(side effect)).",
            why="With only 15 points in 3-D, the space is sparse. **UCB k=2.576** with **narrow bounds** on sensitive dims (x3 ls=0.07: search ±0.15 around best) keeps exploration local after Week 1's boundary jump backfired.",
            lesson="Small length-scale dimensions are sensitive - take small steps in them. When a big jump backfires, narrow the search box around the best point instead of hugging box edges."),
    4: dict(world="You are placing items in a warehouse; 4 factors control how efficient the layout is.",
            x="4 placement factors", y="an efficiency score (higher = better)",
            goal="maximise warehouse efficiency.",
            why="The landscape is **multimodal** (many local optima), so committing early is dangerous. We use the **highest exploration setting (UCB k=3.0)** to cover the space widely and avoid getting trapped in a poor basin.",
            lesson="In multimodal spaces, breadth beats greed early on. Week 1 jumped from a negative region to a positive one precisely because exploration was prioritised."),
    5: dict(world="You are optimising a chemical reaction's yield; 4 process settings control the output.",
            x="4 process settings", y="the reaction yield (higher = better)",
            goal="maximise the yield (a single broad peak).",
            why="This function has one broad peak, so the strategy is **find the signal, then exploit**. Once the best value crossed the signal threshold, the model dropped to a low-k UCB and now climbs the peak. An **anti-duplicate guard** stops it re-sending a point we already measured: instead it does a local UCB search around the peak.",
            lesson="Exploitation must keep producing NEW information. Re-querying the exact best point wastes a week - so local search around the peak (with the same acquisition) is the right way to climb."),
    6: dict(world="You are perfecting a cake recipe defined by 5 ingredient amounts; a judge scores how bad it is.",
            x="5 ingredient amounts", y="the negative badness (y near 0 = great cake)",
            goal="minimise badness, i.e. push y toward 0 (we maximise y = -(badness)).",
            why="In 5-D a balanced search pays off. **EI** gives a measured explore/exploit trade-off and steadily nudges toward 0 without over-committing to one region too soon.",
            lesson="In medium dimension, steady incremental gains are the norm. EI's balance avoids both blind wandering and premature exploitation."),
    7: dict(world="You are tuning 6 hyperparameters of a machine-learning model.",
            x="6 hyperparameters", y="a validation score (higher = better)",
            goal="maximise the validation score.",
            why="High dimension means the space is large and easy to over-commit in. **EI** keeps a careful balance; jumping to exploitation too early would risk locking onto a local optimum before the space is mapped.",
            lesson="In 6-D, patience matters. Small, reliable improvements accumulate; aggressive exploitation is a trap until more of the space is known."),
    8: dict(world="You are optimising a complex ML model with 8 parameters.",
            x="8 parameters", y="a model score (higher = better)",
            goal="maximise the score in a large 8-D space.",
            why="The 8-D space is enormous. **UCB k=2.576** plus a **boundary penalty** keeps exploration alive but discourages edge-hugging points (Week 2 had 1 dim on boundary vs 5 before). nu=1.5 is a mid-smoothness compromise.",
            lesson="In very high dimension, expect slow steady progress. Penalise boundary artefacts so UCB does not waste queries on misleading GP uncertainty at box edges."),
}

WK1_X = {1: [0.196386, 0.970701], 2: [0.694835, 0.926564], 3: [0.492581, 0.020000, 0.648182],
         4: [0.403955, 0.407959, 0.338079, 0.437525], 5: [0.224189, 0.846480, 0.980000, 0.980000],
         6: [0.465618, 0.243059, 0.577549, 0.980000, 0.020000],
         7: [0.020000, 0.491672, 0.247422, 0.217425, 0.377957, 0.746469],
         8: [0.020000, 0.020000, 0.188724, 0.038786, 0.403935, 0.486768, 0.020000, 0.893085]}
WK1_Y = {1: 4.846319514951174e-214, 2: 0.4898172329737405, 3: -0.16845658599408186,
         4: 0.2574881015382826, 5: 2497.315519875975, 6: -0.47754451531418857,
         7: 1.4506493171190014, 8: 9.795587212017}
WK2_X = {1: [0.421062, 0.463562], 2: [0.734317, 0.926564], 3: [0.492581, 0.691593, 0.401268],
         4: [0.460385, 0.434644, 0.203056, 0.431758], 5: [0.074189, 0.696480, 0.980000, 0.980000],
         6: [0.517086, 0.282151, 0.771390, 0.980000, 0.207535],
         7: [0.020000, 0.491672, 0.247422, 0.214597, 0.377195, 0.806097],
         8: [0.070000, 0.070000, 0.020000, 0.038786, 0.403935, 0.070000, 0.070000, 0.893085]}
WK2_Y = {1: -0.006627379464825304, 2: 0.5706060535359335, 3: -0.020302412806162906,
         4: -3.305599024194517, 5: 1811.05681696222, 6: -0.5782346356754113,
         7: 1.2983310369966137, 8: 9.637407822369}
WK3_X = {1: [0.070000, 0.669525], 2: [0.718765, 0.926564], 3: [0.642581, 0.691593, 0.478715],
         4: [0.343955, 0.453869, 0.398079, 0.433861], 5: [0.150000, 0.926480, 0.980000, 0.980000],
         6: [0.524058, 0.360869, 0.413794, 0.897694, 0.020000],
         7: [0.070000, 0.491672, 0.247422, 0.167429, 0.353878, 0.715603],
         8: [0.070000, 0.070000, 0.020000, 0.038786, 0.403935, 0.930000, 0.020000, 0.893085]}
WK3_Y = {1: -1.7640587689392826e-130, 2: 0.6022360650843126, 3: -0.02269443855307699,
         4: -0.12619162666369688, 5: 3108.4878561302053, 6: -0.5376870203763128,
         7: 1.5253347319738353, 8: 9.606407822369}
WK4_X = {1: [0.661537, 0.436390], 2: [0.700000, 0.020000],
         3: [0.592581, 0.771593, 0.436323], 4: [0.414097, 0.385945, 0.378079, 0.441536],
         5: [0.380000, 0.980000, 0.980000, 0.980000],
         6: [0.365618, 0.143059, 0.477549, 0.930000, 0.120000],
         7: [0.070000, 0.431672, 0.307422, 0.158929, 0.347393, 0.672154],
         8: [0.020000, 0.020000, 0.188184, 0.038786, 0.403935, 0.486122, 0.020000, 0.893085]}
WK4_Y = {1: 3.21298272257291e-28, 2: 0.6598602814677763, 3: -0.043381912559889324,
         4: 0.16598412185782196, 5: 3743.829067735118, 6: -0.6062467956245956,
         7: 1.8574559098912007, 8: 9.795759089917}
WK5_X = {1: [0.662502, 0.070000], 2: [0.717869, 0.020000],
         3: [0.492581, 0.691593, 0.401000], 4: [0.425820, 0.439559, 0.381148, 0.436983],
         5: [0.280000, 0.980000, 0.980000, 0.980000],
         6: [0.430000, 0.240000, 0.580000, 0.720000, 0.120000],
         7: [0.070000, 0.376096, 0.307422, 0.107492, 0.323741, 0.648355],
         8: [0.126155, 0.070000, 0.224493, 0.038786, 0.403935, 0.497424, 0.228063, 0.893085]}
WK5_Y = {1: -4.778494662600997e-128, 2: 0.7766450728516721, 3: -0.022346711262055334,
         4: 0.24027427340052343, 5: 3692.519989512911, 6: -0.2654080647396229,
         7: 1.8161306404666622, 8: 9.864471173458}
WK6_X = {1: [0.755000, 0.710000], 2: [0.750000, 0.020000],
         3: [0.492581, 0.691593, 0.401000], 4: [0.400838, 0.413498, 0.376688, 0.406083],
         5: [0.360000, 0.980000, 0.980000, 0.980000],
         6: [0.440000, 0.250000, 0.590000, 0.730000, 0.130000],
         7: [0.070000, 0.416628, 0.307422, 0.136908, 0.324592, 0.654726],
         8: [0.070000, 0.272853, 0.209858, 0.038786, 0.403935, 0.545195, 0.198456, 0.893085]}
WK6_Y = {1: -1.2733719774833445e-16, 2: 0.40347007739097895, 3: -0.011366393913517245,
         4: 0.469508628918597, 5: 3729.8366843702797, 6: -0.24039734108674735,
         7: 1.8471407406042062, 8: 9.862535706371}
WK7_X = {1: [0.760000, 0.760000], 2: [0.720000, 0.020000],
         3: [0.485000, 0.685000, 0.401000], 4: [0.395000, 0.420000, 0.380000, 0.410000],
         5: [0.380000, 0.980000, 0.980000, 0.980000],
         6: [0.445000, 0.255000, 0.595000, 0.735000, 0.135000],
         7: [0.070000, 0.435000, 0.310000, 0.160000, 0.350000, 0.675000],
         8: [0.130000, 0.070000, 0.220000, 0.040000, 0.400000, 0.500000, 0.230000, 0.890000]}
WK7_Y = {1: 5.183539428400652e-25, 2: 0.5073917805634148, 3: -0.014465733476312878,
         4: 0.4636989224185055, 5: 3743.829067735118, 6: -0.26724660706706216,
         7: 1.8468357700520182, 8: 9.86519}


def fit(X, Y, c):
    var = np.var(X, axis=0); var[var < 1e-6] = 0.1
    mk = Matern(length_scale=np.sqrt(var), length_scale_bounds=(1e-2, 10.0), nu=c["nu"])
    k = C(1.0, (1e-3, 1e3)) * mk
    if c["white"]:
        k = k + WhiteKernel(1e-3, (1e-8, 1e-1))
    gp = GaussianProcessRegressor(kernel=k, alpha=c["a"], n_restarts_optimizer=10,
                                  normalize_y=True, random_state=42)
    gp.fit(X, Y); return gp


def lscales(gp):
    for k, v in gp.kernel_.get_params(deep=True).items():
        if k.endswith("length_scale") and not k.endswith("bounds"):
            return np.atleast_1d(np.asarray(v, dtype=float))


def f(v):
    a = abs(v)
    return f"{v:.3e}" if (a != 0 and (a < 1e-3 or a >= 1e4)) else f"{v:.4f}"


def vec(x):
    return "[" + ", ".join(f(v) for v in x) + "]"


for fn, c in CFG.items():
    dim, n0 = c["dim"], c["n"]
    X = np.load(DATA_ROOT / f"function_{fn}" / "initial_inputs.npy")[: n0 + 7]
    Y = np.load(DATA_ROOT / f"function_{fn}" / "initial_outputs.npy")[: n0 + 7]
    gp = fit(X, Y, c); ls = lscales(gp)
    w1_prev = float(Y[:n0].max()); cur_best = float(Y.max())
    bi = int(np.argmax(Y)); bx = X[bi]
    w1x, w1y = WK1_X[fn], WK1_Y[fn]
    w2x, w2y = WK2_X[fn], WK2_Y[fn]
    w3x, w3y = WK3_X[fn], WK3_Y[fn]
    w4x, w4y = WK4_X[fn], WK4_Y[fn]
    w5x, w5y = WK5_X[fn], WK5_Y[fn]
    w6x, w6y = WK6_X[fn], WK6_Y[fn]
    w7x, w7y = WK7_X[fn], WK7_Y[fn]
    w2_prev = float(Y[: n0 + 1].max())
    w3_prev = float(Y[: n0 + 2].max())
    w4_prev = float(Y[: n0 + 3].max())
    w5_prev = float(Y[: n0 + 4].max())
    w6_prev = float(Y[: n0 + 5].max())
    w7_prev = float(Y[: n0 + 6].max())
    mu4, sg4 = gp.predict(np.asarray(w4x).reshape(1, -1), return_std=True)
    mu5, sg5 = gp.predict(np.asarray(w5x).reshape(1, -1), return_std=True)
    mu6, sg6 = gp.predict(np.asarray(w6x).reshape(1, -1), return_std=True)
    mu7, sg7 = gp.predict(np.asarray(w7x).reshape(1, -1), return_std=True)
    mu4, sg4 = float(mu4[0]), float(sg4[0])
    mu5, sg5 = float(mu5[0]), float(sg5[0])
    mu6, sg6 = float(mu6[0]), float(sg6[0])
    mu7, sg7 = float(mu7[0]), float(sg7[0])
    w1_improved = w1y > w1_prev
    w2_improved = w2y > w2_prev
    w3_improved = w3y > w3_prev
    w4_improved = w4y > w4_prev
    w5_improved = w5y > w5_prev
    w6_improved = w6y > w6_prev
    w7_improved = w7y > w7_prev
    nr = NARR[fn]

    # ranked observations
    order = np.argsort(Y)[::-1]
    rows = []
    for r in list(order[:3]) + list(order[-2:]):
        tag = "BEST" if r == bi else ("WORST" if r == order[-1] else "")
        rows.append(f"| {r+1} | " + " | ".join(f(v) for v in X[r]) + f" | {f(Y[r])} | {tag} |")

    # length-scale interpretation
    ls_lines = []
    for i in range(dim):
        v = ls[i]
        if v >= 4.5:
            tag = "**degenerate** - GP sees little effect from this dimension (it locks it)"
        elif v <= 0.5:
            tag = "**very sensitive** - small changes move y a lot (take small steps)"
        else:
            tag = "moderate influence"
        ls_lines.append(f"- `x{i+1}`: length-scale = {f(v)} -> {tag}")

    xheaders = " | ".join(f"x{i+1}" for i in range(dim))

    doc = f"""# F{fn} - {NAME[fn]} ({dim}-D) - Learn from Scratch

## 1. The big picture: what is the problem?

**Real world:** {nr['world']}

- **x** = {nr['x']}
- **y** = {nr['y']}
- **Goal:** {nr['goal']}
- **Constraint:** every evaluation is expensive - only **one query per week**, ~13 weeks total. Choose wisely.

This is a **black box**: we never see the formula, only "input x -> output y". That is exactly what
Bayesian Optimisation is built for - finding the best of an expensive unknown function in few tries.

## 2. What we were given ({n0} initial points + 7 weekly queries = {len(Y)} observations)

| # | {xheaders} | y | note |
|---|{"|".join(["---"] * dim)}|---|---|
{chr(10).join(rows)}

- **Best so far:** y = {f(cur_best)} at x = {vec(bx)}

## 3. What the GP learned (reading the length scales)

The Gaussian Process fits one **length scale** per dimension - how fast y changes along that axis.
A tiny length scale means "very sensitive"; a maxed-out one means "this dimension barely matters".

{chr(10).join(ls_lines)}

The GP also reports, for any point, a prediction **mu** and an uncertainty **sigma**. Where data is
dense, sigma is small (confident); in unexplored gaps, sigma is large (uncertain).

## 4. Why this acquisition function: **{c['m']}{(' (k=' + str(c['k']) + ')') if c['k'] else ''}**

{nr['why']}

## 5. Week 1 - what we sent and what happened

- **Sent:** x = {vec(w1x)}
- **Received:** y = {f(w1y)}
- **Outcome:** {"**IMPROVED** over the previous best (" + f(w1_prev) + ")" if w1_improved else "did **not** improve over the previous best (" + f(w1_prev) + ") - but it is still information"}.

## 6. Week 2 - what we sent and what happened

- **Sent:** x = {vec(w2x)}
- **Received:** y = {f(w2y)}
- **Outcome:** {"**IMPROVED** over the previous best (" + f(w2_prev) + ")" if w2_improved else "did **not** improve over the previous best (" + f(w2_prev) + ")"}.

## 7. Week 3 - what we sent and what happened

- **Sent:** x = {vec(w3x)}
- **Received:** y = {f(w3y)}
- **Outcome:** {"**IMPROVED** over the previous best (" + f(w3_prev) + ")" if w3_improved else "did **not** improve over the previous best (" + f(w3_prev) + ")"}.

## 8. Week 4 - what we sent and what happened

- **Sent:** x = {vec(w4x)}
- **Received:** y = {f(w4y)}
- **GP had expected:** mu = {f(mu4)}, sigma = {f(sg4)}
- **Outcome:** {"**IMPROVED** over the previous best (" + f(w4_prev) + ")" if w4_improved else "did **not** improve over the previous best (" + f(w4_prev) + ")"}.

## 9. Week 5 - what we sent and what happened

- **Sent:** x = {vec(w5x)}
- **Received:** y = {f(w5y)}
- **GP had expected:** mu = {f(mu5)}, sigma = {f(sg5)}
- **Outcome:** {"**IMPROVED** over the previous best (" + f(w5_prev) + ")" if w5_improved else "did **not** improve over the previous best (" + f(w5_prev) + ")"}.

## 10. Week 6 - what we sent and what happened

- **Sent:** x = {vec(w6x)}
- **Received:** y = {f(w6y)}
- **GP had expected:** mu = {f(mu6)}, sigma = {f(sg6)}
- **Outcome:** {"**IMPROVED** over the previous best (" + f(w6_prev) + ")" if w6_improved else "did **not** improve over the previous best (" + f(w6_prev) + ")"}.

## 11. Week 7 - what we sent and what happened

- **Sent:** x = {vec(w7x)}
- **Received:** y = {f(w7y)}
- **GP had expected:** mu = {f(mu7)}, sigma = {f(sg7)}
- **Outcome:** {"**IMPROVED** over the previous best (" + f(w7_prev) + ")" if w7_improved else "did **not** improve over the previous best (" + f(w7_prev) + ")"}.

## 12. The lesson

{nr['lesson']}

## 13. Summary

| | Value |
|---|---|
| Real-world task | {NAME[fn]} |
| Dimensions | {dim} |
| Acquisition | {c['m']}{(' k=' + str(c['k'])) if c['k'] else ''} (Matern nu={c['nu']}) |
| Best before W1 | {f(w1_prev)} |
| Week 1 result | {f(w1y)} ({"improved" if w1_improved else "no improvement"}) |
| Week 2 result | {f(w2y)} ({"improved" if w2_improved else "no improvement"}) |
| Week 3 result | {f(w3y)} ({"improved" if w3_improved else "no improvement"}) |
| Week 4 result | {f(w4y)} ({"improved" if w4_improved else "no improvement"}) |
| Week 5 result | {f(w5y)} ({"improved" if w5_improved else "no improvement"}) |
| Week 6 result | {f(w6y)} ({"improved" if w6_improved else "no improvement"}) |
| Week 7 result | {f(w7y)} ({"improved" if w7_improved else "no improvement"}) |
| Current best | {f(cur_best)} |

*See `analysis_F{fn}.png` in this folder for the full 9-panel visual analysis.*
"""
    out = DATA_ROOT / f"function_{fn}" / f"EXPLANATION_F{fn}.md"
    out.write_text(doc, encoding="utf-8")
    print(f"F{fn}: wrote {out.relative_to(ROOT)}")

print("All explanation docs done.")
