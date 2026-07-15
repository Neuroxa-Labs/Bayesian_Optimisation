# Week 8 Strategy — Black-Box Bayesian Optimisation

*Draft for approval after Week 7 (1/8 improved: F8).*

## Analysis entering Week 8

| Fn | Best y @ x (approx) | Recent lesson |
|----|---------------------|---------------|
| F1 | ~1e−16 @ [0.731, 0.733] | Best-neighbour + B+ both failed → try **2nd-best warm** region |
| F2 | **0.777** @ [0.718, 0.02] | 0.72→0.507, 0.75→0.403 → **exact W5 return** |
| F3 | **−0.011** @ W6 [0.493, 0.692, 0.401] | Stay on W6 point / tiny step |
| F4 | **0.470** @ W6 basin | Tiny local step only |
| F5 | **3744** @ [0.38, 0.98³] | Ridge locked; micro-tune x₁ **0.37–0.39** |
| F6 | **−0.240** @ W6 [0.44, 0.25, 0.59, 0.73, 0.13] | W7 step hurt → **return to W6** |
| F7 | **1.857** @ W4 coords | Micro-steps failed → **exact best return** |
| F8 | **9.865** @ W7 query | Continue light exploit from new best |

## Proposed approach

| Fn | Mode | Proposed query idea |
|----|------|---------------------|
| **F1** | Soft-signal **2nd-best probe** | Near [0.662, 0.436] (2nd highest y), e.g. **0.670000-0.450000** — not another UR clone |
| **F2** | Exact-band return | **0.717869-0.020000** (W5 record x) or **0.715000-0.020000** |
| **F3** | W6 best protect | **0.492581-0.691593-0.401000** |
| **F4** | Basin micro | **0.402000-0.415000-0.375000-0.408000** |
| **F5** | Ridge micro | **0.375000-0.980000-0.980000-0.980000** |
| **F6** | Return W6 | **0.440000-0.250000-0.590000-0.730000-0.130000** |
| **F7** | Return W4 best | **0.070000-0.431672-0.307422-0.158929-0.347393-0.672154** |
| **F8** | Exploit W7 | Small step from W7 best, e.g. **0.128000-0.070000-0.218000-0.040000-0.402000-0.502000-0.228000-0.892000** |

## F1 rationale (changed again)

UR local search (W6/W7) exhausted without signal. Second-best point `[0.662, 0.436]` is the only other relatively “less dead” reading (y≈3e−28). Week 8 probes that lobe instead of repeating [0.73, 0.73].

## Expectation

**~2–4 / 8** improve if return-to-best works on F2/F6/F7 and F8 continues; F1 still low probability.

## Status

**Awaiting approval** before portal submission. Final 8-line block will be locked after your OK (optionally after `run_week.py 8` cross-check).
