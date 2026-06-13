# Black-Box Bayesian Optimisation — Capstone

> **Main report:** open [`bbo_progress_report.html`](bbo_progress_report.html) for the interactive
> dashboard, or click [`bbo_progress_report.png`](bbo_progress_report.png) for the full image
> (also available as [`bbo_progress_report.jpg`](bbo_progress_report.jpg)).

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
| **F4** | **Warehouse Placement** | 4 | 4 placement factors → efficiency | UCB κ=2.5 | Multimodal; local basin search after W2 dip |
| **F5** | **Chemical Yield Optimisation** | 4 | 4 process settings → yield | EI exploit (after signal) | log(y) GP; EI over f*=2497 |
| **F6** | **Cake Recipe Optimisation** | 5 | 5 ingredient amounts → −(badness) | EI | Balanced push toward 0 |
| **F7** | **ML Hyperparameter Tuning** | 6 | 6 hyperparameters → validation score | EI | Balanced search in 6D |
| **F8** | **8-Parameter ML Model Optimisation** | 8 | 8 parameters → score | UCB κ=2.576 | Broad exploration of a large space |

Each `function_*/` folder contains a detailed `EXPLANATION_F*.md` (learn-from-scratch write-up) and a
comprehensive `analysis_F*.png` figure (data → GP → acquisition → Week 1 → Week 2).

## Repository contents

| Path | Description |
|------|-------------|
| **`bbo_progress_report.html`** | **Main progress report** — interactive dashboard (Week 1/2 tables, per-function links) |
| **`bbo_progress_report.png`** / **`.jpg`** | **Main report image** — click to view the full dashboard as a single picture |
| `make_main_report_image.py` | Regenerates the main report PNG/JPG from current data |
| `BBO_Capstone_Optimized.ipynb` | Main pipeline notebook (GP + AF, per-function strategy, plots) |
| `WEEK1_REFLECTION.md` | Reflection on Week 1 results (what worked, what didn't, why) |
| `WEEK2_STRATEGY.md` | Week 2 strategy and submitted queries |
| `WEEK2_REFLECTION.md` | Week 2 results analysis |
| `WEEK3_STRATEGY.md` | Week 3 strategy and portal submission block |
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
- **Week 2 results received.** 1/8 improved — only **F3** (−0.168 → −0.020) after narrow-bounds fix.
  F5 exploit step returned 1811 (best remains 2497). See [`WEEK2_REFLECTION.md`](WEEK2_REFLECTION.md).
- **Week 3 queries ready** — see [`WEEK3_STRATEGY.md`](WEEK3_STRATEGY.md) for rationale and portal values.

See [`WEEK1_REFLECTION.md`](WEEK1_REFLECTION.md), [`WEEK2_REFLECTION.md`](WEEK2_REFLECTION.md),
[`WEEK2_STRATEGY.md`](WEEK2_STRATEGY.md), and `progress_week3_report.png` for diagnostics.

---

## Stage 2 — purpose, inputs/outputs, and iterative modelling

This repository documents **Stage 2** of the Imperial PCMLAI BBO capstone: optimising eight hidden
functions with one expensive query per function per week (~13 weeks). The objective is not to find
the perfect point immediately, but to **reason, iterate, and adapt** as new `y` values arrive.

| | Description |
|---|-------------|
| **Inputs** | Normalised vectors `x ∈ [0,1]^d` (d = 2…8), one per function per week |
| **Outputs** | Scalar `y` (maximise); stored in `function_*/initial_outputs.npy` |
| **Objective** | Maximise each black-box function under a strict query budget |
| **Approach** | GP surrogate → acquisition function → next `x` → append data → repeat |

### Connection to course modules (regression, kernels, SVM)

- **Gaussian Process = kernel regression with uncertainty.** Like ridge/kernel regression, the GP
  uses a Matérn kernel over `x` to predict `y`. Unlike plain regression, it also returns **σ(x)**,
  which drives UCB and EI — this uncertainty is what makes BO work.
- **SVM link (conceptual, not used as surrogate here).** SVMs and GPs both rely on **kernel
  similarity** between inputs. We use Matérn kernels in the GP for the same reason SVMs use RBF
  kernels: smooth, localised influence in input space. We do **not** replace the GP with an SVM
  because standard SVMs do not provide calibrated predictive variance for acquisition functions.
- **Iterative modelling.** Each week is one loop of: fit model on all data so far → choose where to
  sample next → observe → update beliefs. Week 1 (5/8 improved) and Week 2 (1/8, F3 fix) show that
  progress comes from **strategy refinement**, not lucky one-shots.

### Preprocessing and scaling (what we actually do)

| Transform | Where | When |
|-----------|--------|------|
| **`normalize_y=True`** | `GaussianProcessRegressor` | Always — scales `y` internally for stable fitting |
| **`log_transform_y`** | `fit_gp()` | **F5 only** — yield spans ~0.1–2500; log compresses dynamic range |
| **WhiteKernel** | F2 GP | Absorbs observation noise (noisy log-likelihood) |
| **Input scaling** | Not applied | `x` already in [0,1]^d from the portal; extra StandardScaler omitted |
| **Per-function α, ν** | `FUNCTIONS` config | F1 ν=0.5 (sharp), F3/F8 ν=1.5, etc. |

We apply log/scaling **only where the data justify it** (F5 magnitude; F2 noise), not blindly to
all functions.

### Why not SVM as the surrogate?

SVM regression could predict `y`, but UCB/EI need **μ and σ** at candidate points. GP provides both
naturally; SVM would require extra machinery (e.g. ensembles, Platt scaling) for uncertainty. For this
capstone, **GP + acquisition** is the correct tool; SVM appears in the README as a **kernel-method
parallel**, not a replacement.

---

## Week 3 portal submission

```
Function 1:  0.070000-0.669525
Function 2:  0.718765-0.926564
Function 3:  0.642581-0.691593-0.478715
Function 4:  0.343955-0.453869-0.398079-0.433861
Function 5:  0.150000-0.926480-0.980000-0.980000
Function 6:  0.524058-0.360869-0.413794-0.897694-0.020000
Function 7:  0.070000-0.491672-0.247422-0.167429-0.353878-0.715603
Function 8:  0.070000-0.070000-0.020000-0.038786-0.403935-0.930000-0.020000-0.893085
```

## Requirements

- Python 3.x
- `numpy`, `scikit-learn`, `scipy`, `matplotlib`

```bash
pip install numpy scikit-learn scipy matplotlib
```

Open `BBO_Capstone_Optimized.ipynb` in Jupyter and run all cells to reproduce the per-function GP
fits, acquisition decisions, and the next query points.
