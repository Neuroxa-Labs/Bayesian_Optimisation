# F8 - 8-Parameter ML Model Optimisation (8-D) - Learn from Scratch

## 1. The big picture: what is the problem?

**Real world:** You are optimising a complex ML model with 8 parameters.

- **x** = 8 parameters
- **y** = a model score (higher = better)
- **Goal:** maximise the score in a large 8-D space.
- **Constraint:** every evaluation is expensive - only **one query per week**, ~13 weeks total. Choose wisely.

This is a **black box**: we never see the formula, only "input x -> output y". That is exactly what
Bayesian Optimisation is built for - finding the best of an expensive unknown function in few tries.

## 2. What we were given (40 initial points + 2 weekly queries = 42 observations)

| # | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | y | note |
|---|---|---|---|---|---|---|---|---|---|---|
| 41 | 0.0200 | 0.0200 | 0.1887 | 0.0388 | 0.4039 | 0.4868 | 0.0200 | 0.8931 | 9.7956 | BEST |
| 42 | 0.0700 | 0.0700 | 0.0200 | 0.0388 | 0.4039 | 0.0700 | 0.0700 | 0.8931 | 9.6374 |  |
| 15 | 0.0564 | 0.0660 | 0.0229 | 0.0388 | 0.4039 | 0.8011 | 0.4883 | 0.8931 | 9.5985 |  |
| 22 | 0.8989 | 0.5236 | 0.8768 | 0.2187 | 0.9003 | 0.2828 | 0.9111 | 0.4724 | 5.8411 |  |
| 10 | 0.9849 | 0.6995 | 0.9989 | 0.1801 | 0.5801 | 0.2311 | 0.4908 | 0.3137 | 5.5922 | WORST |

- **Best so far:** y = 9.7956 at x = [0.0200, 0.0200, 0.1887, 0.0388, 0.4039, 0.4868, 0.0200, 0.8931]

## 3. What the GP learned (reading the length scales)

The Gaussian Process fits one **length scale** per dimension - how fast y changes along that axis.
A tiny length scale means "very sensitive"; a maxed-out one means "this dimension barely matters".

- `x1`: length-scale = 3.6652 -> moderate influence
- `x2`: length-scale = 5.7405 -> **degenerate** - GP sees little effect from this dimension (it locks it)
- `x3`: length-scale = 2.6902 -> moderate influence
- `x4`: length-scale = 9.7271 -> **degenerate** - GP sees little effect from this dimension (it locks it)
- `x5`: length-scale = 10.0000 -> **degenerate** - GP sees little effect from this dimension (it locks it)
- `x6`: length-scale = 7.3184 -> **degenerate** - GP sees little effect from this dimension (it locks it)
- `x7`: length-scale = 3.8318 -> moderate influence
- `x8`: length-scale = 10.0000 -> **degenerate** - GP sees little effect from this dimension (it locks it)

The GP also reports, for any point, a prediction **mu** and an uncertainty **sigma**. Where data is
dense, sigma is small (confident); in unexplored gaps, sigma is large (uncertain).

## 4. Why this acquisition function: **UCB (k=2.576)**

The 8-D space is enormous. **UCB k=2.576** plus a **boundary penalty** keeps exploration alive but discourages edge-hugging points (Week 2 had 1 dim on boundary vs 5 before). nu=1.5 is a mid-smoothness compromise.

## 5. Week 1 - what we sent and what happened

- **Sent:** x = [0.0200, 0.0200, 0.1887, 0.0388, 0.4039, 0.4868, 0.0200, 0.8931]
- **Received:** y = 9.7956
- **Outcome:** **IMPROVED** over the previous best (9.5985).

## 6. Week 2 - what we sent and what happened

- **Sent:** x = [0.0700, 0.0700, 0.0200, 0.0388, 0.4039, 0.0700, 0.0700, 0.8931]
- **Received:** y = 9.6374
- **GP had expected:** mu = 9.6374, sigma = 0.0032
- **Outcome:** did **not** improve over the previous best (9.7956).

## 7. The lesson

In very high dimension, expect slow steady progress. Penalise boundary artefacts so UCB does not waste queries on misleading GP uncertainty at box edges.

## 8. Summary

| | Value |
|---|---|
| Real-world task | 8-Parameter ML Model Optimisation |
| Dimensions | 8 |
| Acquisition | UCB k=2.576 (Matern nu=1.5) |
| Best before W1 | 9.5985 |
| Week 1 result | 9.7956 (improved) |
| Week 2 result | 9.6374 (no improvement) |
| Current best | 9.7956 |

*See `analysis_F8.png` in this folder for the full 9-panel visual analysis.*
