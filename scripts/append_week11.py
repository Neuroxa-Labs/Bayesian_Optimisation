"""Append Week 11 observations to function_*/initial_*.npy (idempotent)."""
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = ROOT / "data"

WK11_X = {
    1: [0.638000, 0.685000],
    2: [0.717800, 0.019800],
    3: [0.492580, 0.691600, 0.401000],
    4: [0.403000, 0.414000, 0.356000, 0.412000],
    5: [0.430000, 0.980000, 0.980000, 0.980000],
    6: [0.443000, 0.247000, 0.593000, 0.727000, 0.129000],
    7: [0.072000, 0.426000, 0.301000, 0.156000, 0.344000, 0.670000],
    8: [0.142000, 0.062000, 0.212000, 0.048000, 0.412000, 0.512000, 0.218000, 0.915000],
}
WK11_Y = {
    1: -0.006229646540338885,
    2: 0.5482414152470184,
    3: -0.02668306040308618,
    4: 0.6751664286960275,
    5: 3789.507062964496,
    6: -0.37218816139913213,
    7: 1.8664969679788408,
    8: 9.8721655,
}

for fn in range(1, 9):
    base = DATA_ROOT / f"function_{fn}"
    X = np.load(base / "initial_inputs.npy")
    Y = np.load(base / "initial_outputs.npy")
    x = np.array(WK11_X[fn], dtype=float)
    y = float(WK11_Y[fn])
    if len(Y) >= 1 and np.allclose(X[-1], x, atol=1e-8):
        Y[-1] = y
        how = "updated"
    else:
        hit = False
        for i in range(len(Y)):
            if np.allclose(X[i], x, atol=1e-8):
                Y[i] = y
                hit = True
                how = "updated-mid"
                break
        if not hit:
            X = np.vstack([X, x.reshape(1, -1)])
            Y = np.append(Y, y)
            how = "appended"
    np.save(base / "initial_inputs.npy", X)
    np.save(base / "initial_outputs.npy", Y)
    prev = float(Y[:-1].max()) if len(Y) > 1 else float("-inf")
    # if updated mid, recompute prev without this y carefully
    best = float(Y.max())
    print(f"F{fn}: {how} | y={y:.6g} | {'IMPROVED' if y > prev else 'no'} | best={best:.6g} | n={len(Y)}")
