# Week 3 Reflection — Black-Box Bayesian Optimisation

*Results received after submitting Week 3 queries.*

## Headline

**2 of 8 functions improved** — a solid recovery after Week 2’s weak 1/8. **F5** and **F7** set new bests; the Week 3 strategy refinements (EI exploit for F5, F3 interior bands, F4 basin search) paid off where it mattered most.

## Week 3 results

| Fn | Task | W2 best → W3 y | Improved? | Notes |
|----|------|----------------|-----------|-------|
| F1 | Radiation | ~0 | ~0 | Still no signal |
| F2 | Noisy ML | 0.611 | 0.602 | No — noise band |
| F3 | Drug side-effects | −0.020 | −0.023 | No — slight regression |
| F4 | Warehouse | 0.257 | −0.126 | No — still in basin but negative draw |
| **F5** | **Chemical yield** | **2497** | **3108** | **Yes — +24% new record** |
| F6 | Cake recipe | −0.478 | −0.538 | No |
| **F7** | **ML hyperparams** | **1.451** | **1.525** | **Yes — +5%** |
| F8 | 8-param ML | 9.796 | 9.606 | No — marginal drop |

## What worked

- **F5 EI exploit** with x₁ ∈ [0.15, 0.30] and log-transform GP: yield jumped **2497 → 3108**. Week 2’s failed exploit (1811) is fully reversed.
- **F7** soft boundary penalty + local EI: new best **1.525** at interior x₁ = 0.07 (vs 0.02 before).

## What did not

- **F3** interior query (−0.023) missed the −0.020 best — x₃ moved to 0.479 vs 0.401; small step back.
- **F4** basin search still returned negative (−0.126) though less catastrophic than Week 2 (−3.31).

## Cumulative best after Week 3

| Fn | Best y | Queries |
|----|--------|---------|
| F1 | ~0 | 13 |
| F2 | 0.611 | 13 |
| F3 | −0.020 | 18 |
| F4 | 0.257 | 33 |
| **F5** | **3108** | 23 |
| F6 | −0.478 | 23 |
| **F7** | **1.525** | 33 |
| F8 | 9.796 | 43 |

## Week 4 focus

- **F5:** continue EI exploit — new peak at (0.15, 0.926, 0.98, 0.98); climb further.
- **F7:** exploit momentum around new best.
- **F3:** tighten back toward −0.020 best (x₃ ≈ 0.40).
- **F4:** stay in positive basin; avoid negative drift.
