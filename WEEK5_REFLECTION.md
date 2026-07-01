# Week 5 Reflection — Black-Box Bayesian Optimisation

*Results received after submitting Week 5 queries (balanced exploit phase).*

## Headline

**3 of 8 functions improved** — **F2** (0.777), **F6** (−0.265), and **F8** (9.864). F5/F7 exploit steps did not beat Week 4 records. F6 interior strategy validated (avoiding box edges).

## Week 5 results

| Fn | Task | W4 best → W5 y | Improved? | Notes |
|----|------|----------------|-----------|-------|
| F1 | Radiation | ~0 | ~0 | Still no signal |
| **F2** | Noisy ML | 0.660 | **0.777** | **Yes — +18% new best** |
| F3 | Drug side-effects | −0.020 | −0.022 | No — x₃ lock held but missed best |
| F4 | Warehouse | 0.257 | 0.240 | No — stayed positive |
| F5 | Chemical yield | 3744 | 3693 | No — x₁=0.28 below W4 ridge at 0.38 |
| **F6** | Cake recipe | −0.478 | **−0.265** | **Yes — large move toward 0** |
| F7 | ML hyperparams | 1.857 | 1.816 | No — local refine underperformed |
| **F8** | 8-param ML | 9.796 | **9.864** | **Yes — new best** |

## What worked

- **F2:** EI exploit along high-x₁, low-x₂ band — clear new record.
- **F6:** Interior exploit (no 0.02/0.98 boundaries) — best week for F6 so far.
- **F8:** Light UCB exploit — modest but real gain in 8D.

## What did not

- **F5:** x₁ pushed to 0.28; best remains at x₁=0.38 (3744).
- **F7:** Local EI near 1.857 did not extend the record.
- **F3:** x₃≈0.401 lock safe but did not beat −0.020.

## Cumulative best after Week 5

| Fn | Best y | Queries |
|----|--------|---------|
| F1 | ~0 | 15 |
| F2 | **0.777** | 15 |
| F3 | −0.020 | 20 |
| F4 | 0.257 | 35 |
| **F5** | **3744** | 25 |
| F6 | **−0.265** | 25 |
| **F7** | **1.857** | 35 |
| **F8** | **9.864** | 45 |

## Week 6 focus

- **F5:** return x₁ toward 0.35–0.40 ridge; keep x₂–x₄ high.
- **F7:** refine around best x (1.857 query coords), not W5 direction.
- **F2 / F8:** continue exploit from new bests.
- **F3:** tighter local search at x₃≈0.401.
- **F1:** systematic coverage continues.
