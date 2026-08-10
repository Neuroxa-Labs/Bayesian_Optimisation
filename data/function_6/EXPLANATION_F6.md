# F6 - Cake Recipe Optimisation (5-D) - Learn from Scratch

## 1. The big picture: what is the problem?

**Real world:** You are perfecting a cake recipe defined by 5 ingredient amounts; a judge scores how bad it is.

- **x** = 5 ingredient amounts
- **y** = the negative badness (y near 0 = great cake)
- **Goal:** minimise badness, i.e. push y toward 0 (we maximise y = -(badness)).
- **Constraint:** every evaluation is expensive - only **one query per week**, ~13 weeks total. Choose wisely.

This is a **black box**: we never see the formula, only "input x -> output y". That is exactly what
Bayesian Optimisation is built for - finding the best of an expensive unknown function in few tries.

## 2. What we were given (20 initial points + 7 weekly queries = 27 observations)

| # | x1 | x2 | x3 | x4 | x5 | y | note |
|---|---|---|---|---|---|---|---|
| 26 | 0.4400 | 0.2500 | 0.5900 | 0.7300 | 0.1300 | -0.2404 | BEST |
| 25 | 0.4300 | 0.2400 | 0.5800 | 0.7200 | 0.1200 | -0.2654 |  |
| 27 | 0.4450 | 0.2550 | 0.5950 | 0.7350 | 0.1350 | -0.2672 |  |
| 19 | 0.9218 | 0.9319 | 0.4149 | 0.5951 | 0.7356 | -2.1558 |  |
| 9 | 0.1257 | 0.8627 | 0.0285 | 0.2466 | 0.7512 | -2.5712 | WORST |

- **Best so far:** y = -0.2404 at x = [0.4400, 0.2500, 0.5900, 0.7300, 0.1300]

## 3. What the GP learned (reading the length scales)

The Gaussian Process fits one **length scale** per dimension - how fast y changes along that axis.
A tiny length scale means "very sensitive"; a maxed-out one means "this dimension barely matters".

- `x1`: length-scale = 1.3126 -> moderate influence
- `x2`: length-scale = 1.0494 -> moderate influence
- `x3`: length-scale = 10.0000 -> **degenerate** - GP sees little effect from this dimension (it locks it)
- `x4`: length-scale = 0.3539 -> **very sensitive** - small changes move y a lot (take small steps)
- `x5`: length-scale = 0.0656 -> **very sensitive** - small changes move y a lot (take small steps)

The GP also reports, for any point, a prediction **mu** and an uncertainty **sigma**. Where data is
dense, sigma is small (confident); in unexplored gaps, sigma is large (uncertain).

## 4. Why this acquisition function: **EI**

In 5-D a balanced search pays off. **EI** gives a measured explore/exploit trade-off and steadily nudges toward 0 without over-committing to one region too soon.

## 5. Week 1 - what we sent and what happened

- **Sent:** x = [0.4656, 0.2431, 0.5775, 0.9800, 0.0200]
- **Received:** y = -0.4775
- **Outcome:** **IMPROVED** over the previous best (-0.7143).

## 6. Week 2 - what we sent and what happened

- **Sent:** x = [0.5171, 0.2822, 0.7714, 0.9800, 0.2075]
- **Received:** y = -0.5782
- **Outcome:** did **not** improve over the previous best (-0.4775).

## 7. Week 3 - what we sent and what happened

- **Sent:** x = [0.5241, 0.3609, 0.4138, 0.8977, 0.0200]
- **Received:** y = -0.5377
- **Outcome:** did **not** improve over the previous best (-0.4775).

## 8. Week 4 - what we sent and what happened

- **Sent:** x = [0.3656, 0.1431, 0.4775, 0.9300, 0.1200]
- **Received:** y = -0.6062
- **GP had expected:** mu = -0.6062, sigma = 6.126e-04
- **Outcome:** did **not** improve over the previous best (-0.4775).

## 9. Week 5 - what we sent and what happened

- **Sent:** x = [0.4300, 0.2400, 0.5800, 0.7200, 0.1200]
- **Received:** y = -0.2654
- **GP had expected:** mu = -0.2654, sigma = 6.125e-04
- **Outcome:** **IMPROVED** over the previous best (-0.4775).

## 10. Week 6 - what we sent and what happened

- **Sent:** x = [0.4400, 0.2500, 0.5900, 0.7300, 0.1300]
- **Received:** y = -0.2404
- **GP had expected:** mu = -0.2404, sigma = 6.118e-04
- **Outcome:** **IMPROVED** over the previous best (-0.2654).

## 11. Week 7 - what we sent and what happened

- **Sent:** x = [0.4450, 0.2550, 0.5950, 0.7350, 0.1350]
- **Received:** y = -0.2672
- **GP had expected:** mu = -0.2672, sigma = 6.122e-04
- **Outcome:** did **not** improve over the previous best (-0.2404).

## 12. The lesson

In medium dimension, steady incremental gains are the norm. EI's balance avoids both blind wandering and premature exploitation.

## 13. Summary

| | Value |
|---|---|
| Real-world task | Cake Recipe Optimisation |
| Dimensions | 5 |
| Acquisition | EI (Matern nu=2.5) |
| Best before W1 | -0.7143 |
| Week 1 result | -0.4775 (improved) |
| Week 2 result | -0.5782 (no improvement) |
| Week 3 result | -0.5377 (no improvement) |
| Week 4 result | -0.6062 (no improvement) |
| Week 5 result | -0.2654 (improved) |
| Week 6 result | -0.2404 (improved) |
| Week 7 result | -0.2672 (no improvement) |
| Current best | -0.2404 |

*See `analysis_F6.png` in this folder for the full 9-panel visual analysis.*
