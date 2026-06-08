# Week 2 Reflection — Black-Box Bayesian Optimisation

*Module 13 Capstone — results received after submitting Week 2 queries.*

## Headline

**1 of 8 functions improved** on the second query. Only **F3** (Drug Side-Effects) beat its prior best.
Week 1's strong run (5/8) did not repeat — several functions that had improved in Week 1 gave back
some or all of that gain.

## Week 2 results

| Fn | Task | W1 y | W2 y | Improved? | Notes |
|----|------|------|------|-----------|-------|
| F1 | Radiation Detection | ~0 | −0.0066 | No | Still no positive signal; negative reading is noise-level |
| F2 | Noisy ML Log-Lik | 0.490 | 0.571 | No | Below best (0.611); noise, not a regime change |
| F3 | Drug Side-Effects | −0.168 | **−0.020** | **Yes** | Narrow bounds worked — now closest to 0 yet |
| F4 | Warehouse Placement | 0.257 | −3.31 | No | Large drop; multimodal landscape, exploration cost |
| F5 | Chemical Yield | 2497 | 1811 | No | Exploit step near boundary underperformed |
| F6 | Cake Recipe | −0.478 | −0.578 | No | Slight regression toward worse cake |
| F7 | ML Hyperparameters | 1.451 | 1.298 | No | Small drop; still in good region |
| F8 | 8-Param ML Model | 9.796 | 9.637 | No | Marginal drop; high-dim noise |

## What worked

- **F3 narrow bounds** after Week 1's boundary jump was the right fix. Keeping x2/x3 near the best
  point while exploring x1 produced our only Week 2 improvement.

## What did not

- **F5 exploitation** near the peak (0.074, 0.696, 0.98, 0.98) returned 1811 vs best 2497 — the
  exploit query moved away from the Week 1 winner (0.224, 0.847) and underperformed.
- **F4** exploration in the positive basin still carries multimodal risk; one query landed deep negative.
- **F1 coverage** (0.421, 0.464) avoided boundary artefacts but still found no source signal.

## Week 3 adjustments (implicit in pipeline)

- **F3:** continue local UCB with sensitive-dim bounds around new best (−0.020).
- **F5:** stay in exploit mode but search near the true best (0.224, 0.847), not the W2 point.
- **F1:** coverage exploration continues (still no signal above threshold).
- **F4/F6/F7/F8:** remain in exploration phase; expect variance, not monotonic gains.

## Cumulative best after Week 2

| Fn | Best y | Queries so far |
|----|--------|----------------|
| F1 | ~0 | 12 |
| F2 | 0.611 | 12 |
| F3 | −0.020 | 17 |
| F4 | 0.257 | 32 |
| F5 | 2497 | 22 |
| F6 | −0.478 | 22 |
| F7 | 1.451 | 32 |
| F8 | 9.796 | 42 |
