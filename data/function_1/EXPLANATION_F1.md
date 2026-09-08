# F1 — Radiation Source Detection (2-D)

## 1. The big picture

**Real world:** You are sweeping a 2-D field to locate a hidden radioactive source with a Geiger counter.

- **x** = the (x1, x2) position on the map
- **y** = the counter reading (higher = closer to the source)
- **Goal:** find the position with the strongest reading (the hidden source).
- **Constraint:** one query per function per week (Stage 2 budget).

This is a **black box**: we never see the formula, only input → output. Bayesian optimisation
(GP + acquisition) is designed for exactly that setting.

## 2. Data so far (10 seed points + 12 weekly queries = 22 observations)

| # | x1 | x2 | y | note |
|---|---|---|---|---|
| 3 | 0.7310 | 0.7330 | 7.711e-16 | BEST |
| 18 | 0.6700 | 0.4500 | 1.000e-20 |  |
| 19 | 0.5500 | 0.3200 | 1.000e-20 |  |
| 12 | 0.4211 | 0.4636 | -0.0066 |  |
| 20 | 0.6400 | 0.6820 | -0.0081 | WORST |

- **Best so far:** y = 7.711e-16 at x = [0.7310, 0.7330]

## 3. What the GP learned (ARD length scales)

- `x1`: length-scale = 0.0123 → **very sensitive** — small changes move y a lot
- `x2`: length-scale = 0.0772 → **very sensitive** — small changes move y a lot

## 4. Acquisition / late policy: **EI**

Almost everywhere reads ~0. After a long null phase near (0.73, 0.73), a peer-supported signal lobe near (0.64, 0.68) produced measurable readings; late weeks stay inside that lobe.

## 5. Week 1 — what we sent and what happened

- **Sent:** x = [0.1964, 0.9707]
- **Received:** y = 4.846e-214
- **Outcome:** did **not** improve over the previous best (7.711e-16).

## 6. Week 2 — what we sent and what happened

- **Sent:** x = [0.4211, 0.4636]
- **Received:** y = -0.0066
- **Outcome:** did **not** improve over the previous best (7.711e-16).

## 7. Week 3 — what we sent and what happened

- **Sent:** x = [0.0700, 0.6695]
- **Received:** y = -1.764e-130
- **Outcome:** did **not** improve over the previous best (7.711e-16).

## 8. Week 4 — what we sent and what happened

- **Sent:** x = [0.6615, 0.4364]
- **Received:** y = 3.213e-28
- **Outcome:** did **not** improve over the previous best (7.711e-16).

## 9. Week 5 — what we sent and what happened

- **Sent:** x = [0.6625, 0.0700]
- **Received:** y = -4.778e-128
- **Outcome:** did **not** improve over the previous best (7.711e-16).

## 10. Week 6 — what we sent and what happened

- **Sent:** x = [0.7550, 0.7100]
- **Received:** y = -1.273e-16
- **Outcome:** did **not** improve over the previous best (7.711e-16).

## 11. Week 7 — what we sent and what happened

- **Sent:** x = [0.7600, 0.7600]
- **Received:** y = 5.184e-25
- **Outcome:** did **not** improve over the previous best (7.711e-16).

## 12. Week 8 — what we sent and what happened

- **Sent:** x = [0.6700, 0.4500]
- **Received:** y = 1.000e-20
- **Outcome:** did **not** improve over the previous best (7.711e-16).

## 13. Week 9 — what we sent and what happened

- **Sent:** x = [0.5500, 0.3200]
- **Received:** y = 1.000e-20
- **Outcome:** did **not** improve over the previous best (7.711e-16).

## 14. Week 10 — what we sent and what happened

- **Sent:** x = [0.6400, 0.6820]
- **Received:** y = -0.0081
- **Outcome:** did **not** improve over the previous best (7.711e-16).

## 15. Week 11 — what we sent and what happened

- **Sent:** x = [0.6380, 0.6850]
- **Received:** y = -0.0062
- **Outcome:** did **not** improve over the previous best (7.711e-16).

## 16. Week 12 — what we sent and what happened

- **Sent:** x = [0.6360, 0.6870]
- **Received:** y = -0.0051
- **Outcome:** did **not** improve over the previous best (7.711e-16).

## 17. The lesson

A zero is elimination, not proof the source is elsewhere. Once a real signal cluster appears, exploit it; do not keep polishing a null basin.

## 18. Summary

| | Value |
|---|---|
| Real-world task | Radiation Source Detection |
| Dimensions | 2 |
| Acquisition | EI (Matérn ν=0.5) |
| Best before W1 | 7.711e-16 |
| Week 1 result | 4.846e-214 (no improvement) |
| Week 2 result | -0.0066 (no improvement) |
| Week 3 result | -1.764e-130 (no improvement) |
| Week 4 result | 3.213e-28 (no improvement) |
| Week 5 result | -4.778e-128 (no improvement) |
| Week 6 result | -1.273e-16 (no improvement) |
| Week 7 result | 5.184e-25 (no improvement) |
| Week 8 result | 1.000e-20 (no improvement) |
| Week 9 result | 1.000e-20 (no improvement) |
| Week 10 result | -0.0081 (no improvement) |
| Week 11 result | -0.0062 (no improvement) |
| Week 12 result | -0.0051 (no improvement) |
| Current best (through Week 12) | 7.711e-16 |

*See `analysis_F1.png` in this folder for the 9-panel visual analysis (regenerated through Week 12).*
