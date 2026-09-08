# Week 13 Strategy — Final portal round

*After Week 12 (4/8 improved: F4, F5, F7, F8). Near-pure exploitation + recoveries. **Last weekly submission** (final round).*

Also linked as [`final_round_strategy.md`](final_round_strategy.md) for portfolio naming.

## Policy

| Mode | Functions | Action |
|------|-----------|--------|
| **Ridge continue** | F5 | x₁ → 0.45 on locked high face |
| **Micro on W12 best** | F4, F7, F8 | Tiny new offsets from incumbents |
| **Hard return to historical best** | F2, F3, F6 | As close as allowed to verified peak (new coords) |
| **Signal lobe** | F1 | Stay in ~0.64/0.68 |

## Approved portal block (Week 13)

```
Function 1:  0.635000-0.688000
Function 2:  0.717870-0.020000
Function 3:  0.492580-0.691590-0.401000
Function 4:  0.405000-0.412000-0.354000-0.414000
Function 5:  0.450000-0.980000-0.980000-0.980000
Function 6:  0.441200-0.249200-0.590800-0.728700-0.131200
Function 7:  0.074000-0.424000-0.299000-0.158000-0.346000-0.672000
Function 8:  0.144000-0.060000-0.210000-0.050000-0.414000-0.510000-0.216000-0.917000
```

## One-line rationale

| Fn | Why |
|----|-----|
| F1 | Signal lobe micro (W12 −0.005) |
| F2 | Exact neighbourhood of historical **0.777** at [0.717869, 0.02] |
| F3 | Exact neighbourhood of **−0.011** peak; x₃ locked |
| F4 | Micro from W12 **0.679** |
| F5 | Ridge continue x₁=**0.45** (W12 0.44 → 3801) |
| F6 | Finish return to W10 **−0.136** centroid |
| F7 | Micro from W12 **1.872** |
| F8 | Micro from W12 **9.873** |

## Status

**Queries locked for Week 13 / final round.** Portal `y` not yet recorded — reflection will follow when results arrive.

RL discussion: [`final_round_rl_reflection.md`](final_round_rl_reflection.md).
