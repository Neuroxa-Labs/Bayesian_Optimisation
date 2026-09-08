# F7 — ML Hyperparameter Tuning (6-D)

## 1. The big picture

**Real world:** You are tuning 6 hyperparameters of a machine-learning model.

- **x** = 6 hyperparameters
- **y** = a validation score (higher = better)
- **Goal:** maximise the validation score.
- **Constraint:** one query per function per week (Stage 2 budget).

This is a **black box**: we never see the formula, only input → output. Bayesian optimisation
(GP + acquisition) is designed for exactly that setting.

## 2. Data so far (30 seed points + 12 weekly queries = 42 observations)

| # | x1 | x2 | x3 | x4 | x5 | x6 | y | note |
|---|---|---|---|---|---|---|---|---|
| 42 | 0.0730 | 0.4250 | 0.3000 | 0.1570 | 0.3450 | 0.6710 | 1.8722 | BEST |
| 41 | 0.0720 | 0.4260 | 0.3010 | 0.1560 | 0.3440 | 0.6700 | 1.8665 |  |
| 40 | 0.0700 | 0.4280 | 0.3030 | 0.1580 | 0.3460 | 0.6720 | 1.8630 |  |
| 28 | 0.8469 | 0.1424 | 0.0607 | 0.7563 | 0.5524 | 0.0813 | 0.0031 |  |
| 20 | 0.8799 | 0.3980 | 0.0036 | 0.9570 | 0.2645 | 0.1149 | 0.0027 | WORST |

- **Best so far:** y = 1.8722 at x = [0.0730, 0.4250, 0.3000, 0.1570, 0.3450, 0.6710]

## 3. What the GP learned (ARD length scales)

- `x1`: length-scale = 0.5913 → moderate influence
- `x2`: length-scale = 0.2606 → **very sensitive** — small changes move y a lot
- `x3`: length-scale = 10.0000 → **degenerate** — little effect (GP effectively locks it)
- `x4`: length-scale = 0.5041 → moderate influence
- `x5`: length-scale = 0.2899 → **very sensitive** — small changes move y a lot
- `x6`: length-scale = 0.4612 → **very sensitive** — small changes move y a lot

## 4. Acquisition / late policy: **EI**

Local EI around the late peak; move ARD-sensitive axes and leave flat ones alone.

## 5. Week 1 — what we sent and what happened

- **Sent:** x = [0.0200, 0.4917, 0.2474, 0.2174, 0.3780, 0.7465]
- **Received:** y = 1.4506
- **Outcome:** **IMPROVED** over the previous best (1.3650).

## 6. Week 2 — what we sent and what happened

- **Sent:** x = [0.0200, 0.4917, 0.2474, 0.2146, 0.3772, 0.8061]
- **Received:** y = 1.2983
- **Outcome:** did **not** improve over the previous best (1.4506).

## 7. Week 3 — what we sent and what happened

- **Sent:** x = [0.0700, 0.4917, 0.2474, 0.1674, 0.3539, 0.7156]
- **Received:** y = 1.5253
- **Outcome:** **IMPROVED** over the previous best (1.4506).

## 8. Week 4 — what we sent and what happened

- **Sent:** x = [0.0700, 0.4317, 0.3074, 0.1589, 0.3474, 0.6722]
- **Received:** y = 1.8575
- **Outcome:** **IMPROVED** over the previous best (1.5253).

## 9. Week 5 — what we sent and what happened

- **Sent:** x = [0.0700, 0.3761, 0.3074, 0.1075, 0.3237, 0.6484]
- **Received:** y = 1.8161
- **Outcome:** did **not** improve over the previous best (1.8575).

## 10. Week 6 — what we sent and what happened

- **Sent:** x = [0.0700, 0.4166, 0.3074, 0.1369, 0.3246, 0.6547]
- **Received:** y = 1.8471
- **Outcome:** did **not** improve over the previous best (1.8575).

## 11. Week 7 — what we sent and what happened

- **Sent:** x = [0.0700, 0.4350, 0.3100, 0.1600, 0.3500, 0.6750]
- **Received:** y = 1.8468
- **Outcome:** did **not** improve over the previous best (1.8575).

## 12. Week 8 — what we sent and what happened

- **Sent:** x = [0.0550, 0.4200, 0.3120, 0.1550, 0.3500, 0.6680]
- **Received:** y = 1.8560
- **Outcome:** did **not** improve over the previous best (1.8575).

## 13. Week 9 — what we sent and what happened

- **Sent:** x = [0.0680, 0.4300, 0.3050, 0.1600, 0.3480, 0.6740]
- **Received:** y = 1.8580
- **Outcome:** **IMPROVED** over the previous best (1.8575).

## 14. Week 10 — what we sent and what happened

- **Sent:** x = [0.0700, 0.4280, 0.3030, 0.1580, 0.3460, 0.6720]
- **Received:** y = 1.8630
- **Outcome:** **IMPROVED** over the previous best (1.8580).

## 15. Week 11 — what we sent and what happened

- **Sent:** x = [0.0720, 0.4260, 0.3010, 0.1560, 0.3440, 0.6700]
- **Received:** y = 1.8665
- **Outcome:** **IMPROVED** over the previous best (1.8630).

## 16. Week 12 — what we sent and what happened

- **Sent:** x = [0.0730, 0.4250, 0.3000, 0.1570, 0.3450, 0.6710]
- **Received:** y = 1.8722
- **Outcome:** **IMPROVED** over the previous best (1.8665).

## 17. The lesson

In 6-D, patience and small local gains accumulate better than global jumps late in the budget.

## 18. Summary

| | Value |
|---|---|
| Real-world task | ML Hyperparameter Tuning |
| Dimensions | 6 |
| Acquisition | EI (Matérn ν=2.5) |
| Best before W1 | 1.3650 |
| Week 1 result | 1.4506 (improved) |
| Week 2 result | 1.2983 (no improvement) |
| Week 3 result | 1.5253 (improved) |
| Week 4 result | 1.8575 (improved) |
| Week 5 result | 1.8161 (no improvement) |
| Week 6 result | 1.8471 (no improvement) |
| Week 7 result | 1.8468 (no improvement) |
| Week 8 result | 1.8560 (no improvement) |
| Week 9 result | 1.8580 (improved) |
| Week 10 result | 1.8630 (improved) |
| Week 11 result | 1.8665 (improved) |
| Week 12 result | 1.8722 (improved) |
| Current best (through Week 12) | 1.8722 |

*See `analysis_F7.png` in this folder for the 9-panel visual analysis (regenerated through Week 12).*
