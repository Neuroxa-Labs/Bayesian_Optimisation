# Week 8 Strategy — FINAL (progress-critical)

*Locked after neighbourhood audit + local GP search. Do **not** re-query exact incumbents.*

## Confidence (honest)

| Level | Functions | Claim |
|-------|-----------|--------|
| **Highest EV** | **F5** | Ridge 0.28→0.36→**0.38**; never tried **>0.38**. Query **0.40** (not 0.50 — GP extrapolates too far). |
| **Solid** | **F2**, **F8** | F2: stay left of 0.72 cliff; F8: plateau still ticking. |
| **Moderate** | **F4, F6, F7** | Local EI in basin; new coords. |
| **Low** | **F3** | Safe-band micro only. |
| **Very low** | **F1** | No signal; explore only. |

**Cannot guarantee 8/8.** Realistic serious-progress target: **≥2 new bests**, stretch **3–4**, with F5 as the primary bet.

## Final portal block

```
Function 1:  0.670000-0.450000
Function 2:  0.712000-0.015000
Function 3:  0.498000-0.698000-0.398000
Function 4:  0.397000-0.420000-0.365000-0.405000
Function 5:  0.400000-0.980000-0.980000-0.980000
Function 6:  0.460000-0.230000-0.610000-0.750000-0.120000
Function 7:  0.055000-0.420000-0.312000-0.155000-0.350000-0.668000
Function 8:  0.135000-0.068000-0.218000-0.042000-0.405000-0.505000-0.225000-0.900000
```

## One-line rationale

| Fn | Why this x |
|----|------------|
| F1 | 2nd warm lobe; GP untrusted |
| F2 | New point left of cliff (0.718 best, 0.720 collapsed) |
| F3 | Untested micro in safe x₃ band |
| F4 | Local EI near 0.470 basin |
| F5 | **Flagship:** first probe above 0.38 on locked high face |
| F6 | Local EI away from failed uniform ± steps |
| F7 | Local EI; soft x₁≠0.02 edge |
| F8 | Light exploit, new vector (not W7 clone; no boundary x₄=0) |

## Status

**APPROVED TO SUBMIT** if you accept the risk profile above.
