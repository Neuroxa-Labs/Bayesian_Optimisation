"""Execute notebook pipeline cells with CURRENT_WEEK=N and save queries."""
import json
import pickle
import sys
from pathlib import Path

WEEK = int(sys.argv[1]) if len(sys.argv) > 1 else 4

ROOT = Path(__file__).parent
nb = json.loads((ROOT / "BBO_Capstone_Optimized.ipynb").read_text(encoding="utf-8"))

ns = {"__name__": "__main__"}
for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] != "code":
        continue
    src = "".join(cell["source"])
    if "EMAIL_RESULTS" in src and "y_new" in src:
        break
    for w in range(2, 14):
        src = src.replace(f"CURRENT_WEEK = {w}", f"CURRENT_WEEK = {WEEK}")
    exec(compile(src, f"cell_{i}", "exec"), ns)

results = ns["results"]
submission_strings = ns["submission_strings"]
print(f"\n=== WEEK {WEEK} PORTAL ===")
for fn in range(1, 9):
    if fn in submission_strings:
        print(f"  Function {fn}: {submission_strings[fn]}")

with open(ROOT / f"week{WEEK}_queries.pkl", "wb") as f:
    pickle.dump({fn: submission_strings[fn] for fn in submission_strings}, f)
