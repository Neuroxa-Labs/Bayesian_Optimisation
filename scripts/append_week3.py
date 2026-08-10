"""Append Week 3 observations to function_*/initial_*.npy files."""
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = ROOT / "data"

WK3_X = {
    1: [0.070000, 0.669525],
    2: [0.718765, 0.926564],
    3: [0.642581, 0.691593, 0.478715],
    4: [0.343955, 0.453869, 0.398079, 0.433861],
    5: [0.150000, 0.926480, 0.980000, 0.980000],
    6: [0.524058, 0.360869, 0.413794, 0.897694, 0.020000],
    7: [0.070000, 0.491672, 0.247422, 0.167429, 0.353878, 0.715603],
    8: [0.070000, 0.070000, 0.020000, 0.038786, 0.403935, 0.930000, 0.020000, 0.893085],
}
WK3_Y = {
    1: -1.7640587689392826e-130,
    2: 0.6022360650843126,
    3: -0.02269443855307699,
    4: -0.12619162666369688,
    5: 3108.4878561302053,
    6: -0.5376870203763128,
    7: 1.5253347319738353,
    8: 9.606407822369,
}

for fn in range(1, 9):
    base = DATA_ROOT / f"function_{fn}"
    X = np.load(base / "initial_inputs.npy")
    Y = np.load(base / "initial_outputs.npy")
    x3 = np.array(WK3_X[fn], dtype=float)
    y3 = float(WK3_Y[fn])

    if len(Y) >= 1 and np.allclose(X[-1], x3, atol=1e-5):
        Y[-1] = y3
        print(f"F{fn}: updated W3 y on existing x")
    else:
        X = np.vstack([X, x3.reshape(1, -1)])
        Y = np.append(Y, y3)
        print(f"F{fn}: appended W3 point")

    np.save(base / "initial_inputs.npy", X)
    np.save(base / "initial_outputs.npy", Y)
    prev_best = float(Y[:-1].max()) if len(Y) > 1 else float("-inf")
    best = float(Y.max())
    print(f"  y={y3:.6g} | {'IMPROVED' if y3 > prev_best else 'no improvement'} | best={best:.6g} | n={len(Y)}")
