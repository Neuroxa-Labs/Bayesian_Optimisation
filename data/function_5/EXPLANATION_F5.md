# F5 - Chemical Yield Optimisation (4-D) - Learn from Scratch

## 1. The big picture: what is the problem?

**Real world:** You are optimising a chemical reaction's yield; 4 process settings control the output.

- **x** = 4 process settings
- **y** = the reaction yield (higher = better)
- **Goal:** maximise the yield (a single broad peak).
- **Constraint:** every evaluation is expensive - only **one query per week**, ~13 weeks total. Choose wisely.

This is a **black box**: we never see the formula, only "input x -> output y". That is exactly what
Bayesian Optimisation is built for - finding the best of an expensive unknown function in few tries.

## 2. What we were given (20 initial points + 7 weekly queries = 27 observations)

| # | x1 | x2 | x3 | x4 | y | note |
|---|---|---|---|---|---|---|
| 27 | 0.3800 | 0.9800 | 0.9800 | 0.9800 | 3743.8291 |  |
| 24 | 0.3800 | 0.9800 | 0.9800 | 0.9800 | 3743.8291 | BEST |
| 26 | 0.3600 | 0.9800 | 0.9800 | 0.9800 | 3729.8367 |  |
| 4 | 0.7061 | 0.5342 | 0.2642 | 0.4821 | 4.2109 |  |
| 3 | 0.4383 | 0.8043 | 0.2102 | 0.1513 | 0.1129 | WORST |

- **Best so far:** y = 3743.8291 at x = [0.3800, 0.9800, 0.9800, 0.9800]

## 3. What the GP learned (reading the length scales)

The Gaussian Process fits one **length scale** per dimension - how fast y changes along that axis.
A tiny length scale means "very sensitive"; a maxed-out one means "this dimension barely matters".

- `x1`: length-scale = 10.0000 -> **degenerate** - GP sees little effect from this dimension (it locks it)
- `x2`: length-scale = 0.8016 -> moderate influence
- `x3`: length-scale = 0.6219 -> moderate influence
- `x4`: length-scale = 4.1498 -> moderate influence

The GP also reports, for any point, a prediction **mu** and an uncertainty **sigma**. Where data is
dense, sigma is small (confident); in unexplored gaps, sigma is large (uncertain).

## 4. Why this acquisition function: **UCB (k=1.0)**

This function has one broad peak, so the strategy is **find the signal, then exploit**. Once the best value crossed the signal threshold, the model dropped to a low-k UCB and now climbs the peak. An **anti-duplicate guard** stops it re-sending a point we already measured: instead it does a local UCB search around the peak.

## 5. Week 1 - what we sent and what happened

- **Sent:** x = [0.2242, 0.8465, 0.9800, 0.9800]
- **Received:** y = 2497.3155
- **Outcome:** **IMPROVED** over the previous best (1088.8596).

## 6. Week 2 - what we sent and what happened

- **Sent:** x = [0.0742, 0.6965, 0.9800, 0.9800]
- **Received:** y = 1811.0568
- **Outcome:** did **not** improve over the previous best (2497.3155).

## 7. Week 3 - what we sent and what happened

- **Sent:** x = [0.1500, 0.9265, 0.9800, 0.9800]
- **Received:** y = 3108.4879
- **Outcome:** **IMPROVED** over the previous best (2497.3155).

## 8. Week 4 - what we sent and what happened

- **Sent:** x = [0.3800, 0.9800, 0.9800, 0.9800]
- **Received:** y = 3743.8291
- **GP had expected:** mu = 3742.7062, sigma = 0.8624
- **Outcome:** **IMPROVED** over the previous best (3108.4879).

## 9. Week 5 - what we sent and what happened

- **Sent:** x = [0.2800, 0.9800, 0.9800, 0.9800]
- **Received:** y = 3692.5200
- **GP had expected:** mu = 3692.0113, sigma = 1.3684
- **Outcome:** did **not** improve over the previous best (3743.8291).

## 10. Week 6 - what we sent and what happened

- **Sent:** x = [0.3600, 0.9800, 0.9800, 0.9800]
- **Received:** y = 3729.8367
- **GP had expected:** mu = 3732.5683, sigma = 0.7224
- **Outcome:** did **not** improve over the previous best (3743.8291).

## 11. Week 7 - what we sent and what happened

- **Sent:** x = [0.3800, 0.9800, 0.9800, 0.9800]
- **Received:** y = 3743.8291
- **GP had expected:** mu = 3742.7062, sigma = 0.8624
- **Outcome:** did **not** improve over the previous best (3743.8291).

## 12. The lesson

Exploitation must keep producing NEW information. Re-querying the exact best point wastes a week - so local search around the peak (with the same acquisition) is the right way to climb.

## 13. Summary

| | Value |
|---|---|
| Real-world task | Chemical Yield Optimisation |
| Dimensions | 4 |
| Acquisition | UCB k=1.0 (Matern nu=2.5) |
| Best before W1 | 1088.8596 |
| Week 1 result | 2497.3155 (improved) |
| Week 2 result | 1811.0568 (no improvement) |
| Week 3 result | 3108.4879 (improved) |
| Week 4 result | 3743.8291 (improved) |
| Week 5 result | 3692.5200 (no improvement) |
| Week 6 result | 3729.8367 (no improvement) |
| Week 7 result | 3743.8291 (no improvement) |
| Current best | 3743.8291 |

*See `analysis_F5.png` in this folder for the full 9-panel visual analysis.*
