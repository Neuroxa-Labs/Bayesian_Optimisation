# Week 7 Reflection — Black-Box Bayesian Optimisation

*Results received after submitting Week 7 queries.*

## Headline

**1 of 8 functions improved** — **F8** (9.865). **F5** re-hit the 3744 ridge (tie with best). F1 B+ still found no measurable radiation peak. F2 moved back toward the record band but did not reclaim 0.777.

## Week 7 results

| Fn | Task | Prior best → W7 y | Improved? | Notes |
|----|------|-------------------|-----------|-------|
| F1 | Radiation | ~1e−16 | 5e−25 | B+ near best; still no signal |
| F2 | Noisy ML | **0.777** | 0.507 | Better than W6 (0.403); not a new best |
| F3 | Drug side-effects | **−0.011** | −0.014 | Safe x₃; slight drop |
| F4 | Warehouse | **0.470** | 0.464 | Basin held |
| F5 | Chemical yield | **3744** | **3744** | Exact ridge re-confirmed |
| F6 | Cake recipe | **−0.240** | −0.267 | Step away from W6 best hurt |
| F7 | ML hyperparams | **1.857** | 1.847 | Micro-step underperformed |
| **F8** | 8-param ML | 9.864 | **9.865** | **Yes — new best** |

## What worked

- **F8:** Light UCB exploit around the prior best — small but real gain.
- **F5:** Returning to x₁=0.38 fully validated the ridge.
- **F2:** Directionally correct vs W6; still below W5 peak.

## What did not

- **F1:** Soft-signal + SVM + Isolation Forest near [0.73, 0.73] still ~0. Peak may be elsewhere or extremely narrow.
- **F6 / F7:** Leaving the exact best coordinates cost performance.
- **F3 / F4:** Local moves did not extend W6 records.

## Cumulative best after Week 7

| Fn | Best y | Queries |
|----|--------|---------|
| F1 | ~0 | 17 |
| F2 | **0.777** | 17 |
| F3 | **−0.011** | 22 |
| F4 | **0.470** | 37 |
| F5 | **3744** | 27 |
| F6 | **−0.240** | 27 |
| F7 | **1.857** | 37 |
| **F8** | **9.865** | 47 |

## Week 8 focus

See [`WEEK8_STRATEGY.md`](WEEK8_STRATEGY.md): return-to-best for F2/F6/F7; tight basin for F3/F4; ridge micro-tune for F5; F8 exploit from 9.865; F1 probe second-best warm region.
