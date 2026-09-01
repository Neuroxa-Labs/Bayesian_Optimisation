# Week 11 Reflection — Black-Box Bayesian Optimisation

*Results after Week 11 portal submission (clustering lens).*

## Headline

**4 of 8 improved** — **F4, F5, F7, F8**. Ridge / local-basin bets paid again. **F6 collapsed** (−0.136 → −0.372) after a small step off the Week 10 cake centroid. F2 missed the 0.777 needle (0.548). F1 stayed in the signal lobe (−0.006).

## Week 11 results

| Fn | Prior best → W11 y | Improved? | Notes |
|----|--------------------|-----------|--------|
| F1 | ~0 | −0.00623 | Signal cluster held (better than W10 −0.008; still not max-best) |
| F2 | **0.777** | 0.548 | No — near centroid but ridge is sharp / noisy |
| F3 | **−0.011** | −0.027 | No — safe x₃ held; did not reclaim peak |
| **F4** | 0.667 | **0.675** | **Yes** |
| **F5** | 3779 | **3790** | **Yes** — ridge x₁=0.43 |
| F6 | **−0.136** | −0.372 | No — left W10 centroid; **return next week** |
| **F7** | 1.863 | **1.866** | **Yes** |
| **F8** | 9.871 | **9.872** | **Yes** |

## What worked

- Trust-region micro-steps on F4 / F7 / F8 kept ticking.
- F5 ridge climb 0.42→**0.43** continues to raise yield.

## What did not

- F6: exploiting “next to” W10 best was still too far — treat −0.136 x as hard centroid.
- F2: 0.7178/0.0198 ≠ 0.777 peak; need closer to historical [≈0.7179, 0.0200].
- F3: local return insufficient; stay locked on best x₃≈0.401.

## Cumulative best after Week 11

| Fn | Best y | Note |
|----|--------|------|
| F1 | ~0 (signal lobe open) | Keep ~[0.64, 0.68] |
| F2 | **0.777** | Return to [≈0.718, 0.02] |
| F3 | **−0.011** | Protect peak coords |
| F4 | **0.675** | W11 |
| F5 | **3790** | W11 ridge |
| F6 | **−0.136** | W10 still incumbent |
| F7 | **1.866** | W11 |
| F8 | **9.872** | W11 |

## Week 12 focus

PCA / ARD lens: move only sensitive axes; **return F6 to W10 cluster**; pull F2 to historical best; continue F5 x₁; micro-exploit F4/F7/F8. See [`WEEK12_STRATEGY.md`](WEEK12_STRATEGY.md).
