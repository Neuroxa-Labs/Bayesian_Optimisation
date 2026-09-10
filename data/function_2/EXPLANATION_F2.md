# F2 — Noisy ML Log-Likelihood (2-D)

## 1. The big picture

**Real world:** You are tuning a machine-learning model whose validation log-likelihood is measured with noise.

- **x** = 2 model settings
- **y** = a noisy log-likelihood score (higher = better)
- **Goal:** maximise the (noisy) log-likelihood.
- **Constraint:** one query per function per week (Stage 2 budget).

This is a **black box**: we never see the formula, only input → output. Bayesian optimisation
(GP + acquisition) is designed for exactly that setting.

## 2. Data so far (10 seed points + 13 weekly queries = 23 observations)

| # | x1 | x2 | y | note |
|---|---|---|---|---|
| 15 | 0.7179 | 0.0200 | 0.7766 | BEST |
| 20 | 0.7175 | 0.0195 | 0.7200 |  |
| 14 | 0.7000 | 0.0200 | 0.6599 |  |
| 9 | 0.3386 | 0.2139 | -0.0139 |  |
| 3 | 0.1427 | 0.3490 | -0.0656 | WORST |

- **Best so far:** y = 0.7766 at x = [0.7179, 0.0200]

## 3. What the GP learned (ARD length scales)

- `x1`: length-scale = 0.1046 → **very sensitive** — small changes move y a lot
- `x2`: length-scale = 10.0000 → **degenerate** — little effect (GP effectively locks it)

## 4. Acquisition / late policy: **EI**

EI with a White noise kernel. The historical peak (~0.777) sits on a sharp ridge; late returns often land ~0.54 when the step is slightly off.

## 5. Week 1 — what we sent and what happened

- **Sent:** x = [0.6948, 0.9266]
- **Received:** y = 0.4898
- **Outcome:** did **not** improve over the previous best (0.6112).

## 6. Week 2 — what we sent and what happened

- **Sent:** x = [0.7343, 0.9266]
- **Received:** y = 0.5706
- **Outcome:** did **not** improve over the previous best (0.6112).

## 7. Week 3 — what we sent and what happened

- **Sent:** x = [0.7188, 0.9266]
- **Received:** y = 0.6022
- **Outcome:** did **not** improve over the previous best (0.6112).

## 8. Week 4 — what we sent and what happened

- **Sent:** x = [0.7000, 0.0200]
- **Received:** y = 0.6599
- **Outcome:** **IMPROVED** over the previous best (0.6112).

## 9. Week 5 — what we sent and what happened

- **Sent:** x = [0.7179, 0.0200]
- **Received:** y = 0.7766
- **Outcome:** **IMPROVED** over the previous best (0.6599).

## 10. Week 6 — what we sent and what happened

- **Sent:** x = [0.7500, 0.0200]
- **Received:** y = 0.4035
- **Outcome:** did **not** improve over the previous best (0.7766).

## 11. Week 7 — what we sent and what happened

- **Sent:** x = [0.7200, 0.0200]
- **Received:** y = 0.5074
- **Outcome:** did **not** improve over the previous best (0.7766).

## 12. Week 8 — what we sent and what happened

- **Sent:** x = [0.7120, 0.0150]
- **Received:** y = 0.6270
- **Outcome:** did **not** improve over the previous best (0.7766).

## 13. Week 9 — what we sent and what happened

- **Sent:** x = [0.7160, 0.0180]
- **Received:** y = 0.5240
- **Outcome:** did **not** improve over the previous best (0.7766).

## 14. Week 10 — what we sent and what happened

- **Sent:** x = [0.7175, 0.0195]
- **Received:** y = 0.7200
- **Outcome:** did **not** improve over the previous best (0.7766).

## 15. Week 11 — what we sent and what happened

- **Sent:** x = [0.7178, 0.0198]
- **Received:** y = 0.5482
- **Outcome:** did **not** improve over the previous best (0.7766).

## 16. Week 12 — what we sent and what happened

- **Sent:** x = [0.7179, 0.0200]
- **Received:** y = 0.5368
- **Outcome:** did **not** improve over the previous best (0.7766).

## 17. Week 13 — what we sent and what happened

- **Sent:** x = [0.7179, 0.0200]
- **Received:** y = 0.3722
- **Outcome:** did **not** improve over the previous best (0.7766).

## 18. The lesson

Treat noise as noise, but also respect razor ridges: hard-return toward the incumbent when neighbour steps keep missing.

## 19. Summary

| | Value |
|---|---|
| Real-world task | Noisy ML Log-Likelihood |
| Dimensions | 2 |
| Acquisition | EI (Matérn ν=2.5) |
| Best before W1 | 0.6112 |
| Week 1 result | 0.4898 (no improvement) |
| Week 2 result | 0.5706 (no improvement) |
| Week 3 result | 0.6022 (no improvement) |
| Week 4 result | 0.6599 (improved) |
| Week 5 result | 0.7766 (improved) |
| Week 6 result | 0.4035 (no improvement) |
| Week 7 result | 0.5074 (no improvement) |
| Week 8 result | 0.6270 (no improvement) |
| Week 9 result | 0.5240 (no improvement) |
| Week 10 result | 0.7200 (no improvement) |
| Week 11 result | 0.5482 (no improvement) |
| Week 12 result | 0.5368 (no improvement) |
| Week 13 result | 0.3722 (no improvement) |
| Current best (through Week 13) | 0.7766 |

*See `analysis_F2.png` in this folder for the 9-panel visual analysis (regenerated through Week 13).*
