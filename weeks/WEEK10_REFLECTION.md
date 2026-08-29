# Week 10 Reflection — Black-Box Bayesian Optimisation

*Results after Week 10 portal submission.*

## Headline

**5 of 8 functions improved** — **F4, F5, F6, F7, F8**. Strongest week since the mid-project streak. F1 produced the first **measurable** reading in the peer basin (~0.64/0.68). F2 recovered toward the 0.777 peak.

## Week 10 results

| Fn | Prior best → W10 y | Improved? | Notes |
|----|--------------------|-----------|--------|
| F1 | ~0 | −0.00807 | Not a max-best; **signal cluster validated** |
| F2 | **0.777** | 0.720 | No; much better than W9 (0.52) |
| F3 | **−0.011** | −0.019 | No; safe x₃ held |
| **F4** | 0.642 | **0.667** | **Yes** |
| **F5** | 3769 | **3779** | **Yes** — ridge x₁=0.42 |
| **F6** | −0.240 | **−0.136** | **Yes** — large jump |
| **F7** | 1.858 | **1.863** | **Yes** |
| **F8** | 9.869 | **9.871** | **Yes** |

## What worked

- Trust-region exploit on F4/F5/F7/F8 continued the W8–W9 climb.
- F6 micro-return toward the cake basin paid off heavily (−0.24 → **−0.14**).
- F1 peer-basin hypothesis: non-null output where the 0.73 lobe was dead.

## What did not

- F2 still below 0.777 (noise / sharp ridge).
- F3 local step did not reclaim −0.011.
- F1 under pure maximisation is not a new incumbent (negative y), but the **cluster** is real.

## Cumulative best after Week 10

| Fn | Best y | Note |
|----|--------|------|
| F1 | ~0 (signal lobe open) | Exploit ~[0.64, 0.68] |
| F2 | **0.777** | |
| F3 | **−0.011** | |
| F4 | **0.667** | W10 |
| F5 | **3779** | W10 |
| F6 | **−0.136** | W10 |
| F7 | **1.863** | W10 |
| F8 | **9.871** | W10 |

## Week 11 focus

Clustering lens: stay inside proven high-y clusters (F4–F8, F6); tighten F1 signal cluster; nudge F2 toward 0.718/0.02; protect F3 safe band. See [`WEEK11_STRATEGY.md`](WEEK11_STRATEGY.md).
