# F2 - Noisy ML Log-Likelihood (2-D) - Learn from Scratch

## 1. The big picture: what is the problem?

**Real world:** You are tuning a machine-learning model whose validation log-likelihood is measured with noise.

- **x** = 2 model settings
- **y** = a noisy log-likelihood score (higher = better)
- **Goal:** maximise the (noisy) log-likelihood.
- **Constraint:** every evaluation is expensive - only **one query per week**, ~13 weeks total. Choose wisely.

This is a **black box**: we never see the formula, only "input x -> output y". That is exactly what
Bayesian Optimisation is built for - finding the best of an expensive unknown function in few tries.

## 2. What we were given (10 initial points + the Week 1 point = 11 observations)

| # | x1 | x2 | y | note |
|---|---|---|---|---|
| 10 | 0.7026 | 0.9266 | 0.6112 | BEST |
| 1 | 0.6658 | 0.1240 | 0.5390 |  |
| 11 | 0.6948 | 0.9266 | 0.4898 |  |
| 9 | 0.3386 | 0.2139 | -0.0139 |  |
| 3 | 0.1427 | 0.3490 | -0.0656 | WORST |

- **Best so far:** y = 0.6112 at x = [0.7026, 0.9266]

## 3. What the GP learned (reading the length scales)

The Gaussian Process fits one **length scale** per dimension - how fast y changes along that axis.
A tiny length scale means "very sensitive"; a maxed-out one means "this dimension barely matters".

- `x1`: length-scale = 0.0691 -> **very sensitive** - small changes move y a lot (take small steps)
- `x2`: length-scale = 10.0000 -> **degenerate** - GP sees little effect from this dimension (it locks it)

The GP also reports, for any point, a prediction **mu** and an uncertainty **sigma**. Where data is
dense, sigma is small (confident); in unexplored gaps, sigma is large (uncertain).

## 4. Why this acquisition function: **EI**

Because the signal is noisy, a single low reading does not mean a region is bad. **EI with a White noise kernel** is robust: it weighs both the probability and the size of an improvement, and the White kernel absorbs measurement noise so the GP is not fooled by it.

## 5. Week 1 - what we sent and what happened

- **Sent:** x = [0.6948, 0.9266]
- **Received:** y = 0.4898
- **Outcome:** did **not** improve over the previous best (0.6112) - but it is still information.

## 6. Week 2 - the refined decision

- **Plan:** x = [0.7343, 0.9266]
- **GP expectation at this point:** mu = 0.4941, sigma = 0.1283
- **Reasoning:** Because the signal is noisy, a single low reading does not mean a region is bad. **EI with a White noise kernel** is robust: it weighs both the probability and the size of an improvement, and the White kernel absorbs measurement noise so the GP is not fooled by it.

## 7. The lesson

Treat noise as noise. Do not abandon a promising region after one unlucky sample - keep sampling near the known-good area.

## 8. Summary

| | Value |
|---|---|
| Real-world task | Noisy ML Log-Likelihood |
| Dimensions | 2 |
| Acquisition | EI (Matern nu=2.5) |
| Previous best | 0.6112 |
| Week 1 result | 0.4898 (no improvement) |
| Current best | 0.6112 |
| Week 2 query | [0.7343, 0.9266] |
| GP expects (W2) | mu = 0.4941 |

*See `analysis_F2.png` in this folder for the full 9-panel visual analysis.*
