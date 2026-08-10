# Week 6 Reflection — Black-Box Bayesian Optimisation

*Results received after submitting Week 6 queries.*

## Headline

**3 of 8 functions improved** — **F3** (−0.011), **F4** (0.470), and **F6** (−0.240). F4 was the standout jump. F1 local refine and F2/F5/F7/F8 did not beat prior records.

## Week 6 results

| Fn | Task | W5 best → W6 y | Improved? | Notes |
|----|------|----------------|-----------|-------|
| F1 | Radiation | ~1e−16 | ~0 | Local refine near best still ~0 |
| F2 | Noisy ML | **0.777** | 0.403 | x₁=0.75 overshot W5 band |
| **F3** | Drug side-effects | −0.020 | **−0.011** | **Yes — x₃ lock + refine** |
| **F4** | Warehouse | 0.257 | **0.470** | **Yes — large basin jump** |
| F5 | Chemical yield | **3744** | 3730 | Close; x₁=0.36 slightly off 0.38 |
| **F6** | Cake recipe | −0.265 | **−0.240** | **Yes — interior refine** |
| F7 | ML hyperparams | **1.857** | 1.847 | Near miss |
| F8 | 8-param ML | **9.864** | 9.863 | Flat |

## What worked

- **F4:** Local UCB around the positive basin — biggest single-week gain.
- **F3:** Keeping x₃≈0.401 while refining x₁/x₂.
- **F6:** Staying interior (no 0.02/0.98 edges).

## What did not

- **F2:** Moving x₁ from 0.718 → 0.75 destroyed the W5 record region.
- **F1:** Best-neighbour refine still no measurable radiation peak.
- **F5:** Ridge confirmed near x₁=0.38; 0.36 was slightly worse.

## Cumulative best after Week 6

| Fn | Best y | Queries |
|----|--------|---------|
| F1 | ~0 | 16 |
| F2 | **0.777** | 16 |
| F3 | **−0.011** | 21 |
| F4 | **0.470** | 36 |
| F5 | **3744** | 26 |
| F6 | **−0.240** | 26 |
| F7 | **1.857** | 36 |
| F8 | **9.864** | 46 |

## Week 7 focus

- **F1:** Switch to B+ (log soft-signal + RBF-SVM + Isolation Forest).
- **F2 / F5 / F7:** Return toward proven best coordinates.
- **F3 / F4 / F6:** Local refine from new Week 6 bests.
- **F8:** Light exploit near 9.864.
