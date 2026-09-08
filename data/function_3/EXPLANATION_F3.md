# F3 — Drug Discovery - Adverse Reactions (3-D)

## 1. The big picture

**Real world:** A drug-development lab mixes 3 chemical components and measures a side-effect score.

- **x** = the 3 component ratios (x1, x2, x3)
- **y** = the negative side effect (y near 0 = safe, very negative = harmful)
- **Goal:** minimise side effects, i.e. push y as close to 0 as possible (we maximise y = -(side effect)).
- **Constraint:** one query per function per week (Stage 2 budget).

This is a **black box**: we never see the formula, only input → output. Bayesian optimisation
(GP + acquisition) is designed for exactly that setting.

## 2. Data so far (15 seed points + 11 weekly queries = 26 observations)

| # | x1 | x2 | x3 | y | note |
|---|---|---|---|---|---|
| 20 | 0.4926 | 0.6916 | 0.4010 | -0.0114 | BEST |
| 21 | 0.4850 | 0.6850 | 0.4010 | -0.0145 |  |
| 24 | 0.4930 | 0.6920 | 0.4010 | -0.0190 |  |
| 16 | 0.4926 | 0.0200 | 0.6482 | -0.1685 |  |
| 7 | 0.1518 | 0.4400 | 0.9909 | -0.3989 | WORST |

- **Best so far:** y = -0.0114 at x = [0.4926, 0.6916, 0.4010]

## 3. What the GP learned (ARD length scales)

- `x1`: length-scale = 0.0100 → **very sensitive** — small changes move y a lot
- `x2`: length-scale = 0.0100 → **very sensitive** — small changes move y a lot
- `x3`: length-scale = 0.1497 → **very sensitive** — small changes move y a lot

## 4. Acquisition / late policy: **EI**

x3 is sensitive; keep it locked in a safe band and take local steps around the -0.011 neighbourhood.

## 5. Week 1 — what we sent and what happened

- **Sent:** x = [0.4926, 0.0200, 0.6482]
- **Received:** y = -0.1685
- **Outcome:** did **not** improve over the previous best (-0.0348).

## 6. Week 2 — what we sent and what happened

- **Sent:** x = [0.4926, 0.6916, 0.4013]
- **Received:** y = -0.0203
- **Outcome:** **IMPROVED** over the previous best (-0.0348).

## 7. Week 3 — what we sent and what happened

- **Sent:** x = [0.6426, 0.6916, 0.4787]
- **Received:** y = -0.0227
- **Outcome:** did **not** improve over the previous best (-0.0203).

## 8. Week 4 — what we sent and what happened

- **Sent:** x = [0.5926, 0.7716, 0.4363]
- **Received:** y = -0.0434
- **Outcome:** did **not** improve over the previous best (-0.0203).

## 9. Week 5 — what we sent and what happened

- **Sent:** x = [0.4926, 0.6916, 0.4010]
- **Received:** y = -0.0114
- **Outcome:** **IMPROVED** over the previous best (-0.0203).

## 10. Week 6 — what we sent and what happened

- **Sent:** x = [0.4850, 0.6850, 0.4010]
- **Received:** y = -0.0145
- **Outcome:** did **not** improve over the previous best (-0.0114).

## 11. Week 7 — what we sent and what happened

- **Sent:** x = [0.4980, 0.6980, 0.3980]
- **Received:** y = -0.0260
- **Outcome:** did **not** improve over the previous best (-0.0114).

## 12. Week 8 — what we sent and what happened

- **Sent:** x = [0.4950, 0.6950, 0.4000]
- **Received:** y = -0.0240
- **Outcome:** did **not** improve over the previous best (-0.0114).

## 13. Week 9 — what we sent and what happened

- **Sent:** x = [0.4930, 0.6920, 0.4010]
- **Received:** y = -0.0190
- **Outcome:** did **not** improve over the previous best (-0.0114).

## 14. Week 10 — what we sent and what happened

- **Sent:** x = [0.4926, 0.6916, 0.4010]
- **Received:** y = -0.0267
- **Outcome:** did **not** improve over the previous best (-0.0114).

## 15. Week 11 — what we sent and what happened

- **Sent:** x = [0.4926, 0.6915, 0.4010]
- **Received:** y = -0.0194
- **Outcome:** did **not** improve over the previous best (-0.0114).

## 16. The lesson

Small length-scale dimensions need small steps. Boundary jumps early on taught that lesson.

## 17. Summary

| | Value |
|---|---|
| Real-world task | Drug Discovery - Adverse Reactions |
| Dimensions | 3 |
| Acquisition | EI (Matérn ν=1.5) |
| Best before W1 | -0.0348 |
| Week 1 result | -0.1685 (no improvement) |
| Week 2 result | -0.0203 (improved) |
| Week 3 result | -0.0227 (no improvement) |
| Week 4 result | -0.0434 (no improvement) |
| Week 5 result | -0.0114 (improved) |
| Week 6 result | -0.0145 (no improvement) |
| Week 7 result | -0.0260 (no improvement) |
| Week 8 result | -0.0240 (no improvement) |
| Week 9 result | -0.0190 (no improvement) |
| Week 10 result | -0.0267 (no improvement) |
| Week 11 result | -0.0194 (no improvement) |
| Current best (through Week 11) | -0.0114 |

*See `analysis_F3.png` in this folder for the 9-panel visual analysis (regenerated through Week 11).*
