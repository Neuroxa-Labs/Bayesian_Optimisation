# Week 12 Reflection — Black-Box Bayesian Optimisation

*Results after Week 12 portal submission (PCA / ARD lens).*

## Headline

**4 of 8 improved** — **F4, F5, F7, F8**. F5 ridge at x₁=0.44 reached ≈**3801**. F6 partially recovered (−0.372 → **−0.205**); F2 still missed 0.777.

## Week 12 results

| Fn | Prior best → W12 y | Improved? | Notes |
|----|--------------------|-----------|--------|
| F1 | ~0 | −0.00512 | Signal lobe held (3rd non-null) |
| F2 | **0.777** | 0.537 | No — still off needle |
| F3 | **−0.011** | −0.019 | No; closer than W11 |
| **F4** | 0.675 | **0.679** | **Yes** |
| **F5** | 3790 | **3801** | **Yes** — ridge continues |
| F6 | **−0.136** | −0.205 | Partial return (not best) |
| **F7** | 1.866 | **1.872** | **Yes** |
| **F8** | 9.872 | **9.873** | **Yes** |

## Cumulative best after Week 12

| Fn | Best y | Note |
|----|--------|------|
| F1 | ~0 (signal lobe) | Keep ~[0.64, 0.68] |
| F2 | **0.777** | Tighter return to [≈0.7179, 0.02] |
| F3 | **−0.011** | Protect peak |
| F4 | **0.679** | W12 |
| F5 | **3801** | W12 ridge |
| F6 | **−0.136** | Finish return to W10 x |
| F7 | **1.872** | W12 |
| F8 | **9.873** | W12 |

## Next

Final round: [`final_round_rl_reflection.md`](final_round_rl_reflection.md) · [`final_round_strategy.md`](final_round_strategy.md).
