# Week 4 Reflection — Black-Box Bayesian Optimisation

*Results received after submitting Week 4 queries (peer-informed GP strategy).*

## Headline

**4 of 8 functions improved** — best week so far. **F5** (3744) and **F7** (1.857) set large new records; **F2** and **F8** also ticked up. F5 ridge exploit and F7 local EI validated the Week 4 plan.

## Week 4 results

| Fn | Task | W3 best → W4 y | Improved? | Notes |
|----|------|----------------|-----------|-------|
| F1 | Radiation | ~0 | ~0 | Still no signal; grid interior search |
| **F2** | Noisy ML | 0.611 | **0.660** | **Yes** — manual low-x₂ query found new best |
| F3 | Drug side-effects | −0.020 | −0.043 | No — x₃ safe but missed best |
| F4 | Warehouse | 0.257 | 0.166 | No — stayed positive (basin OK) |
| **F5** | **Chemical yield** | **3108** | **3744** | **Yes — +20% record** |
| F6 | Cake recipe | −0.478 | −0.606 | No |
| **F7** | **ML hyperparams** | **1.525** | **1.857** | **Yes — +22%** |
| **F8** | 8-param ML | 9.796 | **9.796** | Marginal (+0.0002) |

## What worked

- **F5:** EI + log-y, x₁→0.38, x₂–x₄ at 0.98 — ridge strategy from Weeks 3–4.
- **F7:** Small EI steps near Week 3 best — cliff exploit.
- **F4:** Local EI kept y positive (0.166) vs Week 2 disaster.

## What did not

- **F3:** x₃ < 0.5 rule held but did not beat −0.020.
- **F6:** Boundary x₄=0.93 hurt again.
- **F2:** Manual low-x₂ query — new best 0.660 actually improved over 0.611.

## Cumulative best after Week 4

| Fn | Best y | Queries |
|----|--------|---------|
| F1 | ~0 | 14 |
| F2 | **0.660** | 14 |
| F3 | −0.020 | 19 |
| F4 | 0.257 | 34 |
| **F5** | **3744** | 24 |
| F6 | −0.478 | 24 |
| **F7** | **1.857** | 34 |
| **F8** | **9.796** | 44 |

## Week 5 focus

- **F5 / F7:** continue EI exploit from new bests.
- **F3:** lock to best x₃≈0.401.
- **F2:** exploit new 0.660 region (high x₂ band).
- **F1:** keep grid / coverage.
