"""Append Week 4 observations to function_*/initial_*.npy files."""
from pathlib import Path
import numpy as np

ROOT = Path(__file__).parent

WK4_X = {
    1: [0.661537, 0.436390],
    2: [0.700000, 0.020000],
    3: [0.592581, 0.771593, 0.436323],
    4: [0.414097, 0.385945, 0.378079, 0.441536],
    5: [0.380000, 0.980000, 0.980000, 0.980000],
    6: [0.365618, 0.143059, 0.477549, 0.930000, 0.120000],
    7: [0.070000, 0.431672, 0.307422, 0.158929, 0.347393, 0.672154],
    8: [0.020000, 0.020000, 0.188184, 0.038786, 0.403935, 0.486122, 0.020000, 0.893085],
}
WK4_Y = {
    1: 3.21298272257291e-28,
    2: 0.6598602814677763,
    3: -0.043381912559889324,
    4: 0.16598412185782196,
    5: 3743.829067735118,
    6: -0.6062467956245956,
    7: 1.8574559098912007,
    8: 9.795759089917,
}

for fn in range(1, 9):
    base = ROOT / f"function_{fn}"
    X = np.load(base / "initial_inputs.npy")
    Y = np.load(base / "initial_outputs.npy")
    x4 = np.array(WK4_X[fn], dtype=float)
    y4 = float(WK4_Y[fn])

    if len(Y) >= 1 and np.allclose(X[-1], x4, atol=1e-5):
        Y[-1] = y4
        print(f"F{fn}: updated W4 y on existing x")
    else:
        X = np.vstack([X, x4.reshape(1, -1)])
        Y = np.append(Y, y4)
        print(f"F{fn}: appended W4 point")

    np.save(base / "initial_inputs.npy", X)
    np.save(base / "initial_outputs.npy", Y)
    prev_best = float(Y[:-1].max()) if len(Y) > 1 else float("-inf")
    best = float(Y.max())
    print(f"  y={y4:.6g} | {'IMPROVED' if y4 > prev_best else 'no improvement'} | best={best:.6g} | n={len(Y)}")
