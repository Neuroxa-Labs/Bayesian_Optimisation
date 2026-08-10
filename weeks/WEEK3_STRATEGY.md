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

## Week 3 results (received)

| Fn | y | vs prev best | Note |
|----|---|--------------|------|
| F1 | ≈ 0 | flat | still no signal |
| F2 | 0.602 | ↓ | below 0.611 |
| F3 | −0.023 | ↓ | slight regression from −0.020 |
| F4 | −0.126 | ↓ | positive basin but not improved |
| F5 | **3108** | **↑** | EI exploit + log-y worked |
| F6 | −0.538 | ↓ | |
| F7 | **1.525** | **↑** | new best |
| F8 | 9.606 | ↓ | below 9.796 |

**2/8 improved.** Cumulative bests: F5 **3108**, F7 **1.525**, F3 −0.020, F4 0.257, F8 9.796.

See [`WEEK3_REFLECTION.md`](WEEK3_REFLECTION.md) for full analysis.
