# Black-Box Bayesian Optimisation — Capstone

> **Main report:** open [`bbo_progress_report.html`](bbo_progress_report.html) for a single-page
> overview of all 8 functions — Week 1 results, Week 2 queries, length scales, and links to each
> per-function explanation and analysis figure.

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

## The 8 functions — real-world meaning

Each black box stands in for a real optimisation problem. Naming them by their real-world task
(rather than "Function 1…8") makes the contribution concrete: every weekly query is like running
one expensive real experiment.

| Fn | Real-world task | Dim | What `x` / `y` mean | Primary AF | Why this AF |
|----|-----------------|-----|---------------------|-----------|-------------|
| **F1** | **Radiation Source Detection** | 2 | position → counter reading (sharp, sparse peak; mostly 0) | UNCERTAINTY → UCB | Mostly zeros; explore until any signal appears |
| **F2** | **Noisy ML Log-Likelihood** | 2 | 2 settings → noisy log-likelihood | EI (+ White kernel) | Noise-robust improvement |
| **F3** | **Drug Discovery — Adverse Reactions** | 3 | component ratios → −(side effect) | UCB κ=2.576 | Steer toward least-negative region |
| **F4** | **Warehouse Placement** | 4 | 4 placement factors → efficiency | UCB κ=3.0 | High exploration to avoid local optima |
| **F5** | **Chemical Yield Optimisation** | 4 | 4 process settings → yield | UCB (explore→exploit) | Find signal, then exploit hard |
| **F6** | **Cake Recipe Optimisation** | 5 | 5 ingredient amounts → −(badness) | EI | Balanced push toward 0 |
| **F7** | **ML Hyperparameter Tuning** | 6 | 6 hyperparameters → validation score | EI | Balanced search in 6D |
| **F8** | **8-Parameter ML Model Optimisation** | 8 | 8 parameters → score | UCB κ=2.576 | Broad exploration of a large space |

Each `function_*/` folder contains a detailed `EXPLANATION_F*.md` (learn-from-scratch write-up) and a
comprehensive `analysis_F*.png` figure (data → GP → acquisition → Week 1 → Week 2).

## Repository contents

| Path | Description |
|------|-------------|
| **`bbo_progress_report.html`** | **Main progress report** — single-page dashboard (Week 1/2 tables, visuals, per-function links) |
| `BBO_Capstone_Optimized.ipynb` | Main pipeline notebook (GP + AF, per-function strategy, plots) |
| `WEEK1_REFLECTION.md` | Reflection on Week 1 results (what worked, what didn't, why) |
| `WEEK2_STRATEGY.md` | Refined Week 2 strategy, per function, with reasoning |
| `function_1/ … function_8/` | Per-function data (`.npy`), `EXPLANATION_F*.md`, and `analysis_F*.png` |
| `make_progress_report.py` | Builds the per-function iteration diagnostics report image |
| `make_function_analysis.py` | Builds the 9-panel per-function analysis figures |
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
