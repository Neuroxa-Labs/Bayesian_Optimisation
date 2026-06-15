"""Save progress_week{N}.png — best observed y per function."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).parent
N_INIT = {1: 10, 2: 10, 3: 15, 4: 30, 5: 20, 6: 20, 7: 30, 8: 40}
WEEK = 3

fig, ax = plt.subplots(figsize=(10, 5))
labels, bests = [], []
for fn in range(1, 9):
    Y = np.load(ROOT / f"function_{fn}" / "initial_outputs.npy")
    labels.append(f"F{fn}")
    bests.append(float(Y.max()))

colors = ["#00b894" if fn == 3 else "#636e72" for fn in range(1, 9)]
ax.bar(labels, bests, color=colors, edgecolor="white")
ax.set_title(f"Best Observed Output — Week {WEEK}")
ax.set_ylabel("best y")
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
out = ROOT / f"progress_week{WEEK}.png"
fig.savefig(out, dpi=150, bbox_inches="tight")
plt.close()
print(f"Saved {out.name}")
