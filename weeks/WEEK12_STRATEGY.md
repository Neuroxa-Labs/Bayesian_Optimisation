# Week 12 Strategy — PCA / ARD lens (12th round)

*After Week 11 (4/8 improved: F4, F5, F7, F8). Compress on principal / sensitive axes; recover F6.*

## Policy

| Mode | Functions | Action |
|------|-----------|--------|
| **Continue PC climb** | F5 | x₁ → 0.44 on locked high face |
| **Micro on new best** | F4, F7, F8 | Tiny offsets from W11 incumbents |
| **Return to true centroid** | F6, F2, F3 | W10 / historical best neighbourhood |
| **Signal lobe** | F1 | Stay in ~0.64/0.68; small step |

## Approved portal block

```
Function 1:  0.636000-0.687000
Function 2:  0.717900-0.020000
Function 3:  0.492600-0.691500-0.401000
Function 4:  0.404000-0.413000-0.355000-0.413000
Function 5:  0.440000-0.980000-0.980000-0.980000
Function 6:  0.440000-0.250000-0.590000-0.728000-0.132000
Function 7:  0.073000-0.425000-0.300000-0.157000-0.345000-0.671000
Function 8:  0.143000-0.061000-0.211000-0.049000-0.413000-0.511000-0.217000-0.916000
```

## One-line rationale

| Fn | Why |
|----|-----|
| F1 | Signal cluster micro (W11 −0.006 confirmed lobe) |
| F2 | Toward historical 0.777 at [0.7179, 0.02] |
| F3 | Exact-neighbour of −0.011 peak; x₃ locked |
| F4 | Local step from W11 0.675 |
| F5 | Ridge continue x₁=0.44 |
| F6 | **Hard return** toward W10 −0.136 centroid (W11 −0.372 was a miss) |
| F7 | Micro from W11 1.866 |
| F8 | Micro from W11 9.872 |

Discussion: [`WEEK12_DISCUSSION.md`](WEEK12_DISCUSSION.md).  
Reflection after results: update when portal `y` arrives.
