# F6 - Cake Recipe Optimisation (5-D) - Learn from Scratch

## 1. The big picture: what is the problem?

**Real world:** You are perfecting a cake recipe defined by 5 ingredient amounts; a judge scores how bad it is.

- **x** = 5 ingredient amounts
- **y** = the negative badness (y near 0 = great cake)
- **Goal:** minimise badness, i.e. push y toward 0 (we maximise y = -(badness)).
- **Constraint:** every evaluation is expensive - only **one query per week**, ~13 weeks total. Choose wisely.

This is a **black box**: we never see the formula, only "input x -> output y". That is exactly what
Bayesian Optimisation is built for - finding the best of an expensive unknown function in few tries.

## 2. What we were given (20 initial points + the Week 1 point = 21 observations)

| # | x1 | x2 | x3 | x4 | x5 | y | note |
|---|---|---|---|---|---|---|---|
| 21 | 0.4656 | 0.2431 | 0.5775 | 0.9800 | 0.0200 | -0.4775 | BEST |
| 1 | 0.7282 | 0.1547 | 0.7326 | 0.6940 | 0.0564 | -0.7143 |  |
| 5 | 0.6188 | 0.3318 | 0.1873 | 0.7562 | 0.3288 | -0.8292 |  |
| 19 | 0.9218 | 0.9319 | 0.4149 | 0.5951 | 0.7356 | -2.1558 |  |
| 9 | 0.1257 | 0.8627 | 0.0285 | 0.2466 | 0.7512 | -2.5712 | WORST |

- **Best so far:** y = -0.4775 at x = [0.4656, 0.2431, 0.5775, 0.9800, 0.0200]

## 3. What the GP learned (reading the length scales)

The Gaussian Process fits one **length scale** per dimension - how fast y changes along that axis.
A tiny length scale means "very sensitive"; a maxed-out one means "this dimension barely matters".

- `x1`: length-scale = 0.5380 -> moderate influence
- `x2`: length-scale = 0.9808 -> moderate influence
- `x3`: length-scale = 1.1503 -> moderate influence
- `x4`: length-scale = 1.2474 -> moderate influence
- `x5`: length-scale = 0.9971 -> moderate influence

The GP also reports, for any point, a prediction **mu** and an uncertainty **sigma**. Where data is
dense, sigma is small (confident); in unexplored gaps, sigma is large (uncertain).

## 4. Why this acquisition function: **EI**

In 5-D a balanced search pays off. **EI** gives a measured explore/exploit trade-off and steadily nudges toward 0 without over-committing to one region too soon.

## 5. Week 1 - what we sent and what happened

- **Sent:** x = [0.4656, 0.2431, 0.5775, 0.9800, 0.0200]
- **Received:** y = -0.4775
- **Outcome:** **IMPROVED** over the previous best (-0.7143).

## 6. Week 2 - the refined decision

- **Plan:** x = [0.5171, 0.2822, 0.7714, 0.9800, 0.2075]
- **GP expectation at this point:** mu = -0.5058, sigma = 0.1678
- **Reasoning:** In 5-D a balanced search pays off. **EI** gives a measured explore/exploit trade-off and steadily nudges toward 0 without over-committing to one region too soon.

## 7. The lesson

In medium dimension, steady incremental gains are the norm. EI's balance avoids both blind wandering and premature exploitation.

## 8. Summary

| | Value |
|---|---|
| Real-world task | Cake Recipe Optimisation |
| Dimensions | 5 |
| Acquisition | EI (Matern nu=2.5) |
| Previous best | -0.7143 |
| Week 1 result | -0.4775 (improved) |
| Current best | -0.4775 |
| Week 2 query | [0.5171, 0.2822, 0.7714, 0.9800, 0.2075] |
| GP expects (W2) | mu = -0.5058 |

*See `analysis_F6.png` in this folder for the full 9-panel visual analysis.*
