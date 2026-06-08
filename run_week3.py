"""Execute notebook pipeline cells with CURRENT_WEEK=3 and save W3 queries."""
import json
import pickle
from pathlib import Path

ROOT = Path(__file__).parent
nb = json.loads((ROOT / "BBO_Capstone_Optimized.ipynb").read_text(encoding="utf-8"))

ns = {"__name__": "__main__"}
for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] != "code":
        continue
    src = "".join(cell["source"])
    if "EMAIL_RESULTS" in src and "y_new" in src:
        break
    if "CURRENT_WEEK = 2" in src:
        src = src.replace("CURRENT_WEEK = 2", "CURRENT_WEEK = 3")
    exec(compile(src, f"cell_{i}", "exec"), ns)

results = ns["results"]
submission_strings = ns["submission_strings"]
out = {}
for fn, data in results.items():
    r = data["result"]
    out[fn] = {
        "x": r["x_next"].tolist(),
        "portal": submission_strings[fn],
        "mu": float(r["mu"]),
        "sigma": float(r["sigma"]),
        "mode": r["mode"],
        "af": r.get("af_name"),
        "kappa": r.get("kappa"),
        "ls": r["length_scales"].tolist() if hasattr(r["length_scales"], "tolist") else list(r["length_scales"]),
    }
    print(f"F{fn}: {submission_strings[fn]}")

with open(ROOT / "week3_queries.pkl", "wb") as f:
    pickle.dump(out, f)
print("\nSaved week3_queries.pkl")
