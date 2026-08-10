"""Generate Week 5 portal queries (GP + peer-informed manual overrides)."""
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = ROOT / "data"
WEEK = 5

# Approved Week 5 — pipeline + manual fixes (F3 x3 lock, F5 x1, F6 interior, F7 x1)
APPROVED = {
    1: [0.662502, 0.070000],
    2: [0.717869, 0.020000],
    3: [0.492581, 0.691593, 0.401000],
    4: [0.425820, 0.439559, 0.381148, 0.436983],
    5: [0.280000, 0.980000, 0.980000, 0.980000],
    6: [0.430000, 0.240000, 0.580000, 0.720000, 0.120000],
    7: [0.070000, 0.376096, 0.307422, 0.107492, 0.323741, 0.648355],
    8: [0.126155, 0.070000, 0.224493, 0.038786, 0.403935, 0.497424, 0.228063, 0.893085],
}


def fmt_sub(x):
    return "-".join(f"{v:.6f}" for v in x)


if __name__ == "__main__":
    print(f"=== WEEK {WEEK} PORTAL (approved) ===\n")
    for fn in range(1, 9):
        s = fmt_sub(APPROVED[fn])
        print(f"Function {fn}: {s}")
    print("\n--- copy block ---")
    for fn in range(1, 9):
        print(f"Function {fn}: {fmt_sub(APPROVED[fn])}")
