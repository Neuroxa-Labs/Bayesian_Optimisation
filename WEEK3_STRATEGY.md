# Week 3 Strategy — Black-Box Bayesian Optimisation

*Stage 2, Component 14.1 — third query after Week 2 reflection.*

## Context

After Week 2 (1/8 improved; F3 narrow bounds validated; F5 exploit mis-step), Week 3 refinements:

| Fn | Change from naive pipeline |
|----|---------------------------|
| F1 | Stronger coverage boundary penalty + interior retry |
| F3 | x1 narrow band (±0.15), x2 locked, x3 ±0.15 |
| F4 | κ 2.5; search ±0.06 around positive basin (not exact best_x) |
| F5 | **EI exploit** (not UCB); x1 ∈ [0.15, 0.30]; **log-transform y** |
| F7 | Soft boundary penalty on free dims |
| F8 | Unchanged (UCB + boundary penalty) |

## Week 3 queries (submit)

```
F1: 0.070000-0.669525
F2: 0.718765-0.926564
F3: 0.642581-0.691593-0.478715
F4: 0.343955-0.453869-0.398079-0.433861
F5: 0.150000-0.926480-0.980000-0.980000
F6: 0.524058-0.360869-0.413794-0.897694-0.020000
F7: 0.070000-0.491672-0.247422-0.167429-0.353878-0.715603
F8: 0.070000-0.070000-0.020000-0.038786-0.403935-0.930000-0.020000-0.893085
```

## Expected focus

- **F3:** continue toward 0 (momentum from −0.020 best).
- **F5:** climb from 2497 using EI at true best region.
- **F4:** stay in positive basin, avoid W2-style deep negative.
- **F1:** interior coverage (F1 x1 still near buffer — monitor).
