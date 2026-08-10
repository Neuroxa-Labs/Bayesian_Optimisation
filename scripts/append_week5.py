"""Append Week 5 observations to function_*/initial_*.npy files."""
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = ROOT / "data"

WK5_X = {
    1: [0.662502, 0.070000],
    2: [0.717869, 0.020000],
    3: [0.492581, 0.691593, 0.401000],
    4: [0.425820, 0.439559, 0.381148, 0.436983],
    5: [0.280000, 0.980000, 0.980000, 0.980000],
    6: [0.430000, 0.240000, 0.580000, 0.720000, 0.120000],
    7: [0.070000, 0.376096, 0.307422, 0.107492, 0.323741, 0.648355],
    8: [0.126155, 0.070000, 0.224493, 0.038786, 0.403935, 0.497424, 0.228063, 0.893085],
}
WK5_Y = {
    1: -4.778494662600997e-128,
    2: 0.7766450728516721,
    3: -0.022346711262055334,
    4: 0.24027427340052343,
    5: 3692.519989512911,
    6: -0.2654080647396229,
    7: 1.8161306404666622,
    8: 9.864471173458,
}

for fn in range(1, 9):
    base = DATA_ROOT / f"function_{fn}"
    X = np.load(base / "initial_inputs.npy")
    Y = np.load(base / "initial_outputs.npy")
    x5 = np.array(WK5_X[fn], dtype=float)
    y5 = float(WK5_Y[fn])

    if len(Y) >= 1 and np.allclose(X[-1], x5, atol=1e-5):
        Y[-1] = y5
        print(f"F{fn}: updated W5 y on existing x")
    else:
        X = np.vstack([X, x5.reshape(1, -1)])
        Y = np.append(Y, y5)
        print(f"F{fn}: appended W5 point")

    np.save(base / "initial_inputs.npy", X)
    np.save(base / "initial_outputs.npy", Y)
    prev_best = float(Y[:-1].max()) if len(Y) > 1 else float("-inf")
    best = float(Y.max())
    print(f"  y={y5:.6g} | {'IMPROVED' if y5 > prev_best else 'no improvement'} | best={best:.6g} | n={len(Y)}")
