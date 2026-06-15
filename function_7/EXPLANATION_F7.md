# F7 - ML Hyperparameter Tuning (6-D) - Learn from Scratch

## 1. The big picture: what is the problem?

**Real world:** You are tuning 6 hyperparameters of a machine-learning model.

- **x** = 6 hyperparameters
- **y** = a validation score (higher = better)
- **Goal:** maximise the validation score.
- **Constraint:** every evaluation is expensive - only **one query per week**, ~13 weeks total. Choose wisely.

This is a **black box**: we never see the formula, only "input x -> output y". That is exactly what
Bayesian Optimisation is built for - finding the best of an expensive unknown function in few tries.

## 2. What we were given (30 initial points + 3 weekly queries = 33 observations)

| # | x1 | x2 | x3 | x4 | x5 | x6 | y | note |
|---|---|---|---|---|---|---|---|---|
| 33 | 0.0700 | 0.4917 | 0.2474 | 0.1674 | 0.3539 | 0.7156 | 1.5253 | BEST |
| 31 | 0.0200 | 0.4917 | 0.2474 | 0.2174 | 0.3780 | 0.7465 | 1.4506 |  |
| 7 | 0.0579 | 0.4917 | 0.2474 | 0.2181 | 0.4204 | 0.7310 | 1.3650 |  |
| 28 | 0.8469 | 0.1424 | 0.0607 | 0.7563 | 0.5524 | 0.0813 | 0.0031 |  |
| 20 | 0.8799 | 0.3980 | 0.0036 | 0.9570 | 0.2645 | 0.1149 | 0.0027 | WORST |

- **Best so far:** y = 1.5253 at x = [0.0700, 0.4917, 0.2474, 0.1674, 0.3539, 0.7156]

## 3. What the GP learned (reading the length scales)

The Gaussian Process fits one **length scale** per dimension - how fast y changes along that axis.
A tiny length scale means "very sensitive"; a maxed-out one means "this dimension barely matters".

- `x1`: length-scale = 1.0535 -> moderate influence
- `x2`: length-scale = 2.9150 -> moderate influence
- `x3`: length-scale = 10.0000 -> **degenerate** - GP sees little effect from this dimension (it locks it)
- `x4`: length-scale = 0.4492 -> **very sensitive** - small changes move y a lot (take small steps)
- `x5`: length-scale = 0.2268 -> **very sensitive** - small changes move y a lot (take small steps)
- `x6`: length-scale = 0.2540 -> **very sensitive** - small changes move y a lot (take small steps)

The GP also reports, for any point, a prediction **mu** and an uncertainty **sigma**. Where data is
dense, sigma is small (confident); in unexplored gaps, sigma is large (uncertain).

## 4. Why this acquisition function: **EI**

High dimension means the space is large and easy to over-commit in. **EI** keeps a careful balance; jumping to exploitation too early would risk locking onto a local optimum before the space is mapped.

## 5. Week 1 - what we sent and what happened

- **Sent:** x = [0.0200, 0.4917, 0.2474, 0.2174, 0.3780, 0.7465]
- **Received:** y = 1.4506
- **Outcome:** **IMPROVED** over the previous best (1.3650).

## 6. Week 2 - what we sent and what happened

- **Sent:** x = [0.0200, 0.4917, 0.2474, 0.2146, 0.3772, 0.8061]
- **Received:** y = 1.2983
- **Outcome:** did **not** improve over the previous best (1.4506).

## 7. Week 3 - what we sent and what happened

- **Sent:** x = [0.0700, 0.4917, 0.2474, 0.1674, 0.3539, 0.7156]
- **Received:** y = 1.5253
- **GP had expected:** mu = 1.5253, sigma = 4.515e-04
- **Outcome:** **IMPROVED** over the previous best (1.4506).

## 8. The lesson

In 6-D, patience matters. Small, reliable improvements accumulate; aggressive exploitation is a trap until more of the space is known.

## 9. Summary

| | Value |
|---|---|
| Real-world task | ML Hyperparameter Tuning |
| Dimensions | 6 |
| Acquisition | EI (Matern nu=2.5) |
| Best before W1 | 1.3650 |
| Week 1 result | 1.4506 (improved) |
| Week 2 result | 1.2983 (no improvement) |
| Week 3 result | 1.5253 (improved) |
| Current best | 1.5253 |

*See `analysis_F7.png` in this folder for the full 9-panel visual analysis.*
