# Week 4 Strategy — Black-Box Bayesian Optimisation

*After Week 3 results: F5 → 3108, F7 → 1.525 (2/8 improved).*

## Week 4 queries (submit)

```
F1: 0.662502-0.070000
F2: 0.709311-0.406719
F3: 0.492581-0.611593-0.521038
F4: 0.427912-0.347959-0.398079-0.465276
F5: 0.300000-0.980000-0.980000-0.980000
F6: 0.429970-0.020000-0.980000-0.883280-0.020000
F7: 0.070000-0.070000-0.247422-0.144873-0.351501-0.694213
F8: 0.195586-0.070000-0.233778-0.038786-0.403935-0.460628-0.234045-0.893085
```

## Rationale snapshot

| Fn | Mode | Focus |
|----|------|-------|
| F1 | Coverage | Interior gap search |
| F2 | EI | Explore away from saturated high-x₂ region |
| F3 | UCB + narrow | Return toward best (−0.020) |
| F4 | UCB basin ±0.06 | Positive region around 0.257 best |
| F5 | EI exploit | Climb from 3108; x₁ pushed toward 0.30 |
| F6 | EI | Best region |
| F7 | EI | Exploit new best 1.525 |
| F8 | UCB + penalty | Broad 8D exploration |
