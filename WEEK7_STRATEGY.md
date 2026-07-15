# Week 7 Strategy — Black-Box Bayesian Optimisation

*Approved for portal submission after Week 6 (3/8 improved).*

**Results received:** 1/8 improved — see [`WEEK7_REFLECTION.md`](WEEK7_REFLECTION.md).

## Strategy summary

| Fn | AF / mode | Rationale |
|----|-----------|-----------|
| F1 | **B+ soft-signal** | `log10(y)` ranking + RBF-SVM good/bad + Isolation Forest; query near warm UR band |
| F2 | EI exploit return | Return toward W5 best `[0.718, 0.02]` (W6 x₁=0.75 failed) |
| F3 | EI + x₃=0.401 | Protect W6 best −0.011 |
| F4 | UCB local | Exploit W6 basin 0.470 |
| F5 | EI ridge return | Exact W4 ridge x₁=**0.38**, x₂–x₄=0.98 |
| F6 | EI interior step | Small step from W6 best −0.240 |
| F7 | EI micro-step | Near W4 best 1.857 coords |
| F8 | UCB light exploit | Near W5 best 9.864 |

## Approved portal queries

```
Function 1:  0.760000-0.760000
Function 2:  0.720000-0.020000
Function 3:  0.485000-0.685000-0.401000
Function 4:  0.395000-0.420000-0.380000-0.410000
Function 5:  0.380000-0.980000-0.980000-0.980000
Function 6:  0.445000-0.255000-0.595000-0.735000-0.135000
Function 7:  0.070000-0.435000-0.310000-0.160000-0.350000-0.675000
Function 8:  0.130000-0.070000-0.220000-0.040000-0.400000-0.500000-0.230000-0.890000
```

## F1 method note (B+)

1. Soft score: `log10(y)` for y>0; large penalty for measurable negatives.
2. Label top/bottom soft quantiles → train **RBF-SVM**.
3. Fit **Isolation Forest** on observed inputs.
4. Score candidates with SVM P(good) + anomaly − distance-to-best; pick **0.76 / 0.76**.
