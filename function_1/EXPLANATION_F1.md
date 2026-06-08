# F1 - Radiation Source Detection (2-D) - Learn from Scratch

## 1. The big picture: what is the problem?

**Real world:** You are sweeping a 2-D field to locate a hidden radioactive source with a Geiger counter.

- **x** = the (x1, x2) position on the map
- **y** = the counter reading (higher = closer to the source)
- **Goal:** find the position with the strongest reading (the hidden source).
- **Constraint:** every evaluation is expensive - only **one query per week**, ~13 weeks total. Choose wisely.

This is a **black box**: we never see the formula, only "input x -> output y". That is exactly what
Bayesian Optimisation is built for - finding the best of an expensive unknown function in few tries.

## 2. What we were given (10 initial points + 2 weekly queries = 12 observations)

| # | x1 | x2 | y | note |
|---|---|---|---|---|
| 3 | 0.7310 | 0.7330 | 7.711e-16 | BEST |
| 8 | 0.6834 | 0.8611 | 2.535e-40 |  |
| 2 | 0.5743 | 0.8799 | 1.033e-46 |  |
| 5 | 0.6501 | 0.6815 | -0.0036 |  |
| 12 | 0.4211 | 0.4636 | -0.0066 | WORST |

- **Best so far:** y = 7.711e-16 at x = [0.7310, 0.7330]

## 3. What the GP learned (reading the length scales)

The Gaussian Process fits one **length scale** per dimension - how fast y changes along that axis.
A tiny length scale means "very sensitive"; a maxed-out one means "this dimension barely matters".

- `x1`: length-scale = 10.0000 -> **degenerate** - GP sees little effect from this dimension (it locks it)
- `x2`: length-scale = 0.0183 -> **very sensitive** - small changes move y a lot (take small steps)

The GP also reports, for any point, a prediction **mu** and an uncertainty **sigma**. Where data is
dense, sigma is small (confident); in unexplored gaps, sigma is large (uncertain).

## 4. Why this acquisition function: **COVERAGE**

The peak is sharp and sparse: almost every reading is 0. With no signal, use **coverage-based exploration** (farthest from existing points) plus a boundary penalty - GP uncertainty at box edges is misleading.

## 5. Week 1 - what we sent and what happened

- **Sent:** x = [0.1964, 0.9707]
- **Received:** y = 4.846e-214
- **Outcome:** did **not** improve over the previous best (7.711e-16) - but it is still information.

## 6. Week 2 - what we sent and what happened

- **Sent:** x = [0.4211, 0.4636]
- **Received:** y = -0.0066
- **GP had expected:** mu = -0.0066, sigma = 2.004e-09
- **Outcome:** did **not** improve over the previous best (7.711e-16).

## 7. The lesson

A zero is not failure - it is elimination. Avoid boundary artefacts; scan the largest interior gaps. nu=0.5 models a rough, spiky surface.

## 8. Summary

| | Value |
|---|---|
| Real-world task | Radiation Source Detection |
| Dimensions | 2 |
| Acquisition | COVERAGE (Matern nu=0.5) |
| Best before W1 | 7.711e-16 |
| Week 1 result | 4.846e-214 (no improvement) |
| Week 2 result | -0.0066 (no improvement) |
| Current best | 7.711e-16 |

*See `analysis_F1.png` in this folder for the full 9-panel visual analysis.*
