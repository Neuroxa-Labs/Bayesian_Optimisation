# F4 - Warehouse Placement (4-D) - Learn from Scratch

## 1. The big picture: what is the problem?

**Real world:** You are placing items in a warehouse; 4 factors control how efficient the layout is.

- **x** = 4 placement factors
- **y** = an efficiency score (higher = better)
- **Goal:** maximise warehouse efficiency.
- **Constraint:** every evaluation is expensive - only **one query per week**, ~13 weeks total. Choose wisely.

This is a **black box**: we never see the formula, only "input x -> output y". That is exactly what
Bayesian Optimisation is built for - finding the best of an expensive unknown function in few tries.

## 2. What we were given (30 initial points + the Week 1 point = 31 observations)

| # | x1 | x2 | x3 | x4 | y | note |
|---|---|---|---|---|---|---|
| 31 | 0.4040 | 0.4080 | 0.3381 | 0.4375 | 0.2575 | BEST |
| 28 | 0.5778 | 0.4288 | 0.4258 | 0.2490 | -4.0255 |  |
| 25 | 0.3261 | 0.4724 | 0.4532 | 0.1059 | -6.7021 |  |
| 21 | 0.6835 | 0.9028 | 0.3354 | 0.9995 | -29.4271 |  |
| 26 | 0.9484 | 0.8945 | 0.8516 | 0.5522 | -32.6257 | WORST |

- **Best so far:** y = 0.2575 at x = [0.4040, 0.4080, 0.3381, 0.4375]

## 3. What the GP learned (reading the length scales)

The Gaussian Process fits one **length scale** per dimension - how fast y changes along that axis.
A tiny length scale means "very sensitive"; a maxed-out one means "this dimension barely matters".

- `x1`: length-scale = 1.5997 -> moderate influence
- `x2`: length-scale = 1.4582 -> moderate influence
- `x3`: length-scale = 1.6336 -> moderate influence
- `x4`: length-scale = 1.4616 -> moderate influence

The GP also reports, for any point, a prediction **mu** and an uncertainty **sigma**. Where data is
dense, sigma is small (confident); in unexplored gaps, sigma is large (uncertain).

## 4. Why this acquisition function: **UCB (k=3.0)**

The landscape is **multimodal** (many local optima), so committing early is dangerous. We use the **highest exploration setting (UCB k=3.0)** to cover the space widely and avoid getting trapped in a poor basin.

## 5. Week 1 - what we sent and what happened

- **Sent:** x = [0.4040, 0.4080, 0.3381, 0.4375]
- **Received:** y = 0.2575
- **Outcome:** **IMPROVED** over the previous best (-4.0255).

## 6. Week 2 - the refined decision

- **Plan:** x = [0.4604, 0.4346, 0.2031, 0.4318]
- **GP expectation at this point:** mu = -1.0438, sigma = 0.8031
- **Reasoning:** The landscape is **multimodal** (many local optima), so committing early is dangerous. We use the **highest exploration setting (UCB k=3.0)** to cover the space widely and avoid getting trapped in a poor basin.

## 7. The lesson

In multimodal spaces, breadth beats greed early on. Week 1 jumped from a negative region to a positive one precisely because exploration was prioritised.

## 8. Summary

| | Value |
|---|---|
| Real-world task | Warehouse Placement |
| Dimensions | 4 |
| Acquisition | UCB k=3.0 (Matern nu=2.5) |
| Previous best | -4.0255 |
| Week 1 result | 0.2575 (improved) |
| Current best | 0.2575 |
| Week 2 query | [0.4604, 0.4346, 0.2031, 0.4318] |
| GP expects (W2) | mu = -1.0438 |

*See `analysis_F4.png` in this folder for the full 9-panel visual analysis.*
