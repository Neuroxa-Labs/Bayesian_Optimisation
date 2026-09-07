"""Append Week 12 observations to function_*/initial_*.npy (idempotent)."""
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = ROOT / "data"

WK12_X = {
    1: [0.636000, 0.687000],
    2: [0.717900, 0.020000],
    3: [0.492600, 0.691500, 0.401000],
    4: [0.404000, 0.413000, 0.355000, 0.413000],
    5: [0.440000, 0.980000, 0.980000, 0.980000],
    6: [0.440000, 0.250000, 0.590000, 0.728000, 0.132000],
    7: [0.073000, 0.425000, 0.300000, 0.157000, 0.345000, 0.671000],
    8: [0.143000, 0.061000, 0.211000, 0.049000, 0.413000, 0.511000, 0.217000, 0.916000],
}
WK12_Y = {
    1: -0.005123435866229551,
    2: 0.5368449903901873,
    3: -0.019448683714986648,
    4: 0.678600310561539,
    5: 3800.739529755285,
    6: -0.20535779957040554,
    7: 1.8722333952396066,
    8: 9.8729279,
}

for fn in range(1, 9):
    base = DATA_ROOT / f"function_{fn}"
    X = np.load(base / "initial_inputs.npy")
    Y = np.load(base / "initial_outputs.npy")
    prev_best = float(Y.max()) if len(Y) else float("-inf")
    x = np.array(WK12_X[fn], dtype=float)
    y = float(WK12_Y[fn])
    hit = False
    for i in range(len(Y)):
        if np.allclose(X[i], x, atol=1e-8):
            Y[i] = y
            hit = True
            how = "updated"
            break
    if not hit:
        X = np.vstack([X, x.reshape(1, -1)])
        Y = np.append(Y, y)
        how = "appended"
    np.save(base / "initial_inputs.npy", X)
    np.save(base / "initial_outputs.npy", Y)
    best = float(Y.max())
    print(f"F{fn}: {how} | y={y:.6g} | {'IMPROVED' if y > prev_best else 'no'} | best={best:.6g} | n={len(Y)}")
