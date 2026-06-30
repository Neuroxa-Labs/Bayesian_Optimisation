# Week 5 Strategy — Black-Box Bayesian Optimisation

*Approved for portal submission (14 observations per function, balanced phase).*

## Strategy summary

| Fn | AF / mode | Rationale |
|----|-----------|-----------|
| F1 | Coverage grid | No signal yet; interior exploration |
| F2 | EI exploit | W4 best 0.660 at high x₁, low x₂ — continue |
| F3 | EI + **x₃ lock ≈ 0.401** | Best −0.020; avoid x₃ > 0.5 (peer W4 lesson) |
| F4 | UCB basin ±0.06 | Stay near positive region (best 0.257) |
| F5 | EI + log-y exploit | Push x₁ down from 0.38; keep x₂–x₄ high |
| F6 | EI interior | Exploit but avoid box edges (W4 boundary hurt) |
| F7 | EI local / manual | Refine near best 1.857; x₁ = 0.07 not 0.02 |
| F8 | UCB k≈1.5 | Light exploit in 8D |

**Surrogate:** Gaussian Process (not NN). NN concepts used in forum reflection only.

## Approved portal queries

```
Function 1:  0.662502-0.070000
Function 2:  0.717869-0.020000
Function 3:  0.492581-0.691593-0.401000
Function 4:  0.425820-0.439559-0.381148-0.436983
Function 5:  0.280000-0.980000-0.980000-0.980000
Function 6:  0.430000-0.240000-0.580000-0.720000-0.120000
Function 7:  0.070000-0.376096-0.307422-0.107492-0.323741-0.648355
Function 8:  0.126155-0.070000-0.224493-0.038786-0.403935-0.497424-0.228063-0.893085
```

## Manual overrides vs pipeline

| Fn | Pipeline issue | Fix |
|----|----------------|-----|
| F3 | x₃ = 0.517 (unsafe) | Locked to 0.401000 |
| F5 | x₁ = 0.15 (too aggressive) | Set to 0.280000 |
| F6 | Boundary values 0.02/0.98 | Interior exploit near best |
| F7 | x₁ = 0.02 at edge | Set to 0.070000 (W4 best region) |

## Cumulative bests entering Week 5

| Fn | Best y |
|----|--------|
| F1 | ~0 |
| F2 | 0.660 |
| F3 | −0.020 |
| F4 | 0.257 |
| F5 | 3744 |
| F6 | −0.478 |
| F7 | 1.857 |
| F8 | 9.796 |
