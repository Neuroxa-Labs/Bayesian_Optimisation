# F2 - Noisy ML Log-Likelihood (2-D) - Learn from Scratch

## 1. The big picture: what is the problem?

**Real world:** You are tuning a machine-learning model whose validation log-likelihood is measured with noise.

- **x** = 2 model settings
- **y** = a noisy log-likelihood score (higher = better)
- **Goal:** maximise the (noisy) log-likelihood.
- **Constraint:** every evaluation is expensive - only **one query per week**, ~13 weeks total. Choose wisely.

This is a **black box**: we never see the formula, only "input x -> output y". That is exactly what
Bayesian Optimisation is built for - finding the best of an expensive unknown function in few tries.

## 2. What we were given (10 initial points + 7 weekly queries = 17 observations)

| # | x1 | x2 | y | note |
|---|---|---|---|---|
| 15 | 0.7179 | 0.0200 | 0.7766 | BEST |
| 14 | 0.7000 | 0.0200 | 0.6599 |  |
| 10 | 0.7026 | 0.9266 | 0.6112 |  |
| 9 | 0.3386 | 0.2139 | -0.0139 |  |
| 3 | 0.1427 | 0.3490 | -0.0656 | WORST |

- **Best so far:** y = 0.7766 at x = [0.7179, 0.0200]

## 3. What the GP learned (reading the length scales)

The Gaussian Process fits one **length scale** per dimension - how fast y changes along that axis.
A tiny length scale means "very sensitive"; a maxed-out one means "this dimension barely matters".

- `x1`: length-scale = 0.0894 -> **very sensitive** - small changes move y a lot (take small steps)
- `x2`: length-scale = 10.0000 -> **degenerate** - GP sees little effect from this dimension (it locks it)

The GP also reports, for any point, a prediction **mu** and an uncertainty **sigma**. Where data is
dense, sigma is small (confident); in unexplored gaps, sigma is large (uncertain).

## 4. Why this acquisition function: **EI**

Because the signal is noisy, a single low reading does not mean a region is bad. **EI with a White noise kernel** is robust: it weighs both the probability and the size of an improvement, and the White kernel absorbs measurement noise so the GP is not fooled by it.

## 5. Week 1 - what we sent and what happened

- **Sent:** x = [0.6948, 0.9266]
- **Received:** y = 0.4898
- **Outcome:** did **not** improve over the previous best (0.6112) - but it is still information.

## 6. Week 2 - what we sent and what happened

- **Sent:** x = [0.7343, 0.9266]
- **Received:** y = 0.5706
- **Outcome:** did **not** improve over the previous best (0.6112).

## 7. Week 3 - what we sent and what happened

- **Sent:** x = [0.7188, 0.9266]
- **Received:** y = 0.6022
- **Outcome:** did **not** improve over the previous best (0.6112).

## 8. Week 4 - what we sent and what happened

- **Sent:** x = [0.7000, 0.0200]
- **Received:** y = 0.6599
- **GP had expected:** mu = 0.6121, sigma = 0.0881
- **Outcome:** **IMPROVED** over the previous best (0.6112).

## 9. Week 5 - what we sent and what happened

- **Sent:** x = [0.7179, 0.0200]
- **Received:** y = 0.7766
- **GP had expected:** mu = 0.6028, sigma = 0.0869
- **Outcome:** **IMPROVED** over the previous best (0.6599).

## 10. Week 6 - what we sent and what happened

- **Sent:** x = [0.7500, 0.0200]
- **Received:** y = 0.4035
- **GP had expected:** mu = 0.4778, sigma = 0.0977
- **Outcome:** did **not** improve over the previous best (0.7766).

## 11. Week 7 - what we sent and what happened

- **Sent:** x = [0.7200, 0.0200]
- **Received:** y = 0.5074
- **GP had expected:** mu = 0.5982, sigma = 0.0870
- **Outcome:** did **not** improve over the previous best (0.7766).

## 12. The lesson

Treat noise as noise. Do not abandon a promising region after one unlucky sample - keep sampling near the known-good area.

## 13. Summary

| | Value |
|---|---|
| Real-world task | Noisy ML Log-Likelihood |
| Dimensions | 2 |
| Acquisition | EI (Matern nu=2.5) |
| Best before W1 | 0.6112 |
| Week 1 result | 0.4898 (no improvement) |
| Week 2 result | 0.5706 (no improvement) |
| Week 3 result | 0.6022 (no improvement) |
| Week 4 result | 0.6599 (improved) |
| Week 5 result | 0.7766 (improved) |
| Week 6 result | 0.4035 (no improvement) |
| Week 7 result | 0.5074 (no improvement) |
| Current best | 0.7766 |

*See `analysis_F2.png` in this folder for the full 9-panel visual analysis.*
