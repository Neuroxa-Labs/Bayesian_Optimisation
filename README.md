# Black-Box Bayesian Optimisation — Capstone

A Bayesian Optimisation (BO) pipeline for optimising **8 unknown black-box functions** (F1–F8,
dimensions 2D–8D). The true functions are hidden: each week we submit **one query point `x` per
function** and receive a single output `y`, which we add to our dataset and use to choose the next
point. The goal is to **maximise** each function within a limited number of weekly queries.

## How it works

```
1. Fit a Gaussian Process (GP) surrogate to the current data
2. Pick an acquisition function (AF) for each function
3. Optimise the AF to propose the next query point x
4. Submit x  ->  receive y  ->  append to data
5. Repeat each week
```

- **Surrogate model:** Gaussian Process (per-function kernels / noise settings).
- **Acquisition functions:** `UNCERTAINTY` (pure exploration), `UCB` (μ + κ·σ, tunable
  explore/exploit), and `EI` (Expected Improvement, robust under noise).
- **Explore → exploit schedule:** weeks 1–4 explore, 5–9 balanced, 10–13 exploit. Two functions
  (F1, F5) additionally switch based on a **signal threshold** rather than the calendar.

## Per-function configuration

| Fn | Dim | Profile | Primary AF | Why |
|----|-----|---------|-----------|-----|
| F1 | 2 | Sparse, sharp peak (radiation source) | UNCERTAINTY → UCB | Mostly zeros; explore until any signal appears |
| F2 | 2 | Noisy log-likelihood | EI (+ White kernel) | Noise-robust improvement |
| F3 | 3 | All-negative (drug discovery) | UCB κ=2.576 | Steer toward least-negative region |
| F4 | 4 | Multimodal (warehouse) | UCB κ=3.0 | High exploration to avoid local optima |
| F5 | 4 | Single broad peak (chemical yield) | UCB (explore→exploit) | Find signal, then exploit hard |
| F6 | 5 | Negative score (cake recipe) | EI | Balanced push toward 0 |
| F7 | 6 | High-dim (hyperparameter tuning) | EI | Balanced search in 6D |
| F8 | 8 | High-dim (8-param ML) | UCB κ=2.576 | Broad exploration of a large space |

## Repository contents

| Path | Description |
|------|-------------|
| `BBO_Capstone_Optimized.ipynb` | Main pipeline notebook (GP + AF, per-function strategy, plots) |
| `WEEK1_REFLECTION.md` | Reflection on Week 1 results (what worked, what didn't, why) |
| `WEEK2_STRATEGY.md` | Refined Week 2 strategy, per function, with reasoning |
| `function_1/ … function_8/` | Input/output data (`.npy`) for each function (incl. Week 1 point) |
| `make_progress_report.py` | Builds the per-function iteration diagnostics report image |
| `progress_week2_report.png` / `.jpg` | Iteration tracking table (Current Best, acquisition, result, method, ν, κ/ξ, length scales) |
| `progress_week1.png`, `progress_week2.png` | Best-observed-output progress charts |
| `function_*_week2_analysis.png` | Per-function Week 2 observation / input plots |

## Progress

- **Week 1 submitted.** 5 of 8 functions improved on the first query (F4, F5, F6, F7, F8).
- **F5** was the standout: 1089 → 2497 (+129%) after the explore→exploit switch.
- **F1** still reads ~0 (sparse peak — exploration continues); **F2/F3** did not improve, but for
  explainable reasons (noise / expected exploration cost).
- **Week 2 queries generated.** Refinements this iteration:
  - **Per-function Matérn smoothness ν**: ν=0.5 for F1 (sharp/sparse peak), ν=1.5 for F3 and F8,
    ν=2.5 for the rest. Sensitivity testing showed F1, F3 and F8 candidate locations change
    meaningfully with ν — confirming the per-function choice.
  - **Anti-duplicate guard**: if the optimiser proposes a point that coincides with an existing
    observation (e.g. F5 sitting on its own best), it switches to a small local exploration around
    the peak instead of wasting a query.

See [`WEEK1_REFLECTION.md`](WEEK1_REFLECTION.md) and [`WEEK2_STRATEGY.md`](WEEK2_STRATEGY.md) for the
full reasoning, and `progress_week2_report.png` for the per-iteration diagnostics table.

## Requirements

- Python 3.x
- `numpy`, `scikit-learn`, `scipy`, `matplotlib`

```bash
pip install numpy scikit-learn scipy matplotlib
```

Open `BBO_Capstone_Optimized.ipynb` in Jupyter and run all cells to reproduce the per-function GP
fits, acquisition decisions, and the next query points.
