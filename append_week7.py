"""Append Week 7 observations to function_*/initial_*.npy files."""
from pathlib import Path
import numpy as np

ROOT = Path(__file__).parent

WK7_X = {
    1: [0.760000, 0.760000],
    2: [0.720000, 0.020000],
    3: [0.485000, 0.685000, 0.401000],
    4: [0.395000, 0.420000, 0.380000, 0.410000],
    5: [0.380000, 0.980000, 0.980000, 0.980000],
    6: [0.445000, 0.255000, 0.595000, 0.735000, 0.135000],
    7: [0.070000, 0.435000, 0.310000, 0.160000, 0.350000, 0.675000],
    8: [0.130000, 0.070000, 0.220000, 0.040000, 0.400000, 0.500000, 0.230000, 0.890000],
}
WK7_Y = {
    1: 5.183539428400652e-25,
    2: 0.5073917805634148,
    3: -0.014465733476312878,
    4: 0.4636989224185055,
    5: 3743.829067735118,
    6: -0.26724660706706216,
    7: 1.8468357700520182,
    8: 9.86519,
}

for fn in range(1, 9):
    base = ROOT / f"function_{fn}"
    X = np.load(base / "initial_inputs.npy")
    Y = np.load(base / "initial_outputs.npy")
    x7 = np.array(WK7_X[fn], dtype=float)
    y7 = float(WK7_Y[fn])

    if len(Y) >= 1 and np.allclose(X[-1], x7, atol=1e-5):
        Y[-1] = y7
        print(f"F{fn}: updated W7 y on existing x")
    else:
        X = np.vstack([X, x7.reshape(1, -1)])
        Y = np.append(Y, y7)
        print(f"F{fn}: appended W7 point")

    np.save(base / "initial_inputs.npy", X)
    np.save(base / "initial_outputs.npy", Y)
    prev_best = float(Y[:-1].max()) if len(Y) > 1 else float("-inf")
    best = float(Y.max())
    print(f"  y={y7:.6g} | {'IMPROVED' if y7 > prev_best else 'no improvement'} | best={best:.6g} | n={len(Y)}")
