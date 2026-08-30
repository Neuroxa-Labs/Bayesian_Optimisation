"""Cluster / progress gallery for GitHub (Module 23 clustering + PCA lens).

Produces:
  reports/analysis/cluster_gallery_3d.png     — F1–F8 3D hulls (ARD axes)
  reports/analysis/progress_best_so_far.png   — best-y step charts
  reports/analysis/cluster_progress_pairs.png — hull + progress pairs (F3,F5,F7)
  reports/analysis/cluster_gallery.html       — lightweight viewer

Axes for 3D plots: top-3 ARD-sensitive dimensions from a Matérn GP (or all
dims if d<=3; for d=2 pad with a dummy z=0 plane note). Hulls = ConvexHull
per KMeans cluster when a cluster has >=4 non-coplanar points.
"""
from __future__ import annotations

import warnings
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
from sklearn.cluster import KMeans
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel as C
from sklearn.gaussian_process.kernels import Matern, WhiteKernel
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = ROOT / "data"
OUT = ROOT / "reports" / "analysis"
OUT.mkdir(parents=True, exist_ok=True)

NAME = {
    1: "Radiation",
    2: "Noisy ML",
    3: "Drug / adverse",
    4: "Warehouse",
    5: "Chemical yield",
    6: "Cake recipe",
    7: "HP tuning 6D",
    8: "8-param ML",
}

# Preferred axis hints (domain knowledge); ARD can override when confident
HINT = {
    1: (0, 1),
    2: (0, 1),
    3: (0, 1, 2),
    4: (0, 1, 2),
    5: (0, 1, 2),  # x1 ridge + high face
    6: (0, 2, 3),
    7: (1, 2, 5),
    8: (0, 4, 5),
}


def load_xy(fn: int):
    X = np.load(DATA_ROOT / f"function_{fn}" / "initial_inputs.npy")
    Y = np.load(DATA_ROOT / f"function_{fn}" / "initial_outputs.npy").ravel()
    return X.astype(float), Y.astype(float)


def fit_lengthscales(X, Y, white=False):
    d = X.shape[1]
    y = Y.copy()
    # F5-scale stabilisation
    if y.max() > 100:
        y = np.log1p(np.clip(y, 0, None))
    kernel = C(1.0, (1e-3, 1e3)) * Matern(
        length_scale=np.ones(d), length_scale_bounds=(1e-2, 1e2), nu=2.5
    )
    if white:
        kernel = kernel + WhiteKernel(noise_level=1e-3, noise_level_bounds=(1e-8, 1e1))
    gp = GaussianProcessRegressor(
        kernel=kernel, alpha=1e-6, normalize_y=True, n_restarts_optimizer=1
    )
    try:
        gp.fit(X, y)
        ls = np.asarray(gp.kernel_.k1.k2.length_scale, dtype=float).ravel()
        if ls.size != d:
            ls = np.ones(d)
    except Exception:
        ls = np.ones(d)
    return ls


def pick_axes(fn: int, X, Y):
    d = X.shape[1]
    if d == 2:
        return (0, 1, None)
    if d == 3:
        return (0, 1, 2)
    white = fn == 2
    ls = fit_lengthscales(X, Y, white=white)
    # shorter length scale => more sensitive
    order = np.argsort(ls)[:3]
    # blend with hint: keep hint dims if they appear in top-4 by sensitivity
    hint = HINT.get(fn, tuple(range(min(3, d))))
    top4 = set(np.argsort(ls)[:4].tolist())
    chosen = []
    for h in hint:
        if h in top4 and h not in chosen:
            chosen.append(int(h))
    for i in order:
        if int(i) not in chosen:
            chosen.append(int(i))
        if len(chosen) == 3:
            break
    while len(chosen) < 3:
        for i in range(d):
            if i not in chosen:
                chosen.append(i)
            if len(chosen) == 3:
                break
    return tuple(chosen[:3])


def kmeans_labels(X, k=None):
    n = len(X)
    if k is None:
        k = int(np.clip(round(np.sqrt(n / 2)), 2, 5))
    k = min(k, max(2, n // 3))
    Xs = StandardScaler().fit_transform(X)
    return KMeans(n_clusters=k, n_init=10, random_state=0).fit_predict(Xs), k


def add_hull(ax, pts, color, alpha=0.18):
    if len(pts) < 4:
        return
    try:
        # need volume
        if np.linalg.matrix_rank(pts - pts.mean(0)) < 3:
            return
        hull = ConvexHull(pts)
        for simplex in hull.simplices:
            tri = pts[simplex]
            poly = Poly3DCollection([tri], alpha=alpha, facecolor=color, edgecolor=color, linewidths=0.4)
            ax.add_collection3d(poly)
    except Exception:
        return


def project3(X, axes):
    a, b, c = axes
    if c is None:
        Z = np.column_stack([X[:, a], X[:, b], np.zeros(len(X))])
        labels = (f"x{a+1}", f"x{b+1}", "(pad)")
    else:
        Z = np.column_stack([X[:, a], X[:, b], X[:, c]])
        labels = (f"x{a+1}", f"x{b+1}", f"x{c+1}")
    return Z, labels


def plot_one_3d(ax, fn, X, Y):
    axes = pick_axes(fn, X, Y)
    Z, labs = project3(X, axes)
    labels, k = kmeans_labels(X)
    cmap = cm.get_cmap("coolwarm")
    yn = (Y - Y.min()) / (np.ptp(Y) + 1e-12)
    colors = cmap(yn)

    # hulls first (cluster mean y color)
    cluster_cmap = cm.get_cmap("tab10")
    for cid in range(k):
        mask = labels == cid
        if mask.sum() < 4:
            continue
        mean_y = float(Y[mask].mean())
        # map mean_y into coolwarm for hull tint
        t = (mean_y - Y.min()) / (np.ptp(Y) + 1e-12)
        add_hull(ax, Z[mask], cluster_cmap(cid % 10), alpha=0.15)

    ax.scatter(Z[:, 0], Z[:, 1], Z[:, 2], c=colors, s=28, depthshade=True, edgecolors="k", linewidths=0.2)
    ib = int(np.argmax(Y))
    ax.scatter(Z[ib, 0], Z[ib, 1], Z[ib, 2], c="gold", s=90, marker="*", edgecolors="k", linewidths=0.5, zorder=5)
    ax.set_xlabel(labs[0], fontsize=8)
    ax.set_ylabel(labs[1], fontsize=8)
    ax.set_zlabel(labs[2], fontsize=8)
    ax.tick_params(labelsize=7)
    d = X.shape[1]
    ax.set_title(f"F{fn} · {NAME[fn]} · d={d} · n={len(Y)} · k={k}", fontsize=9, pad=4)
    ax.view_init(elev=18, azim=35)


def plot_progress(ax, Y, title, n_init_guess=None):
    idx = np.arange(1, len(Y) + 1)
    running = np.maximum.accumulate(Y)
    ax.plot(idx, Y, "o", color="#9aa0a6", ms=4, label="y")
    ax.step(idx, running, where="post", color="#1a73e8", lw=2, label="best so far")
    # mark approximate BO start after initial design
    if n_init_guess is None:
        # heuristic: last jump before weekly cadence — use known inits
        n_init_guess = {1: 10, 2: 10, 3: 15, 4: 30, 5: 20, 6: 20, 7: 30, 8: 40}.get(
            int(title.split()[0][1:]) if title.startswith("F") else 0, 10
        )
    if 1 < n_init_guess < len(Y):
        ax.axvline(n_init_guess + 0.5, color="#d93025", ls="--", lw=1, label="weekly BO starts")
    ax.set_xlabel("sample", fontsize=8)
    ax.set_ylabel("y", fontsize=8)
    ax.set_title(title, fontsize=9)
    ax.tick_params(labelsize=7)
    ax.legend(fontsize=7, loc="best", frameon=False)
    ax.grid(True, alpha=0.25)


def main():
    # --- gallery 3D ---
    fig = plt.figure(figsize=(16, 10), facecolor="white")
    for i, fn in enumerate(range(1, 9)):
        ax = fig.add_subplot(2, 4, i + 1, projection="3d")
        X, Y = load_xy(fn)
        plot_one_3d(ax, fn, X, Y)
    fig.suptitle(
        "Promising clusters (KMeans hulls) · axes = ARD-sensitive dims · ★ = best y",
        fontsize=13,
        y=0.98,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    p1 = OUT / "cluster_gallery_3d.png"
    fig.savefig(p1, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print("wrote", p1)

    # --- progress all ---
    fig, axes = plt.subplots(2, 4, figsize=(14, 7), facecolor="white")
    n_init = {1: 10, 2: 10, 3: 15, 4: 30, 5: 20, 6: 20, 7: 30, 8: 40}
    for ax, fn in zip(axes.ravel(), range(1, 9)):
        _, Y = load_xy(fn)
        plot_progress(ax, Y, f"F{fn} {NAME[fn]}", n_init_guess=n_init[fn])
    fig.suptitle("Trends influencing next query — best so far", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    p2 = OUT / "progress_best_so_far.png"
    fig.savefig(p2, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print("wrote", p2)

    # --- pairs (like peer blog: hull | progress) ---
    fig = plt.figure(figsize=(12, 10), facecolor="white")
    for row, fn in enumerate([3, 5, 7]):
        X, Y = load_xy(fn)
        ax3 = fig.add_subplot(3, 2, 2 * row + 1, projection="3d")
        plot_one_3d(ax3, fn, X, Y)
        axp = fig.add_subplot(3, 2, 2 * row + 2)
        plot_progress(axp, Y, f"F{fn} progress", n_init_guess=n_init[fn])
    fig.suptitle("Cluster view + progress (F3, F5, F7)", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    p3 = OUT / "cluster_progress_pairs.png"
    fig.savefig(p3, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print("wrote", p3)

    # --- html viewer ---
    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>BBO cluster &amp; progress gallery</title>
<style>
body{{font-family:system-ui,sans-serif;max-width:1100px;margin:24px auto;padding:0 16px;color:#222;background:#f7f8fa}}
h1{{font-size:1.35rem}} h2{{font-size:1.05rem;margin-top:1.6rem}}
p{{color:#555;line-height:1.45;font-size:.95rem}}
img{{width:100%;border:1px solid #ddd;border-radius:8px;background:#fff;margin:.6rem 0 1.2rem}}
code{{background:#eee;padding:1px 5px;border-radius:3px;font-size:.85rem}}
</style></head><body>
<h1>Cluster &amp; progress gallery</h1>
<p>KMeans hulls on ARD-selected axes (GP Matérn length scales). Gold star = incumbent.
Generated by <code>scripts/make_cluster_gallery.py</code> from <code>data/function_*/</code> through Week 10.</p>
<h2>3D promising clusters (F1–F8)</h2>
<img src="cluster_gallery_3d.png" alt="3D cluster gallery">
<h2>Best-so-far trends</h2>
<img src="progress_best_so_far.png" alt="Progress charts">
<h2>Pairs — cluster + trend (F3, F5, F7)</h2>
<img src="cluster_progress_pairs.png" alt="Cluster progress pairs">
</body></html>
"""
    p4 = OUT / "cluster_gallery.html"
    p4.write_text(html, encoding="utf-8")
    print("wrote", p4)


if __name__ == "__main__":
    main()
