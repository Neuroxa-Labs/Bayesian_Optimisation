"""Generate a per-function iteration progress report (Week 1 + Week 2) as an image.

Mirrors the GP/BO diagnostics: Current Best, Acquisition value of the next
query, Actual Result, Improvement, Method, exploration parameter, kernel
amplitude and per-dimension length scales — for each function and iteration.
"""
import warnings
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel as C
from sklearn.gaussian_process.kernels import Matern, WhiteKernel

warnings.filterwarnings("ignore")
ROOT = Path(__file__).parent

# ---- per-function config (matches the notebook) ----
FUNCTIONS = {
    1: dict(dim=2, n_init=10, alpha=1e-12, nu=0.5, white=False),
    2: dict(dim=2, n_init=10, alpha=1e-8, nu=2.5, white=True),
    3: dict(dim=3, n_init=15, alpha=1e-6, nu=1.5, white=False),
    4: dict(dim=4, n_init=30, alpha=1e-4, nu=2.5, white=False),
    5: dict(dim=4, n_init=20, alpha=1e-6, nu=2.5, white=False),
    6: dict(dim=5, n_init=20, alpha=1e-6, nu=2.5, white=False),
    7: dict(dim=6, n_init=30, alpha=1e-6, nu=2.5, white=False),
    8: dict(dim=8, n_init=40, alpha=1e-5, nu=1.5, white=False),
}

# method + exploration parameter per function/iteration (exploration phase, weeks 1-2)
# F5 flips to exploitation in iter2 once its best crosses 2000.
METHOD = {
    1: ("UNC", None, "COV", None, "COV", None, "COV", None, "COV", None),
    2: ("EI", 0.0, "EI", 0.0, "EI", 0.0, "MAN", None, "EI", 0.0),
    3: ("UCB", 2.576, "UCB", 2.576, "UCB", 2.576, "EI", 0.0, "EI", 0.0),
    4: ("UCB", 3.0, "UCB", 2.5, "UCB", 2.5, "EI", 0.0, "UCB", 1.5),
    5: ("UCB", 2.576, "UCB", 1.0, "EI", 0.0, "EI", 0.0, "EI", 0.0),
    6: ("EI", 0.0, "EI", 0.0, "EI", 0.0, "EI", 0.0, "EI", 0.0),
    7: ("EI", 0.0, "EI", 0.0, "EI", 0.0, "EI", 0.0, "EI", 0.0),
    8: ("UCB", 2.576, "UCB", 2.576, "UCB", 2.576, "UCB", 2.576, "UCB", 1.5),
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
    1: [0.421062, 0.463562], 2: [0.734317, 0.926564],
    3: [0.492581, 0.691593, 0.401268],
    4: [0.460385, 0.434644, 0.203056, 0.431758],
    5: [0.074189, 0.696480, 0.980000, 0.980000],
    6: [0.517086, 0.282151, 0.771390, 0.980000, 0.207535],
    7: [0.020000, 0.491672, 0.247422, 0.214597, 0.377195, 0.806097],
    8: [0.070000, 0.070000, 0.020000, 0.038786, 0.403935, 0.070000, 0.070000, 0.893085],
}
WK2_Y = {
    1: -0.006627379464825304, 2: 0.5706060535359335, 3: -0.020302412806162906,
    4: -3.305599024194517, 5: 1811.05681696222, 6: -0.5782346356754113,
    7: 1.2983310369966137, 8: 9.637407822369,
}
WK3_X = {
    1: [0.070000, 0.669525], 2: [0.718765, 0.926564],
    3: [0.642581, 0.691593, 0.478715],
    4: [0.343955, 0.453869, 0.398079, 0.433861],
    5: [0.150000, 0.926480, 0.980000, 0.980000],
    6: [0.524058, 0.360869, 0.413794, 0.897694, 0.020000],
    7: [0.070000, 0.491672, 0.247422, 0.167429, 0.353878, 0.715603],
    8: [0.070000, 0.070000, 0.020000, 0.038786, 0.403935, 0.930000, 0.020000, 0.893085],
}
WK3_Y = {
    1: -1.7640587689392826e-130, 2: 0.6022360650843126, 3: -0.02269443855307699,
    4: -0.12619162666369688, 5: 3108.4878561302053, 6: -0.5376870203763128,
    7: 1.5253347319738353, 8: 9.606407822369,
}
WK4_X = {
    1: [0.661537, 0.436390], 2: [0.700000, 0.020000],
    3: [0.592581, 0.771593, 0.436323],
    4: [0.414097, 0.385945, 0.378079, 0.441536],
    5: [0.380000, 0.980000, 0.980000, 0.980000],
    6: [0.365618, 0.143059, 0.477549, 0.930000, 0.120000],
    7: [0.070000, 0.431672, 0.307422, 0.158929, 0.347393, 0.672154],
    8: [0.020000, 0.020000, 0.188184, 0.038786, 0.403935, 0.486122, 0.020000, 0.893085],
}
WK4_Y = {
    1: 3.21298272257291e-28, 2: 0.6598602814677763, 3: -0.043381912559889324,
    4: 0.16598412185782196, 5: 3743.829067735118, 6: -0.6062467956245956,
    7: 1.8574559098912007, 8: 9.795759089917,
}
WK5_X = {
    1: [0.662502, 0.070000], 2: [0.717869, 0.020000],
    3: [0.492581, 0.691593, 0.401000],
    4: [0.425820, 0.439559, 0.381148, 0.436983],
    5: [0.280000, 0.980000, 0.980000, 0.980000],
    6: [0.430000, 0.240000, 0.580000, 0.720000, 0.120000],
    7: [0.070000, 0.376096, 0.307422, 0.107492, 0.323741, 0.648355],
    8: [0.126155, 0.070000, 0.224493, 0.038786, 0.403935, 0.497424, 0.228063, 0.893085],
}
WK5_Y = {
    1: -4.778494662600997e-128, 2: 0.7766450728516721, 3: -0.022346711262055334,
    4: 0.24027427340052343, 5: 3692.519989512911, 6: -0.2654080647396229,
    7: 1.8161306404666622, 8: 9.864471173458,
}


def fit_gp(X, Y, cfg):
    var = np.var(X, axis=0); var[var < 1e-6] = 0.1
    ls_init = np.sqrt(var)
    matern = Matern(length_scale=ls_init, length_scale_bounds=(1e-2, 10.0), nu=cfg["nu"])
    kernel = C(1.0, (1e-3, 1e3)) * matern
    if cfg["white"]:
        kernel = kernel + WhiteKernel(noise_level=1e-3, noise_level_bounds=(1e-8, 1e-1))
    gp = GaussianProcessRegressor(kernel=kernel, alpha=cfg["alpha"],
                                  n_restarts_optimizer=10, normalize_y=True, random_state=42)
    gp.fit(X, Y)
    return gp


def kernel_amp_and_ls(gp):
    params = gp.kernel_.get_params(deep=True)
    amp = None; ls = None
    for k, v in params.items():
        if k.endswith("constant_value") and amp is None:
            amp = float(v)
        if k.endswith("length_scale") and not k.endswith("length_scale_bounds"):
            ls = np.atleast_1d(np.asarray(v, dtype=float))
    return amp, ls


def acq_value(gp, x, method, param, f_best):
    x = np.asarray(x, dtype=float).reshape(1, -1)
    mu, sigma = gp.predict(x, return_std=True)
    mu, sigma = float(mu[0]), float(sigma[0])
    if method == "UNC":
        return sigma
    if method == "UCB":
        return mu + param * sigma
    s = max(sigma, 1e-12)
    z = (mu - f_best) / s
    return max((mu - f_best) * norm.cdf(z) + s * norm.pdf(z), 0.0)


def fmt(v):
    if v is None:
        return ""
    a = abs(v)
    if a != 0 and (a < 1e-3 or a >= 1e4):
        return f"{v:.2e}"
    return f"{v:.4f}"


# ---- compute everything ----
iters = {}  # iters[it][fn] = dict of metrics
for it in (1, 2, 3, 4, 5):
    iters[it] = {}
    for fn, cfg in FUNCTIONS.items():
        X = np.load(ROOT / f"function_{fn}" / "initial_inputs.npy")
        Y = np.load(ROOT / f"function_{fn}" / "initial_outputs.npy")
        n0 = cfg["n_init"]
        if it == 1:
            Xi, Yi = X[:n0], Y[:n0]
            next_x = WK1_X[fn]
            actual = WK1_Y[fn]
            method, param = METHOD[fn][0], METHOD[fn][1]
        elif it == 2:
            Xi, Yi = X[: n0 + 1], Y[: n0 + 1]
            next_x = WK2_X[fn]
            actual = WK2_Y[fn]
            method, param = METHOD[fn][2], METHOD[fn][3]
        elif it == 3:
            Xi, Yi = X[: n0 + 2], Y[: n0 + 2]
            next_x = WK3_X[fn]
            actual = WK3_Y[fn]
            method, param = METHOD[fn][4], METHOD[fn][5]
        elif it == 4:
            Xi, Yi = X[: n0 + 3], Y[: n0 + 3]
            next_x = WK4_X[fn]
            actual = WK4_Y[fn]
            method, param = METHOD[fn][6], METHOD[fn][7]
        else:
            Xi, Yi = X[: n0 + 4], Y[: n0 + 4]
            next_x = WK5_X[fn]
            actual = WK5_Y[fn]
            method, param = METHOD[fn][8], METHOD[fn][9]
        gp = fit_gp(Xi, Yi, cfg)
        cur_best = float(Yi.max())
        amp, ls = kernel_amp_and_ls(gp)
        acq = acq_value(gp, next_x, method, param if param is not None else 0.0, cur_best)
        improvement = (actual - cur_best) if actual is not None else None
        iters[it][fn] = dict(cur_best=cur_best, acq=acq, actual=actual,
                             improvement=improvement, method=method, param=param,
                             amp=amp, ls=ls, next_x=next_x, dim=cfg["dim"])

# ---- render ----
row_labels = (["Current Best", "Acquisition (next)", "Actual Result", "Improvement",
               "Method", "kappa / xi", "Kernel amp"]
              + [f"length-scale X[{i+1}]" for i in range(8)])
n_rows = len(row_labels)
SHORT = {1: "Radiation\nDetection", 2: "Noisy ML\nLog-Lik", 3: "Drug\nSide-Effects",
         4: "Warehouse\nPlacement", 5: "Chemical\nYield", 6: "Cake\nRecipe",
         7: "ML Hyper-\nparameters", 8: "8-Param\nML Model"}
fn_cols = [f"F{i}\n{SHORT[i]}" for i in range(1, 9)]

fig, axes = plt.subplots(5, 1, figsize=(17, 30))
fig.suptitle("BBO Progress Report — per-function GP / Bayesian Optimisation diagnostics",
             fontsize=15, fontweight="bold")

for ax_idx, it in enumerate((1, 2, 3, 4, 5)):
    ax = axes[ax_idx]
    ax.axis("off")
    ax.set_title(f"ITERATION {it}  (Week {it})", loc="left", fontsize=13,
                 fontweight="bold", color="#333")
    cell_text = []
    cell_colors = []
    for r, label in enumerate(row_labels):
        row = []
        colors = []
        for fn in range(1, 9):
            d = iters[it][fn]
            bg = "white"
            if label == "Current Best":
                val = fmt(d["cur_best"])
            elif label == "Acquisition (next)":
                val = fmt(d["acq"])
            elif label == "Actual Result":
                val = fmt(d["actual"]) if d["actual"] is not None else "(pending)"
                if d["actual"] is not None:
                    bg = "#b6e7b0" if d["improvement"] > 0 else "#f2b3b3"
                else:
                    bg = "#fff6cc"
            elif label == "Improvement":
                if d["improvement"] is None:
                    val = ""
                else:
                    val = ("+" if d["improvement"] > 0 else "") + fmt(d["improvement"])
                    bg = "#b6e7b0" if d["improvement"] > 0 else "#f2b3b3"
            elif label == "Method":
                val = f"Matern v={FUNCTIONS[fn]['nu']} / {d['method']}"
            elif label == "kappa / xi":
                val = "-" if d["param"] is None else fmt(d["param"])
            elif label == "Kernel amp":
                val = fmt(d["amp"])
            else:
                dim_i = int(label.split("[")[1].rstrip("]")) - 1
                if dim_i < len(d["ls"]):
                    val = fmt(float(d["ls"][dim_i]))
                else:
                    val = ""
                    bg = "#f0f0f0"
            row.append(val)
            colors.append(bg)
        cell_text.append(row)
        cell_colors.append(colors)

    tbl = ax.table(cellText=cell_text, rowLabels=row_labels, colLabels=fn_cols,
                   cellColours=cell_colors, loc="center", cellLoc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8.5)
    tbl.scale(1.0, 1.35)
    for (r, c), cell in tbl.get_celld().items():
        if r == 0 or c == -1:
            cell.set_text_props(fontweight="bold")
            cell.set_facecolor("#d9e1f2")
        if r == 0:
            cell.set_height(cell.get_height() * 2.1)
            cell.set_fontsize(8)

plt.tight_layout(rect=[0, 0, 1, 0.97])
png = ROOT / "progress_week5_report.png"
jpg = ROOT / "progress_week5_report.jpg"
plt.savefig(png, dpi=150, bbox_inches="tight")
try:
    plt.savefig(jpg, dpi=150, bbox_inches="tight")
    print(f"Saved {png.name} and {jpg.name}")
except Exception as e:
    print(f"Saved {png.name}; JPEG failed ({e})")

for fn in range(1, 9):
    d = iters[5][fn]
    ls = [round(float(v), 4) for v in d["ls"]]
    print(f"W5 F{fn}: best={d['cur_best']:.6g} acq={d['acq']:.6g} actual={d['actual']:.6g} ls={ls}")
