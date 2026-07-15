"""Append Week 6 observations to function_*/initial_*.npy files."""
from pathlib import Path
import numpy as np

ROOT = Path(__file__).parent

WK6_X = {
    1: [0.755000, 0.710000],
    2: [0.750000, 0.020000],
    3: [0.492581, 0.691593, 0.401000],
    4: [0.400838, 0.413498, 0.376688, 0.406083],
    5: [0.360000, 0.980000, 0.980000, 0.980000],
    6: [0.440000, 0.250000, 0.590000, 0.730000, 0.130000],
    7: [0.070000, 0.416628, 0.307422, 0.136908, 0.324592, 0.654726],
    8: [0.070000, 0.272853, 0.209858, 0.038786, 0.403935, 0.545195, 0.198456, 0.893085],
}
WK6_Y = {
    1: -1.2733719774833445e-16,
    2: 0.40347007739097895,
    3: -0.011366393913517245,
    4: 0.469508628918597,
    5: 3729.8366843702797,
    6: -0.24039734108674735,
    7: 1.8471407406042062,
    8: 9.862535706371,
}

for fn in range(1, 9):
    base = ROOT / f"function_{fn}"
    X = np.load(base / "initial_inputs.npy")
    Y = np.load(base / "initial_outputs.npy")
    x6 = np.array(WK6_X[fn], dtype=float)
    y6 = float(WK6_Y[fn])

    if len(Y) >= 1 and np.allclose(X[-1], x6, atol=1e-5):
        Y[-1] = y6
        print(f"F{fn}: updated W6 y on existing x")
    else:
        X = np.vstack([X, x6.reshape(1, -1)])
        Y = np.append(Y, y6)
        print(f"F{fn}: appended W6 point")

    np.save(base / "initial_inputs.npy", X)
    np.save(base / "initial_outputs.npy", Y)
    prev_best = float(Y[:-1].max()) if len(Y) > 1 else float("-inf")
    best = float(Y.max())
    print(f"  y={y6:.6g} | {'IMPROVED' if y6 > prev_best else 'no improvement'} | best={best:.6g} | n={len(Y)}")
