"""Append Week 13 / final-round observations when portal y arrives (idempotent).

Fill WK13_Y from the portal email, then run:
  python scripts/append_week13.py
"""
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = ROOT / "data"

WK13_X = {
    1: [0.635000, 0.688000],
    2: [0.717870, 0.020000],
    3: [0.492580, 0.691590, 0.401000],
    4: [0.405000, 0.412000, 0.354000, 0.414000],
    5: [0.450000, 0.980000, 0.980000, 0.980000],
    6: [0.441200, 0.249200, 0.590800, 0.728700, 0.131200],
    7: [0.074000, 0.424000, 0.299000, 0.158000, 0.346000, 0.672000],
    8: [0.144000, 0.060000, 0.210000, 0.050000, 0.414000, 0.510000, 0.216000, 0.917000],
}

# Paste portal outputs here when available (None = skip append for that function)
WK13_Y = {
    1: None,
    2: None,
    3: None,
    4: None,
    5: None,
    6: None,
    7: None,
    8: None,
}

for fn in range(1, 9):
    y = WK13_Y[fn]
    if y is None:
        print(f"F{fn}: skipped (y not set yet)")
        continue
    base = DATA_ROOT / f"function_{fn}"
    X = np.load(base / "initial_inputs.npy")
    Y = np.load(base / "initial_outputs.npy")
    prev_best = float(Y.max()) if len(Y) else float("-inf")
    x = np.array(WK13_X[fn], dtype=float)
    y = float(y)
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
