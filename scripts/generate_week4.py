"""Generate Week 4 portal queries (peer-informed GP strategy)."""
import warnings
from pathlib import Path

import numpy as np
from scipy.optimize import differential_evolution
from scipy.stats import norm
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel as C, Matern, WhiteKernel

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = ROOT / "data"
BUF = 0.02
WEEK = 4

FUNCTIONS = {
    1: dict(dim=2, n_init=10, alpha=1e-12, nu=0.5, white=False),
    2: dict(dim=2, n_init=10, alpha=1e-8, nu=2.5, white=True),
    3: dict(dim=3, n_init=15, alpha=1e-6, nu=1.5, white=False),
    4: dict(dim=4, n_init=30, alpha=1e-4, nu=2.5, white=False),
    5: dict(dim=4, n_init=20, alpha=1e-6, nu=2.5, white=False, log_y=True),
    6: dict(dim=5, n_init=20, alpha=1e-6, nu=2.5, white=False),
    7: dict(dim=6, n_init=30, alpha=1e-6, nu=2.5, white=False),
    8: dict(dim=8, n_init=40, alpha=1e-5, nu=1.5, white=False),
}


def fmt_sub(x):
    return "-".join(f"{v:.6f}" for v in x)


def fit_gp(X, Y, cfg):
    Yf = np.log(Y) if cfg.get("log_y") and np.all(Y > 0) else Y.copy()
    var = np.var(X, axis=0)
    var[var < 1e-6] = 0.1
    k = C(1.0, (1e-3, 1e3)) * Matern(np.sqrt(var), (1e-2, 10.0), nu=cfg["nu"])
    if cfg.get("white"):
        k = k + WhiteKernel(1e-3, (1e-8, 1e-1))
    gp = GaussianProcessRegressor(kernel=k, alpha=cfg["alpha"], n_restarts_optimizer=10,
                                  normalize_y=True, random_state=42)
    gp.fit(X, Yf)
    return gp, float(Yf.max())


def ei(gp, x, fb):
    mu, sg = gp.predict(np.asarray(x, dtype=float).reshape(1, -1), return_std=True)
    sg = max(float(sg[0]), 1e-12)
    z = (float(mu[0]) - fb) / sg
    return max((float(mu[0]) - fb) * norm.cdf(z) + sg * norm.pdf(z), 0.0)


def ucb(gp, x, fb, kappa):
    mu, sg = gp.predict(np.asarray(x, dtype=float).reshape(1, -1), return_std=True)
    return float(mu[0]) + kappa * float(sg[0])


def de_max(obj, bounds, seed=0):
    r = differential_evolution(lambda x: -obj(x), bounds, seed=seed, maxiter=800,
                               popsize=20, tol=1e-10, polish=True)
    return np.clip(r.x, 0.0, 0.999999)


def grid_f1(X, min_sep=0.10, n=12000, seed=44):
    rng = np.random.default_rng(seed)
    best_x, best_s = None, -1.0
    center = np.array([0.5, 0.5])
    for _ in range(n):
        x = rng.uniform(BUF + 0.08, 1 - BUF - 0.08, 2)
        d = float(np.min(np.linalg.norm(X - x, axis=1)))
        if d < min_sep:
            continue
        s = d + 0.08 * (1.0 - np.linalg.norm(x - center))
        if s > best_s:
            best_s, best_x = s, x.copy()
    if best_x is None:
        best_x = np.array([0.350000, 0.550000])
    return np.clip(best_x, BUF, 1 - BUF)


def query_f1(X):
    return grid_f1(X)


def query_f2():
    return np.array([0.700000, 0.020000])


def query_f3(X, Y, cfg):
    gp, fb = fit_gp(X, Y, cfg)
    safe = Y[X[:, 2] < 0.5]
    if len(safe):
        idx = np.where(X[:, 2] < 0.5)[0]
        bx = X[idx[np.argmax(Y[idx])]]
    else:
        bx = X[np.argmax(Y)]
    bnds = []
    for di in range(3):
        if di == 2:
            lo, hi = max(BUF, bx[2] - 0.06), min(0.49, bx[2] + 0.06)
        elif di == 1:
            lo, hi = max(BUF, bx[1] - 0.08), min(1 - BUF, bx[1] + 0.08)
        else:
            lo, hi = max(BUF, bx[0] - 0.10), min(1 - BUF, bx[0] + 0.10)
        bnds.append((lo, hi))
    return de_max(lambda x: ei(gp, x, fb), bnds)


def query_f4(X, Y, cfg):
    gp, fb = fit_gp(X, Y, cfg)
    bx = X[np.argmax(Y)]
    rad = 0.04
    bnds = [(max(BUF, bx[i] - rad), min(1 - BUF, bx[i] + rad)) for i in range(4)]
    return de_max(lambda x: ei(gp, x, fb), bnds)


def query_f5(X, Y, cfg):
    gp, fb = fit_gp(X, Y, cfg)
    bx = X[np.argmax(Y)]
    bnds = []
    for di in range(4):
        if di == 0:
            lo, hi = max(BUF, 0.15), min(1 - BUF, 0.38)
        elif di in (2, 3):
            lo, hi = max(BUF, 0.960), min(1 - BUF, 0.980)
        else:
            lo, hi = max(BUF, bx[1] - 0.06), min(1 - BUF, bx[1] + 0.06)
        bnds.append((lo, hi))
    return de_max(lambda x: ei(gp, x, fb), bnds)


def boundary_pen(x):
    return 0.5 * (np.maximum(0, BUF + 0.05 - x).sum() + np.maximum(0, x - (1 - BUF - 0.05)).sum())


def query_f6(X, Y, cfg):
    gp, fb = fit_gp(X, Y, cfg)
    bx = X[np.argmax(Y)]
    rad = 0.10
    bnds = [(max(BUF + 0.05, bx[i] - rad), min(1 - BUF - 0.05, bx[i] + rad)) for i in range(5)]
    return de_max(lambda x: ei(gp, x, fb) - 2.0 * boundary_pen(x), bnds)


def query_f7(X, Y, cfg):
    gp, fb = fit_gp(X, Y, cfg)
    bx = X[np.argmax(Y)]
    rad = 0.06
    bnds = [(max(BUF + 0.03, bx[i] - rad), min(1 - BUF - 0.03, bx[i] + rad)) for i in range(6)]
    return de_max(lambda x: ei(gp, x, fb) - 2.0 * boundary_pen(x), bnds)


def query_f8(X, Y, cfg):
    gp, fb = fit_gp(X, Y, cfg)
    bx = X[np.argmax(Y)]
    ls = gp.kernel_.get_params(deep=True)
    length = None
    for k, v in ls.items():
        if k.endswith("length_scale") and not k.endswith("bounds"):
            length = np.atleast_1d(np.asarray(v, dtype=float))
            break
    deg = [i for i, l in enumerate(length) if l >= 8.0]
    free = [i for i in range(8) if i not in deg]
    x = bx.copy()
    bnds = []
    for di in free:
        sens = length[di] < 0.2
        r = 0.08 if sens else 0.15
        bnds.append((max(BUF, bx[di] - r), min(1 - BUF, bx[di] + r)))
    if not free:
        return bx
    def obj(xf):
        pt = bx.copy()
        for fi, di in enumerate(free):
            pt[di] = xf[fi]
        mu, sg = gp.predict(pt.reshape(1, -1), return_std=True)
        return -(float(mu[0]) + 2.576 * float(sg[0]) - boundary_pen(pt))
    xf = de_max(obj, bnds)
    for fi, di in enumerate(free):
        x[di] = xf[fi]
    return np.clip(x, BUF, 1 - BUF)


GENERATORS = {
    1: lambda X, Y, c: query_f1(X),
    2: lambda X, Y, c: query_f2(),
    3: query_f3,
    4: query_f4,
    5: query_f5,
    6: query_f6,
    7: query_f7,
    8: query_f8,
}

if __name__ == "__main__":
    print(f"=== WEEK {WEEK} PORTAL (peer-informed GP) ===\n")
    out = {}
    for fn in range(1, 9):
        X = np.load(DATA_ROOT / f"function_{fn}" / "initial_inputs.npy")
        Y = np.load(DATA_ROOT / f"function_{fn}" / "initial_outputs.npy")
        x = GENERATORS[fn](X, Y, FUNCTIONS[fn])
        s = fmt_sub(x)
        out[fn] = s
        print(f"Function {fn}: {s}")
    print("\n--- copy block ---")
    for fn in range(1, 9):
        print(f"F{fn}: {out[fn]}")
