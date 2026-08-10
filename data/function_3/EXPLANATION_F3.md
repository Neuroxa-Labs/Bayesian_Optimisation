# F3 - Drug Discovery - Adverse Reactions (3-D) - Learn from Scratch

## 1. The big picture: what is the problem?

**Real world:** A drug-development lab mixes 3 chemical components and measures a side-effect score.

- **x** = the 3 component ratios (x1, x2, x3)
- **y** = the negative side effect (y near 0 = safe, very negative = harmful)
- **Goal:** minimise side effects, i.e. push y as close to 0 as possible (we maximise y = -(side effect)).
- **Constraint:** every evaluation is expensive - only **one query per week**, ~13 weeks total. Choose wisely.

This is a **black box**: we never see the formula, only "input x -> output y". That is exactly what
Bayesian Optimisation is built for - finding the best of an expensive unknown function in few tries.

## 2. What we were given (15 initial points + 7 weekly queries = 22 observations)

| # | x1 | x2 | x3 | y | note |
|---|---|---|---|---|---|
| 21 | 0.4926 | 0.6916 | 0.4010 | -0.0114 | BEST |
| 22 | 0.4850 | 0.6850 | 0.4010 | -0.0145 |  |
| 17 | 0.4926 | 0.6916 | 0.4013 | -0.0203 |  |
| 16 | 0.4926 | 0.0200 | 0.6482 | -0.1685 |  |
| 7 | 0.1518 | 0.4400 | 0.9909 | -0.3989 | WORST |

- **Best so far:** y = -0.0114 at x = [0.4926, 0.6916, 0.4010]

## 3. What the GP learned (reading the length scales)

The Gaussian Process fits one **length scale** per dimension - how fast y changes along that axis.
A tiny length scale means "very sensitive"; a maxed-out one means "this dimension barely matters".

- `x1`: length-scale = 0.7609 -> moderate influence
- `x2`: length-scale = 10.0000 -> **degenerate** - GP sees little effect from this dimension (it locks it)
- `x3`: length-scale = 0.0197 -> **very sensitive** - small changes move y a lot (take small steps)

The GP also reports, for any point, a prediction **mu** and an uncertainty **sigma**. Where data is
dense, sigma is small (confident); in unexplored gaps, sigma is large (uncertain).

## 4. Why this acquisition function: **UCB (k=2.576)**

With only 15 points in 3-D, the space is sparse. **UCB k=2.576** with **narrow bounds** on sensitive dims (x3 ls=0.07: search ±0.15 around best) keeps exploration local after Week 1's boundary jump backfired.

## 5. Week 1 - what we sent and what happened

- **Sent:** x = [0.4926, 0.0200, 0.6482]
- **Received:** y = -0.1685
- **Outcome:** did **not** improve over the previous best (-0.0348) - but it is still information.

## 6. Week 2 - what we sent and what happened

- **Sent:** x = [0.4926, 0.6916, 0.4013]
- **Received:** y = -0.0203
- **Outcome:** **IMPROVED** over the previous best (-0.0348).

## 7. Week 3 - what we sent and what happened

- **Sent:** x = [0.6426, 0.6916, 0.4787]
- **Received:** y = -0.0227
- **Outcome:** did **not** improve over the previous best (-0.0203).

## 8. Week 4 - what we sent and what happened

- **Sent:** x = [0.5926, 0.7716, 0.4363]
- **Received:** y = -0.0434
- **GP had expected:** mu = -0.0434, sigma = 8.112e-05
- **Outcome:** did **not** improve over the previous best (-0.0203).

## 9. Week 5 - what we sent and what happened

- **Sent:** x = [0.4926, 0.6916, 0.4010]
- **Received:** y = -0.0223
- **GP had expected:** mu = -0.0169, sigma = 5.730e-05
- **Outcome:** did **not** improve over the previous best (-0.0203).

## 10. Week 6 - what we sent and what happened

- **Sent:** x = [0.4926, 0.6916, 0.4010]
- **Received:** y = -0.0114
- **GP had expected:** mu = -0.0169, sigma = 5.730e-05
- **Outcome:** **IMPROVED** over the previous best (-0.0203).

## 11. Week 7 - what we sent and what happened

- **Sent:** x = [0.4850, 0.6850, 0.4010]
- **Received:** y = -0.0145
- **GP had expected:** mu = -0.0145, sigma = 8.101e-05
- **Outcome:** did **not** improve over the previous best (-0.0114).

## 12. The lesson

Small length-scale dimensions are sensitive - take small steps in them. When a big jump backfires, narrow the search box around the best point instead of hugging box edges.

## 13. Summary

| | Value |
|---|---|
| Real-world task | Drug Discovery - Adverse Reactions |
| Dimensions | 3 |
| Acquisition | UCB k=2.576 (Matern nu=1.5) |
| Best before W1 | -0.0348 |
| Week 1 result | -0.1685 (no improvement) |
| Week 2 result | -0.0203 (improved) |
| Week 3 result | -0.0227 (no improvement) |
| Week 4 result | -0.0434 (no improvement) |
| Week 5 result | -0.0223 (no improvement) |
| Week 6 result | -0.0114 (improved) |
| Week 7 result | -0.0145 (no improvement) |
| Current best | -0.0114 |

*See `analysis_F3.png` in this folder for the full 9-panel visual analysis.*
