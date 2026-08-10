# Black-Box Bayesian Optimisation — Capstone

> **Main report:** open [`bbo_progress_report.html`](bbo_progress_report.html) for the interactive
> dashboard, or click [`bbo_progress_report.png`](bbo_progress_report.png) for the full image
> (also available as [`bbo_progress_report.jpg`](bbo_progress_report.jpg)).

> **Documentation (Module 21):** [`DATASHEET.md`](DATASHEET.md) (query history dataset) · [`MODEL_CARD.md`](MODEL_CARD.md) (optimisation approach)

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
| **F2** | **Noisy ML Log-Likelihood** | 2 | 2 settings → noisy log-likelihood | EI (+ White kernel) | Best **0.777** (W5) |
| **F3** | **Drug Discovery — Adverse Reactions** | 3 | component ratios → −(side effect) | UCB κ=2.576 | Best **−0.011** (W6) |
| **F4** | **Warehouse Placement** | 4 | 4 placement factors → efficiency | UCB κ=2.5 | Best **0.470** (W6) |
| **F5** | **Chemical Yield Optimisation** | 4 | 4 process settings → yield | EI exploit (after signal) | log(y) GP; best **3744** (W4/W7) |
| **F6** | **Cake Recipe Optimisation** | 5 | 5 ingredient amounts → −(badness) | EI | Best **−0.240** (W6) |
| **F7** | **ML Hyperparameter Tuning** | 6 | 6 hyperparameters → validation score | EI | Best **1.857** (W4) |
| **F8** | **8-Parameter ML Model Optimisation** | 8 | 8 parameters → score | UCB κ=2.576 | Best **9.865** (W7) |

Each `function_*/` folder contains a detailed `EXPLANATION_F*.md` (learn-from-scratch write-up) and a
comprehensive `analysis_F*.png` figure (data → GP → acquisition → weekly panels through Week 7).

## Repository layout

```
capstone/
├── BBO_Capstone_Optimized.ipynb   # Main GP + acquisition pipeline
├── bbo_progress_report.html       # Interactive dashboard (start here)
├── bbo_progress_report.png/jpg    # Full report image
├── run_week.py                    # Generate Week N queries from notebook logic
├── generate_week4.py / generate_week5.py   # Approved query generators
├── append_week2.py … append_week7.py       # Append portal y to .npy files
├── make_progress_report.py        # Iteration diagnostics table
├── make_function_analysis.py      # 9-panel per-function figures
├── make_main_report_image.py      # Dashboard PNG/JPG
├── make_progress_chart.py         # Best-y progress chart
├── WEEK*_STRATEGY.md              # Weekly queries + rationale
├── WEEK*_REFLECTION.md            # Post-results analysis
├── WEEK*_DISCUSSION.md            # Forum reflections
├── TECHNICAL_JUSTIFICATION.md     # Literature + library rationale
├── GITHUB_REPOSITORY_REFLECTION.md  # Repo structure & libraries (Module 16)
├── DATASHEET.md                   # Dataset documentation (Mini-lesson 21.1)
├── MODEL_CARD.md                  # Optimisation approach card (Mini-lesson 21.2)
└── function_1/ … function_8/
    ├── initial_inputs.npy
    ├── initial_outputs.npy
    ├── EXPLANATION_F*.md
    └── analysis_F*.png
```

## Weekly workflow

```bash
# 1. After portal email: append new y values
python append_week7.py          # edit script with portal results first

# 2. Regenerate reports (set WEEK in make_progress_chart.py if needed)
python make_progress_report.py
python make_function_analysis.py
python make_main_report_image.py
python make_progress_chart.py

# 3. Generate next week's queries
python run_week.py 8

# 4. Update WEEK*_STRATEGY.md, submit to portal, write forum reflection
```

## Repository contents

| Path | Description |
|------|-------------|
| **`DATASHEET.md`** | **Dataset datasheet** — motivation, composition, collection, uses, maintenance |
| **`MODEL_CARD.md`** | **Model card** — GP–BO approach, intended use, performance, limitations, ethics |
| **`bbo_progress_report.html`** | **Main progress report** — interactive dashboard (Week 1/2 tables, per-function links) |
| **`bbo_progress_report.png`** / **`.jpg`** | **Main report image** — click to view the full dashboard as a single picture |
| `make_main_report_image.py` | Regenerates the main report PNG/JPG from current data |
| `BBO_Capstone_Optimized.ipynb` | Main pipeline notebook (GP + AF, per-function strategy, plots) |
| `WEEK1_REFLECTION.md` | Reflection on Week 1 results (what worked, what didn't, why) |
| `WEEK2_STRATEGY.md` | Week 2 strategy and submitted queries |
| `WEEK2_REFLECTION.md` | Week 2 results analysis |
| `WEEK3_STRATEGY.md` | Week 3 strategy and results |
| `WEEK3_REFLECTION.md` | Week 3 results analysis |
| `WEEK4_STRATEGY.md` | Week 4 strategy, queries, and results |
| `WEEK4_REFLECTION.md` | Week 4 results analysis |
| `WEEK4_DISCUSSION.md` | Week 4 forum reflection (GP vs NN) |
| `WEEK5_STRATEGY.md` | Week 5 strategy and approved queries |
| `WEEK5_REFLECTION.md` | Week 5 results analysis |
| `WEEK5_DISCUSSION.md` | Week 5 forum reflection (Module 16 / DL lens) |
| `WEEK6_STRATEGY.md` / `WEEK6_REFLECTION.md` | Week 6 strategy and results |
| `WEEK6_DISCUSSION.md` | Week 6 forum reflection (Module 17 / CNN parallels) |
| `WEEK7_STRATEGY.md` / `WEEK7_REFLECTION.md` | Week 7 strategy and results (F1 B+ soft-signal) |
| `WEEK8_STRATEGY.md` | Week 8 draft strategy (awaiting approval) |
| `TECHNICAL_JUSTIFICATION.md` | Literature + library rationale (GP/EI/UCB; sklearn) |
| `GITHUB_REPOSITORY_REFLECTION.md` | Repo structure, libraries, documentation (Module 16) |
| `generate_week4.py` / `generate_week5.py` | Peer-informed / approved query generators |
| `append_week4.py` … `append_week7.py` | Append portal results to `.npy` files |
| `run_week.py` | Run notebook pipeline for Week N queries |
| `function_1/ … function_8/` | Per-function data (`.npy`), `EXPLANATION_F*.md`, and `analysis_F*.png` |
| `make_progress_report.py` | Builds the per-function iteration diagnostics report image |
| `make_function_analysis.py` | Builds the 9-panel per-function analysis figures |
| `progress_week7_report.png` / `.jpg` | Iteration tracking table through Week 7 |
| `progress_week1.png` … `progress_week7.png` | Best-observed-output progress charts |
| `function_*_week2_analysis.png` | Per-function Week 2 observation / input plots |

## Progress

- **Week 1 submitted.** 5 of 8 functions improved on the first query (F4, F5, F6, F7, F8).
- **F5** was the standout: 1089 → 2497 (+129%) after the explore→exploit switch.
- **F1** still reads ~0 (sparse peak — exploration continues); **F2/F3** did not improve, but for
  explainable reasons (noise / expected exploration cost).
- **Week 2 results received.** 1/8 improved — only **F3** (−0.168 → −0.020) after narrow-bounds fix.
  F5 exploit step returned 1811 (best remains 2497). See [`WEEK2_REFLECTION.md`](WEEK2_REFLECTION.md).
- **Week 3 results received.** 2/8 improved — **F5** 2497 → **3108**, **F7** 1.451 → **1.525**. See [`WEEK3_REFLECTION.md`](WEEK3_REFLECTION.md).
- **Week 4 results received.** **4/8 improved** — **F5** 3108 → **3744**, **F7** 1.525 → **1.857**, **F2** 0.611 → **0.660**. See [`WEEK4_REFLECTION.md`](WEEK4_REFLECTION.md).
- **Week 5 results received.** **3/8 improved** — **F2** 0.660 → **0.777**, **F6** −0.478 → **−0.265**, **F8** 9.796 → **9.864**. F5/F7 did not beat W4 records. See [`WEEK5_REFLECTION.md`](WEEK5_REFLECTION.md).
- **Week 6 results received.** **3/8 improved** — **F3** −0.020 → **−0.011**, **F4** 0.257 → **0.470**, **F6** −0.265 → **−0.240**. See [`WEEK6_REFLECTION.md`](WEEK6_REFLECTION.md).
- **Week 7 results received.** **1/8 improved** — **F8** 9.864 → **9.865**; F5 re-confirmed 3744 ridge; F1 B+ soft-signal still ~0. See [`WEEK7_REFLECTION.md`](WEEK7_REFLECTION.md).
- **Week 8 strategy drafted** — return-to-best for F2/F6/F7; F1 probes 2nd-best warm region. See [`WEEK8_STRATEGY.md`](WEEK8_STRATEGY.md).

See [`WEEK1_REFLECTION.md`](WEEK1_REFLECTION.md) through [`WEEK7_REFLECTION.md`](WEEK7_REFLECTION.md),
[`WEEK6_DISCUSSION.md`](WEEK6_DISCUSSION.md), [`TECHNICAL_JUSTIFICATION.md`](TECHNICAL_JUSTIFICATION.md),
and `progress_week7_report.png` for diagnostics.

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
- **Prior work & tooling.** See [`TECHNICAL_JUSTIFICATION.md`](TECHNICAL_JUSTIFICATION.md) for the
  short literature/library rationale (Rasmussen & Williams; Jones et al.; Srinivas et al.; scikit-learn).
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

### Why not PyTorch / TensorFlow as the surrogate?

Module 16 covers PyTorch and TensorFlow for building and scaling neural networks. I use those ideas in **forum reflections** (see [`WEEK5_DISCUSSION.md`](WEEK5_DISCUSSION.md)), but the portal pipeline stays GP-based: with 14–44 observations per function, NNs risk overfitting and do not provide calibrated uncertainty for EI/UCB without extra machinery (ensembles, MC dropout). See also [`GITHUB_REPOSITORY_REFLECTION.md`](GITHUB_REPOSITORY_REFLECTION.md).

### Why not SVM as the surrogate?

SVM regression could predict `y`, but UCB/EI need **μ and σ** at candidate points. GP provides both
naturally; SVM would require extra machinery (e.g. ensembles, Platt scaling) for uncertainty. For this
capstone, **GP + acquisition** is the correct tool; SVM appears in the README as a **kernel-method
parallel**, not a replacement.

---

## Week 5 portal submission (results received)

See [`WEEK5_STRATEGY.md`](WEEK5_STRATEGY.md) and [`WEEK5_REFLECTION.md`](WEEK5_REFLECTION.md).

Submitted queries and outcomes: **3/8 improved** (F2, F6, F8).

## Requirements

- Python 3.x
- `numpy`, `scikit-learn`, `scipy`, `matplotlib`

```bash
pip install numpy scikit-learn scipy matplotlib
```

Open `BBO_Capstone_Optimized.ipynb` in Jupyter and run all cells to reproduce the per-function GP
fits, acquisition decisions, and the next query points.
