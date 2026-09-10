# Weekly analysis archive

Per-function diagnostic snapshots regenerated from `data/function_*/` through **Week 13**.
Each file uses only the history available **at that week** (no future leakage).

| Pattern | Meaning |
|---------|---------|
| `function_{N}_week{W}_analysis.png` | Function N after weekly round W |

## Coverage

| Fn | Weeks present |
|----|---------------|
| F1 Radiation | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 |
| F2 Noisy ML | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 |
| F3 Drug / adverse | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 |
| F4 Warehouse | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 |
| F5 Chem. yield | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 |
| F6 Cake recipe | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 |
| F7 HP tuning | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 |
| F8 8-param ML | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 |

**Current (Week-12) gallery** (cluster hulls + best-so-far): [`../README.md`](../README.md).

**Current 9-panel deep dive** per function: `data/function_N/analysis_FN.png`.

Regenerate this archive:

```bash
python scripts/make_archive_week_snapshots.py
```
