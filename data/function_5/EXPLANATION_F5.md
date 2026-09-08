# F5 — Chemical Yield Optimisation (4-D)

## 1. The big picture

**Real world:** You are optimising a chemical reaction's yield; 4 process settings control the output.

- **x** = 4 process settings
- **y** = the reaction yield (higher = better)
- **Goal:** maximise the yield along a ridge.
- **Constraint:** one query per function per week (Stage 2 budget).

This is a **black box**: we never see the formula, only input → output. Bayesian optimisation
(GP + acquisition) is designed for exactly that setting.

## 2. Data so far (20 seed points + 12 weekly queries = 32 observations)

| # | x1 | x2 | x3 | x4 | y | note |
|---|---|---|---|---|---|---|
| 32 | 0.4400 | 0.9800 | 0.9800 | 0.9800 | 3800.7395 | BEST |
| 31 | 0.4300 | 0.9800 | 0.9800 | 0.9800 | 3789.5071 |  |
| 30 | 0.4200 | 0.9800 | 0.9800 | 0.9800 | 3779.0000 |  |
| 4 | 0.7061 | 0.5342 | 0.2642 | 0.4821 | 4.2109 |  |
| 3 | 0.4383 | 0.8043 | 0.2102 | 0.1513 | 0.1129 | WORST |

- **Best so far:** y = 3800.7395 at x = [0.4400, 0.9800, 0.9800, 0.9800]

## 3. What the GP learned (ARD length scales)

- `x1`: length-scale = 3.7495 → moderate influence
- `x2`: length-scale = 0.8151 → moderate influence
- `x3`: length-scale = 1.6765 → moderate influence
- `x4`: length-scale = 0.8745 → moderate influence

## 4. Acquisition / late policy: **EI**

Lock the high x2–x4 face and climb x1 (log-y GP fit). This produced a sustained yield run into the late weeks.

## 5. Week 1 — what we sent and what happened

- **Sent:** x = [0.2242, 0.8465, 0.9800, 0.9800]
- **Received:** y = 2497.3155
- **Outcome:** **IMPROVED** over the previous best (1088.8596).

## 6. Week 2 — what we sent and what happened

- **Sent:** x = [0.0742, 0.6965, 0.9800, 0.9800]
- **Received:** y = 1811.0568
- **Outcome:** did **not** improve over the previous best (2497.3155).

## 7. Week 3 — what we sent and what happened

- **Sent:** x = [0.1500, 0.9265, 0.9800, 0.9800]
- **Received:** y = 3108.4879
- **Outcome:** **IMPROVED** over the previous best (2497.3155).

## 8. Week 4 — what we sent and what happened

- **Sent:** x = [0.3800, 0.9800, 0.9800, 0.9800]
- **Received:** y = 3743.8291
- **Outcome:** **IMPROVED** over the previous best (3108.4879).

## 9. Week 5 — what we sent and what happened

- **Sent:** x = [0.2800, 0.9800, 0.9800, 0.9800]
- **Received:** y = 3692.5200
- **Outcome:** did **not** improve over the previous best (3743.8291).

## 10. Week 6 — what we sent and what happened

- **Sent:** x = [0.3600, 0.9800, 0.9800, 0.9800]
- **Received:** y = 3729.8367
- **Outcome:** did **not** improve over the previous best (3743.8291).

## 11. Week 7 — what we sent and what happened

- **Sent:** x = [0.3800, 0.9800, 0.9800, 0.9800]
- **Received:** y = 3743.8291
- **Outcome:** did **not** improve over the previous best (3743.8291).

## 12. Week 8 — what we sent and what happened

- **Sent:** x = [0.4000, 0.9800, 0.9800, 0.9800]
- **Received:** y = 3760.0000
- **Outcome:** **IMPROVED** over the previous best (3743.8291).

## 13. Week 9 — what we sent and what happened

- **Sent:** x = [0.4100, 0.9800, 0.9800, 0.9800]
- **Received:** y = 3769.0000
- **Outcome:** **IMPROVED** over the previous best (3760.0000).

## 14. Week 10 — what we sent and what happened

- **Sent:** x = [0.4200, 0.9800, 0.9800, 0.9800]
- **Received:** y = 3779.0000
- **Outcome:** **IMPROVED** over the previous best (3769.0000).

## 15. Week 11 — what we sent and what happened

- **Sent:** x = [0.4300, 0.9800, 0.9800, 0.9800]
- **Received:** y = 3789.5071
- **Outcome:** **IMPROVED** over the previous best (3779.0000).

## 16. Week 12 — what we sent and what happened

- **Sent:** x = [0.4400, 0.9800, 0.9800, 0.9800]
- **Received:** y = 3800.7395
- **Outcome:** **IMPROVED** over the previous best (3789.5071).

## 17. The lesson

Exploitation must keep producing NEW information along the sensitive axis — not re-query the same point.

## 18. Summary

| | Value |
|---|---|
| Real-world task | Chemical Yield Optimisation |
| Dimensions | 4 |
| Acquisition | EI (Matérn ν=2.5) |
| Best before W1 | 1088.8596 |
| Week 1 result | 2497.3155 (improved) |
| Week 2 result | 1811.0568 (no improvement) |
| Week 3 result | 3108.4879 (improved) |
| Week 4 result | 3743.8291 (improved) |
| Week 5 result | 3692.5200 (no improvement) |
| Week 6 result | 3729.8367 (no improvement) |
| Week 7 result | 3743.8291 (no improvement) |
| Week 8 result | 3760.0000 (improved) |
| Week 9 result | 3769.0000 (improved) |
| Week 10 result | 3779.0000 (improved) |
| Week 11 result | 3789.5071 (improved) |
| Week 12 result | 3800.7395 (improved) |
| Current best (through Week 12) | 3800.7395 |

*See `analysis_F5.png` in this folder for the 9-panel visual analysis (regenerated through Week 12).*
