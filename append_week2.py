"""Append Week 2 observations to function_*/initial_*.npy files."""
from pathlib import Path
import numpy as np

ROOT = Path(__file__).parent

WK2_X = {
    1: [0.421062, 0.463562],
    2: [0.734317, 0.926564],
    3: [0.492581, 0.691593, 0.401268],
    4: [0.460385, 0.434644, 0.203056, 0.431758],
    5: [0.074189, 0.696480, 0.980000, 0.980000],
    6: [0.517086, 0.282151, 0.771390, 0.980000, 0.207535],
    7: [0.020000, 0.491672, 0.247422, 0.214597, 0.377195, 0.806097],
    8: [0.070000, 0.070000, 0.020000, 0.038786, 0.403935, 0.070000, 0.070000, 0.893085],
}
WK2_Y = {
    1: -0.006627379464825304,
    2: 0.5706060535359335,
    3: -0.020302412806162906,
    4: -3.305599024194517,
    5: 1811.05681696222,
    6: -0.5782346356754113,
    7: 1.2983310369966137,
    8: 9.637407822369,
}

for fn in range(1, 9):
    base = ROOT / f"function_{fn}"
    X = np.load(base / "initial_inputs.npy")
    Y = np.load(base / "initial_outputs.npy")
    x2 = np.array(WK2_X[fn], dtype=float)
    y2 = float(WK2_Y[fn])

    if len(Y) >= 1 and np.allclose(X[-1], x2, atol=1e-5):
        print(f"F{fn}: already has W2 x — updating y only")
        Y[-1] = y2
    else:
        X = np.vstack([X, x2.reshape(1, -1)])
        Y = np.append(Y, y2)
        print(f"F{fn}: appended W2 point")

    np.save(base / "initial_inputs.npy", X)
    np.save(base / "initial_outputs.npy", Y)
    prev_best = float(Y[:-1].max()) if len(Y) > 1 else float("-inf")
    best = float(Y.max())
    improved = y2 > prev_best
    print(f"  y={y2:.6g} | {'IMPROVED' if improved else 'no improvement'} | best={best:.6g} | n={len(Y)}")
