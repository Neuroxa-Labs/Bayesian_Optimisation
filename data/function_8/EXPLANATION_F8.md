# F8 — 8-Parameter ML Model Optimisation (8-D)

## 1. The big picture

**Real world:** You are optimising a complex ML model with 8 parameters.

- **x** = 8 parameters
- **y** = a model score (higher = better)
- **Goal:** maximise the score in a large 8-D space.
- **Constraint:** one query per function per week (Stage 2 budget).

This is a **black box**: we never see the formula, only input → output. Bayesian optimisation
(GP + acquisition) is designed for exactly that setting.

## 2. Data so far (40 seed points + 12 weekly queries = 52 observations)

| # | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | y | note |
|---|---|---|---|---|---|---|---|---|---|---|
| 52 | 0.1430 | 0.0610 | 0.2110 | 0.0490 | 0.4130 | 0.5110 | 0.2170 | 0.9160 | 9.8729 | BEST |
| 51 | 0.1420 | 0.0620 | 0.2120 | 0.0480 | 0.4120 | 0.5120 | 0.2180 | 0.9150 | 9.8722 |  |
| 50 | 0.1400 | 0.0640 | 0.2140 | 0.0460 | 0.4100 | 0.5100 | 0.2200 | 0.9100 | 9.8710 |  |
| 22 | 0.8989 | 0.5236 | 0.8768 | 0.2187 | 0.9003 | 0.2828 | 0.9111 | 0.4724 | 5.8411 |  |
| 10 | 0.9849 | 0.6995 | 0.9989 | 0.1801 | 0.5801 | 0.2311 | 0.4908 | 0.3137 | 5.5922 | WORST |

- **Best so far:** y = 9.8729 at x = [0.1430, 0.0610, 0.2110, 0.0490, 0.4130, 0.5110, 0.2170, 0.9160]

## 3. What the GP learned (ARD length scales)

- `x1`: length-scale = 3.6839 → moderate influence
- `x2`: length-scale = 5.7468 → **degenerate** — little effect (GP effectively locks it)
- `x3`: length-scale = 2.7315 → moderate influence
- `x4`: length-scale = 9.4291 → **degenerate** — little effect (GP effectively locks it)
- `x5`: length-scale = 10.0000 → **degenerate** — little effect (GP effectively locks it)
- `x6`: length-scale = 6.7362 → **degenerate** — little effect (GP effectively locks it)
- `x7`: length-scale = 3.8359 → moderate influence
- `x8`: length-scale = 10.0000 → **degenerate** — little effect (GP effectively locks it)

## 4. Acquisition / late policy: **UCB (k=1.5)**

Expect slow late gains. Trust-region steps on ARD-sensitive dims with a boundary penalty.

## 5. Week 1 — what we sent and what happened

- **Sent:** x = [0.0200, 0.0200, 0.1887, 0.0388, 0.4039, 0.4868, 0.0200, 0.8931]
- **Received:** y = 9.7956
- **Outcome:** **IMPROVED** over the previous best (9.5985).

## 6. Week 2 — what we sent and what happened

- **Sent:** x = [0.0700, 0.0700, 0.0200, 0.0388, 0.4039, 0.0700, 0.0700, 0.8931]
- **Received:** y = 9.6374
- **Outcome:** did **not** improve over the previous best (9.7956).

## 7. Week 3 — what we sent and what happened

- **Sent:** x = [0.0700, 0.0700, 0.0200, 0.0388, 0.4039, 0.9300, 0.0200, 0.8931]
- **Received:** y = 9.6064
- **Outcome:** did **not** improve over the previous best (9.7956).

## 8. Week 4 — what we sent and what happened

- **Sent:** x = [0.0200, 0.0200, 0.1882, 0.0388, 0.4039, 0.4861, 0.0200, 0.8931]
- **Received:** y = 9.7958
- **Outcome:** **IMPROVED** over the previous best (9.7956).

## 9. Week 5 — what we sent and what happened

- **Sent:** x = [0.1262, 0.0700, 0.2245, 0.0388, 0.4039, 0.4974, 0.2281, 0.8931]
- **Received:** y = 9.8645
- **Outcome:** **IMPROVED** over the previous best (9.7958).

## 10. Week 6 — what we sent and what happened

- **Sent:** x = [0.0700, 0.2729, 0.2099, 0.0388, 0.4039, 0.5452, 0.1985, 0.8931]
- **Received:** y = 9.8625
- **Outcome:** did **not** improve over the previous best (9.8645).

## 11. Week 7 — what we sent and what happened

- **Sent:** x = [0.1300, 0.0700, 0.2200, 0.0400, 0.4000, 0.5000, 0.2300, 0.8900]
- **Received:** y = 9.8652
- **Outcome:** **IMPROVED** over the previous best (9.8645).

## 12. Week 8 — what we sent and what happened

- **Sent:** x = [0.1350, 0.0680, 0.2180, 0.0420, 0.4050, 0.5050, 0.2250, 0.9000]
- **Received:** y = 9.8680
- **Outcome:** **IMPROVED** over the previous best (9.8652).

## 13. Week 9 — what we sent and what happened

- **Sent:** x = [0.1380, 0.0660, 0.2160, 0.0440, 0.4080, 0.5080, 0.2220, 0.9050]
- **Received:** y = 9.8690
- **Outcome:** **IMPROVED** over the previous best (9.8680).

## 14. Week 10 — what we sent and what happened

- **Sent:** x = [0.1400, 0.0640, 0.2140, 0.0460, 0.4100, 0.5100, 0.2200, 0.9100]
- **Received:** y = 9.8710
- **Outcome:** **IMPROVED** over the previous best (9.8690).

## 15. Week 11 — what we sent and what happened

- **Sent:** x = [0.1420, 0.0620, 0.2120, 0.0480, 0.4120, 0.5120, 0.2180, 0.9150]
- **Received:** y = 9.8722
- **Outcome:** **IMPROVED** over the previous best (9.8710).

## 16. Week 12 — what we sent and what happened

- **Sent:** x = [0.1430, 0.0610, 0.2110, 0.0490, 0.4130, 0.5110, 0.2170, 0.9160]
- **Received:** y = 9.8729
- **Outcome:** **IMPROVED** over the previous best (9.8722).

## 17. The lesson

In 8-D, steady micro-improvements are success; do not chase edge uncertainty artefacts.

## 18. Summary

| | Value |
|---|---|
| Real-world task | 8-Parameter ML Model Optimisation |
| Dimensions | 8 |
| Acquisition | UCB (k=1.5) (Matérn ν=1.5) |
| Best before W1 | 9.5985 |
| Week 1 result | 9.7956 (improved) |
| Week 2 result | 9.6374 (no improvement) |
| Week 3 result | 9.6064 (no improvement) |
| Week 4 result | 9.7958 (improved) |
| Week 5 result | 9.8645 (improved) |
| Week 6 result | 9.8625 (no improvement) |
| Week 7 result | 9.8652 (improved) |
| Week 8 result | 9.8680 (improved) |
| Week 9 result | 9.8690 (improved) |
| Week 10 result | 9.8710 (improved) |
| Week 11 result | 9.8722 (improved) |
| Week 12 result | 9.8729 (improved) |
| Current best (through Week 12) | 9.8729 |

*See `analysis_F8.png` in this folder for the 9-panel visual analysis (regenerated through Week 12).*
