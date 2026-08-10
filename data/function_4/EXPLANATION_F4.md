# F4 - Warehouse Placement (4-D) - Learn from Scratch

## 1. The big picture: what is the problem?

**Real world:** You are placing items in a warehouse; 4 factors control how efficient the layout is.

- **x** = 4 placement factors
- **y** = an efficiency score (higher = better)
- **Goal:** maximise warehouse efficiency.
- **Constraint:** every evaluation is expensive - only **one query per week**, ~13 weeks total. Choose wisely.

This is a **black box**: we never see the formula, only "input x -> output y". That is exactly what
Bayesian Optimisation is built for - finding the best of an expensive unknown function in few tries.

## 2. What we were given (30 initial points + 7 weekly queries = 37 observations)

| # | x1 | x2 | x3 | x4 | y | note |
|---|---|---|---|---|---|---|
| 36 | 0.4008 | 0.4135 | 0.3767 | 0.4061 | 0.4695 | BEST |
| 37 | 0.3950 | 0.4200 | 0.3800 | 0.4100 | 0.4637 |  |
| 31 | 0.4040 | 0.4080 | 0.3381 | 0.4375 | 0.2575 |  |
| 21 | 0.6835 | 0.9028 | 0.3354 | 0.9995 | -29.4271 |  |
| 26 | 0.9484 | 0.8945 | 0.8516 | 0.5522 | -32.6257 | WORST |

- **Best so far:** y = 0.4695 at x = [0.4008, 0.4135, 0.3767, 0.4061]

## 3. What the GP learned (reading the length scales)

The Gaussian Process fits one **length scale** per dimension - how fast y changes along that axis.
A tiny length scale means "very sensitive"; a maxed-out one means "this dimension barely matters".

- `x1`: length-scale = 1.3555 -> moderate influence
- `x2`: length-scale = 1.3236 -> moderate influence
- `x3`: length-scale = 1.1443 -> moderate influence
- `x4`: length-scale = 1.2790 -> moderate influence

The GP also reports, for any point, a prediction **mu** and an uncertainty **sigma**. Where data is
dense, sigma is small (confident); in unexplored gaps, sigma is large (uncertain).

## 4. Why this acquisition function: **UCB (k=3.0)**

The landscape is **multimodal** (many local optima), so committing early is dangerous. We use the **highest exploration setting (UCB k=3.0)** to cover the space widely and avoid getting trapped in a poor basin.

## 5. Week 1 - what we sent and what happened

- **Sent:** x = [0.4040, 0.4080, 0.3381, 0.4375]
- **Received:** y = 0.2575
- **Outcome:** **IMPROVED** over the previous best (-4.0255).

## 6. Week 2 - what we sent and what happened

- **Sent:** x = [0.4604, 0.4346, 0.2031, 0.4318]
- **Received:** y = -3.3056
- **Outcome:** did **not** improve over the previous best (0.2575).

## 7. Week 3 - what we sent and what happened

- **Sent:** x = [0.3440, 0.4539, 0.3981, 0.4339]
- **Received:** y = -0.1262
- **Outcome:** did **not** improve over the previous best (0.2575).

## 8. Week 4 - what we sent and what happened

- **Sent:** x = [0.4141, 0.3859, 0.3781, 0.4415]
- **Received:** y = 0.1660
- **GP had expected:** mu = 0.2441, sigma = 0.0821
- **Outcome:** did **not** improve over the previous best (0.2575).

## 9. Week 5 - what we sent and what happened

- **Sent:** x = [0.4258, 0.4396, 0.3811, 0.4370]
- **Received:** y = 0.2403
- **GP had expected:** mu = 0.2528, sigma = 0.0817
- **Outcome:** did **not** improve over the previous best (0.2575).

## 10. Week 6 - what we sent and what happened

- **Sent:** x = [0.4008, 0.4135, 0.3767, 0.4061]
- **Received:** y = 0.4695
- **GP had expected:** mu = 0.4238, sigma = 0.0604
- **Outcome:** **IMPROVED** over the previous best (0.2575).

## 11. Week 7 - what we sent and what happened

- **Sent:** x = [0.3950, 0.4200, 0.3800, 0.4100]
- **Received:** y = 0.4637
- **GP had expected:** mu = 0.4178, sigma = 0.0548
- **Outcome:** did **not** improve over the previous best (0.4695).

## 12. The lesson

In multimodal spaces, breadth beats greed early on. Week 1 jumped from a negative region to a positive one precisely because exploration was prioritised.

## 13. Summary

| | Value |
|---|---|
| Real-world task | Warehouse Placement |
| Dimensions | 4 |
| Acquisition | UCB k=3.0 (Matern nu=2.5) |
| Best before W1 | -4.0255 |
| Week 1 result | 0.2575 (improved) |
| Week 2 result | -3.3056 (no improvement) |
| Week 3 result | -0.1262 (no improvement) |
| Week 4 result | 0.1660 (no improvement) |
| Week 5 result | 0.2403 (no improvement) |
| Week 6 result | 0.4695 (improved) |
| Week 7 result | 0.4637 (no improvement) |
| Current best | 0.4695 |

*See `analysis_F4.png` in this folder for the full 9-panel visual analysis.*
