# F4 — Warehouse Placement (4-D)

## 1. The big picture

**Real world:** You are placing items in a warehouse; 4 factors control how efficient the layout is.

- **x** = 4 placement factors
- **y** = an efficiency score (higher = better)
- **Goal:** maximise warehouse efficiency.
- **Constraint:** one query per function per week (Stage 2 budget).

This is a **black box**: we never see the formula, only input → output. Bayesian optimisation
(GP + acquisition) is designed for exactly that setting.

## 2. Data so far (30 seed points + 12 weekly queries = 42 observations)

| # | x1 | x2 | x3 | x4 | y | note |
|---|---|---|---|---|---|---|
| 42 | 0.4040 | 0.4130 | 0.3550 | 0.4130 | 0.6786 | BEST |
| 41 | 0.4030 | 0.4140 | 0.3560 | 0.4120 | 0.6752 |  |
| 40 | 0.4020 | 0.4160 | 0.3580 | 0.4100 | 0.6670 |  |
| 21 | 0.6835 | 0.9028 | 0.3354 | 0.9995 | -29.4271 |  |
| 26 | 0.9484 | 0.8945 | 0.8516 | 0.5522 | -32.6257 | WORST |

- **Best so far:** y = 0.6786 at x = [0.4040, 0.4130, 0.3550, 0.4130]

## 3. What the GP learned (ARD length scales)

- `x1`: length-scale = 1.2622 → moderate influence
- `x2`: length-scale = 1.1899 → moderate influence
- `x3`: length-scale = 0.9177 → moderate influence
- `x4`: length-scale = 1.1153 → moderate influence

## 4. Acquisition / late policy: **UCB (k=1.5)**

After early exploration mapped a useful basin, late weeks use tight trust-region micro-steps.

## 5. Week 1 — what we sent and what happened

- **Sent:** x = [0.4040, 0.4080, 0.3381, 0.4375]
- **Received:** y = 0.2575
- **Outcome:** **IMPROVED** over the previous best (-4.0255).

## 6. Week 2 — what we sent and what happened

- **Sent:** x = [0.4604, 0.4346, 0.2031, 0.4318]
- **Received:** y = -3.3056
- **Outcome:** did **not** improve over the previous best (0.2575).

## 7. Week 3 — what we sent and what happened

- **Sent:** x = [0.3440, 0.4539, 0.3981, 0.4339]
- **Received:** y = -0.1262
- **Outcome:** did **not** improve over the previous best (0.2575).

## 8. Week 4 — what we sent and what happened

- **Sent:** x = [0.4141, 0.3859, 0.3781, 0.4415]
- **Received:** y = 0.1660
- **Outcome:** did **not** improve over the previous best (0.2575).

## 9. Week 5 — what we sent and what happened

- **Sent:** x = [0.4258, 0.4396, 0.3811, 0.4370]
- **Received:** y = 0.2403
- **Outcome:** did **not** improve over the previous best (0.2575).

## 10. Week 6 — what we sent and what happened

- **Sent:** x = [0.4008, 0.4135, 0.3767, 0.4061]
- **Received:** y = 0.4695
- **Outcome:** **IMPROVED** over the previous best (0.2575).

## 11. Week 7 — what we sent and what happened

- **Sent:** x = [0.3950, 0.4200, 0.3800, 0.4100]
- **Received:** y = 0.4637
- **Outcome:** did **not** improve over the previous best (0.4695).

## 12. Week 8 — what we sent and what happened

- **Sent:** x = [0.3970, 0.4200, 0.3650, 0.4050]
- **Received:** y = 0.5720
- **Outcome:** **IMPROVED** over the previous best (0.4695).

## 13. Week 9 — what we sent and what happened

- **Sent:** x = [0.4000, 0.4180, 0.3600, 0.4080]
- **Received:** y = 0.6420
- **Outcome:** **IMPROVED** over the previous best (0.5720).

## 14. Week 10 — what we sent and what happened

- **Sent:** x = [0.4020, 0.4160, 0.3580, 0.4100]
- **Received:** y = 0.6670
- **Outcome:** **IMPROVED** over the previous best (0.6420).

## 15. Week 11 — what we sent and what happened

- **Sent:** x = [0.4030, 0.4140, 0.3560, 0.4120]
- **Received:** y = 0.6752
- **Outcome:** **IMPROVED** over the previous best (0.6670).

## 16. Week 12 — what we sent and what happened

- **Sent:** x = [0.4040, 0.4130, 0.3550, 0.4130]
- **Received:** y = 0.6786
- **Outcome:** **IMPROVED** over the previous best (0.6752).

## 17. The lesson

Multimodal spaces need breadth first, then local climb once a basin proves real.

## 18. Summary

| | Value |
|---|---|
| Real-world task | Warehouse Placement |
| Dimensions | 4 |
| Acquisition | UCB (k=1.5) (Matérn ν=2.5) |
| Best before W1 | -4.0255 |
| Week 1 result | 0.2575 (improved) |
| Week 2 result | -3.3056 (no improvement) |
| Week 3 result | -0.1262 (no improvement) |
| Week 4 result | 0.1660 (no improvement) |
| Week 5 result | 0.2403 (no improvement) |
| Week 6 result | 0.4695 (improved) |
| Week 7 result | 0.4637 (no improvement) |
| Week 8 result | 0.5720 (improved) |
| Week 9 result | 0.6420 (improved) |
| Week 10 result | 0.6670 (improved) |
| Week 11 result | 0.6752 (improved) |
| Week 12 result | 0.6786 (improved) |
| Current best (through Week 12) | 0.6786 |

*See `analysis_F4.png` in this folder for the 9-panel visual analysis (regenerated through Week 12).*
