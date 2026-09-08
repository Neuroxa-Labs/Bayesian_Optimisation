# F6 — Cake Recipe Optimisation (5-D)

## 1. The big picture

**Real world:** You are perfecting a cake recipe defined by 5 ingredient amounts; a judge scores how bad it is.

- **x** = 5 ingredient amounts
- **y** = the negative badness (y near 0 = great cake)
- **Goal:** minimise badness, i.e. push y toward 0 (we maximise y = -(badness)).
- **Constraint:** one query per function per week (Stage 2 budget).

This is a **black box**: we never see the formula, only input → output. Bayesian optimisation
(GP + acquisition) is designed for exactly that setting.

## 2. Data so far (20 seed points + 12 weekly queries = 32 observations)

| # | x1 | x2 | x3 | x4 | x5 | y | note |
|---|---|---|---|---|---|---|---|
| 30 | 0.4410 | 0.2490 | 0.5910 | 0.7290 | 0.1310 | -0.1360 | BEST |
| 32 | 0.4400 | 0.2500 | 0.5900 | 0.7280 | 0.1320 | -0.2054 |  |
| 26 | 0.4400 | 0.2500 | 0.5900 | 0.7300 | 0.1300 | -0.2404 |  |
| 19 | 0.9218 | 0.9319 | 0.4149 | 0.5951 | 0.7356 | -2.1558 |  |
| 9 | 0.1257 | 0.8627 | 0.0285 | 0.2466 | 0.7512 | -2.5712 | WORST |

- **Best so far:** y = -0.1360 at x = [0.4410, 0.2490, 0.5910, 0.7290, 0.1310]

## 3. What the GP learned (ARD length scales)

- `x1`: length-scale = 0.0100 → **very sensitive** — small changes move y a lot
- `x2`: length-scale = 0.0100 → **very sensitive** — small changes move y a lot
- `x3`: length-scale = 0.0100 → **very sensitive** — small changes move y a lot
- `x4`: length-scale = 0.0100 → **very sensitive** — small changes move y a lot
- `x5`: length-scale = 0.0327 → **very sensitive** — small changes move y a lot

## 4. Acquisition / late policy: **EI**

A sharp interior basin. Week 10 set the incumbent; a small off-centroid step collapsed the score — later weeks hard-return toward that centroid.

## 5. Week 1 — what we sent and what happened

- **Sent:** x = [0.4656, 0.2431, 0.5775, 0.9800, 0.0200]
- **Received:** y = -0.4775
- **Outcome:** **IMPROVED** over the previous best (-0.7143).

## 6. Week 2 — what we sent and what happened

- **Sent:** x = [0.5171, 0.2822, 0.7714, 0.9800, 0.2075]
- **Received:** y = -0.5782
- **Outcome:** did **not** improve over the previous best (-0.4775).

## 7. Week 3 — what we sent and what happened

- **Sent:** x = [0.5241, 0.3609, 0.4138, 0.8977, 0.0200]
- **Received:** y = -0.5377
- **Outcome:** did **not** improve over the previous best (-0.4775).

## 8. Week 4 — what we sent and what happened

- **Sent:** x = [0.3656, 0.1431, 0.4775, 0.9300, 0.1200]
- **Received:** y = -0.6062
- **Outcome:** did **not** improve over the previous best (-0.4775).

## 9. Week 5 — what we sent and what happened

- **Sent:** x = [0.4300, 0.2400, 0.5800, 0.7200, 0.1200]
- **Received:** y = -0.2654
- **Outcome:** **IMPROVED** over the previous best (-0.4775).

## 10. Week 6 — what we sent and what happened

- **Sent:** x = [0.4400, 0.2500, 0.5900, 0.7300, 0.1300]
- **Received:** y = -0.2404
- **Outcome:** **IMPROVED** over the previous best (-0.2654).

## 11. Week 7 — what we sent and what happened

- **Sent:** x = [0.4450, 0.2550, 0.5950, 0.7350, 0.1350]
- **Received:** y = -0.2672
- **Outcome:** did **not** improve over the previous best (-0.2404).

## 12. Week 8 — what we sent and what happened

- **Sent:** x = [0.4600, 0.2300, 0.6100, 0.7500, 0.1200]
- **Received:** y = -0.2830
- **Outcome:** did **not** improve over the previous best (-0.2404).

## 13. Week 9 — what we sent and what happened

- **Sent:** x = [0.4420, 0.2480, 0.5920, 0.7280, 0.1320]
- **Received:** y = -0.2520
- **Outcome:** did **not** improve over the previous best (-0.2404).

## 14. Week 10 — what we sent and what happened

- **Sent:** x = [0.4410, 0.2490, 0.5910, 0.7290, 0.1310]
- **Received:** y = -0.1360
- **Outcome:** **IMPROVED** over the previous best (-0.2404).

## 15. Week 11 — what we sent and what happened

- **Sent:** x = [0.4430, 0.2470, 0.5930, 0.7270, 0.1290]
- **Received:** y = -0.3722
- **Outcome:** did **not** improve over the previous best (-0.1360).

## 16. Week 12 — what we sent and what happened

- **Sent:** x = [0.4400, 0.2500, 0.5900, 0.7280, 0.1320]
- **Received:** y = -0.2054
- **Outcome:** did **not** improve over the previous best (-0.1360).

## 17. The lesson

Nearby is not enough on a sharp basin. After a failed neighbour, return hard to the proven mode.

## 18. Summary

| | Value |
|---|---|
| Real-world task | Cake Recipe Optimisation |
| Dimensions | 5 |
| Acquisition | EI (Matérn ν=2.5) |
| Best before W1 | -0.7143 |
| Week 1 result | -0.4775 (improved) |
| Week 2 result | -0.5782 (no improvement) |
| Week 3 result | -0.5377 (no improvement) |
| Week 4 result | -0.6062 (no improvement) |
| Week 5 result | -0.2654 (improved) |
| Week 6 result | -0.2404 (improved) |
| Week 7 result | -0.2672 (no improvement) |
| Week 8 result | -0.2830 (no improvement) |
| Week 9 result | -0.2520 (no improvement) |
| Week 10 result | -0.1360 (improved) |
| Week 11 result | -0.3722 (no improvement) |
| Week 12 result | -0.2054 (no improvement) |
| Current best (through Week 12) | -0.1360 |

*See `analysis_F6.png` in this folder for the 9-panel visual analysis (regenerated through Week 12).*
