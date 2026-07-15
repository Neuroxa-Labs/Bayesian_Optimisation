# Week 6 Strategy — Black-Box Bayesian Optimisation

*Approved for portal submission after Week 5 (3/8 improved).*

**Results received:** 3/8 improved — see [`WEEK6_REFLECTION.md`](WEEK6_REFLECTION.md).

## Strategy summary

| Fn | AF / mode | Rationale |
|----|-----------|-----------|
| F1 | Manual local refine | Near best [0.731, 0.733]; coverage had failed for weeks |
| F2 | EI exploit | High x₁ / low x₂ band near W5 best 0.777 |
| F3 | EI + **x₃ lock ≈ 0.401** | Keep safe x₃; refine x₁/x₂ |
| F4 | UCB basin | Stay near positive region (then W5 best 0.257) |
| F5 | EI + log-y | Push x₁ toward 0.35–0.40 ridge; x₂–x₄ = 0.98 |
| F6 | EI interior | Exploit near W5 best; avoid box edges |
| F7 | EI local / manual | x₁ = 0.07; refine near 1.857 region |
| F8 | UCB light exploit | Continue from W5 best 9.864 |

## Approved portal queries

```
Function 1:  0.755000-0.710000
Function 2:  0.750000-0.020000
Function 3:  0.492581-0.691593-0.401000
Function 4:  0.400838-0.413498-0.376688-0.406083
Function 5:  0.360000-0.980000-0.980000-0.980000
Function 6:  0.440000-0.250000-0.590000-0.730000-0.130000
Function 7:  0.070000-0.416628-0.307422-0.136908-0.324592-0.654726
Function 8:  0.070000-0.272853-0.209858-0.038786-0.403935-0.545195-0.198456-0.893085
```

## Manual overrides vs pipeline

| Fn | Pipeline issue | Fix |
|----|----------------|-----|
| F1 | Corner 0.93/0.93 | Local best → 0.755/0.710 |
| F2 | x₁=0.98 boundary | Exploit band → 0.75/0.02 |
| F3 | x₃ drifted | Locked to 0.401000 |
| F5 | x₁=0.30 too low | Ridge → 0.360000 |
| F6 | x₅=0.02 boundary | Interior near best |
| F7 | x₁=0.025 edge | Set to 0.070000 |
