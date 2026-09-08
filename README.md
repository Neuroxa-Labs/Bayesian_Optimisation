# Black-Box Bayesian Optimisation

Imperial College London · PCMLAI Stage 2 capstone  
Maximise **eight unknown black-box functions** (2D–8D) with **one query per function per week**.

| | |
|--|--|
| **Method** | Gaussian Process (Matérn + ARD) · EI / UCB · trust-region exploit |
| **Extras** | WhiteKernel on F2 · log-y on F5 · F1 trust gate · per-function locks |
| **Status** | Weeks 1–12 complete · Week 13 (final) queries locked · awaiting portal results |
| **Repository** | https://github.com/Neuroxa-Labs/Bayesian_Optimisation |

---

## For a general audience

We ran a careful series of experiments on eight hidden scoring problems — from locating a radiation source to tuning machine-learning models and chemical recipes. Each week we could try only one setting per problem, so random guessing would waste the budget. Instead we used past results to choose the next trial: focus where scores were already improving, change course when a region looked dead, and keep steps small near the best known settings. Several scores rose steadily over the project, especially chemical yield and the warehouse / hyperparameter tasks, and this repository records what we tried and why.

---

## Approach in brief

1. Fit a **Matérn GP** with ARD length scales on the growing \((x, y)\) history.
2. Score candidates with **EI** or **UCB**, then search globally and inside a **trust region** around the incumbent.
3. Apply **per-function rules**: F1 trust gate (no exploit on a null map), F2 WhiteKernel, F3 safe \(x_3\), F5 high-face ridge + log-\(y\), boundary penalties, anti-duplicate.
4. Submit one six-decimal portal string per function; append the returned \(y\); repeat.

Late policy (Weeks 10–13): stay inside proven basins, move only sensitive axes, and hard-return after a failed neighbour step (especially F2 / F6).

Executable pipeline: [`notebooks/BBO_Capstone_Optimized.ipynb`](notebooks/BBO_Capstone_Optimized.ipynb).  
Method write-up: [`docs/TECHNICAL_JUSTIFICATION.md`](docs/TECHNICAL_JUSTIFICATION.md) · presentation text: [`docs/approach_presentation.md`](docs/approach_presentation.md).

---

## The eight problems (plain English)

Each “function” is a **hidden scoring machine**: you propose settings \(x\), the portal returns a score \(y\). Higher \(y\) is always better. You never see the formula — only the history of tries. That is why this is called **black-box** optimisation.

| | Meaning |
|--|--|
| **\(x\)** | The knobs you choose (2 to 8 numbers, each between 0 and 1) |
| **\(y\)** | The score the course portal returns for that choice |
| **Budget** | One new try per function per week |

### F1 — Radiation source (2 knobs)

**Story.** Find a hidden radiation source on a map. Most places read almost zero; only a tiny region “lights up.”  
**What we found.** The official best is still a near-zero seed reading (**7.711×10⁻¹⁶**). Weeks 10–12 finally hit a real signal area near \((0.64,\ 0.68)\) with readings **−0.00807 → −0.00623 → −0.00512** — still below the seed max, but the first usable basin to refine in the final round.

### F2 — Noisy machine-learning score (2 knobs)

**Story.** Tune two settings of an ML model when the score is **noisy** (the same \(x\) can look different by chance).  
**What we found.** A sharp ridge peaks at **0.776645**. Steps that look “nearby” often fall to ~0.54, so late weeks hard-return toward the historical peak.

### F3 — Drug mixture / side effects (3 knobs)

**Story.** Mix three ingredients; \(y\) is a safety score (closer to zero = safer).  
**What we found.** Best **−0.011366** once a safe band for the sensitive third ingredient (\(x_3\)) was locked and kept.

### F4 — Warehouse layout (4 knobs)

**Story.** Arrange warehouse factors to raise efficiency. Many local traps early on.  
**What we found.** Climbed from a poor start to **0.6786** by Week 12 with small local steps inside a proven basin.

### F5 — Chemical yield (4 knobs)

**Story.** Maximise reaction yield. One strong “ridge” appears once the right face of the box is found.  
**What we found.** Biggest success story: seed ~1089 → **3800.74** by locking high \(x_2\)–\(x_4\) and climbing \(x_1\) (≈0.44).

### F6 — Cake recipe (5 knobs)

**Story.** Five ingredient amounts; the judge scores how bad the cake is (we maximise the negative of badness, so nearer zero is better).  
**What we found.** Best **−0.136** at Week 10. A small off-centre step collapsed the score in Week 11; later weeks return toward that basin.

### F7 — Hyperparameter tuning (6 knobs)

**Story.** Six ML training knobs; \(y\) is a validation score.  
**What we found.** Slow, steady local gains to **1.872** by Week 12 — move sensitive axes, leave flat ones alone.

### F8 — Eight-parameter ML model (8 knobs)

**Story.** Largest search space; expect slow progress.  
**What we found.** Incremental ticks to **9.8729** by Week 12 under a tight trust region.

More detail per function: `data/function_*/EXPLANATION_F*.md` and `analysis_F*.png`.

---

## Impact — best-so-far through Week 12

Blue step = incumbent; grey points = each evaluation; red dashed line = first weekly BO query (after the seed set).

![Best-so-far trends for F1–F8](reports/analysis/progress_best_so_far.png)

| Chart | Takeaway |
|-------|----------|
| **F5** | Large jump once the yield ridge was found (~3801) |
| **F4 / F7 / F8** | Steady late climbs under trust-region exploit |
| **F2** | Sharp ridge to **0.777**; later neighbour steps often miss |
| **F6** | Strong Week-10 basin (−0.136); fragile to off-centroid steps |
| **F1** | Long null phase; measurable lobe only late near (0.64, 0.68) |
| **F3** | Safe band held near **−0.011** |

Full visual pack: [`reports/analysis/README.md`](reports/analysis/README.md).

![3D promising clusters F1–F8](reports/analysis/cluster_gallery_3d.png)

---

## Results — compact week comparison

Incumbent = best \(y\) seen so far. Few columns so the table stays readable. Bold = new best that week.

| | Seed | W8 | W10 | W12 |
|--|-----:|---:|----:|----:|
| **F1** | **7.71e−16** | 7.71e−16 | 7.71e−16 | 7.71e−16 |
| **F2** | 0.611 | **0.777** | 0.777 | 0.777 |
| **F3** | −0.035 | **−0.011** | −0.011 | −0.011 |
| **F4** | −4.03 | 0.572 | **0.667** | **0.679** |
| **F5** | 1089 | 3760 | **3779** | **3801** |
| **F6** | −0.714 | −0.240 | **−0.136** | −0.136 |
| **F7** | 1.365 | 1.857 | **1.863** | **1.872** |
| **F8** | 9.598 | 9.868 | **9.871** | **9.873** |

**Queries that beat the previous best:** W8 3/8 · W9 4/8 · W10 **5/8** · W11 4/8 · W12 4/8 (F4, F5, F7, F8).

**How to read this.** Seed = after the free starting data. W8 / W10 / W12 = after those weekly rounds. F5’s jump and F4/F7/F8’s late climb are the clearest “BO paid off” stories; F1/F2/F6 show how fragile sparse peaks and sharp basins can be.

**Week 13 portal block** (final round — see [`WEEK13_STRATEGY.md`](weeks/WEEK13_STRATEGY.md)):

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

---

## Quick links

| What | Where |
|------|--------|
| Datasheet | [`DATASHEET.md`](DATASHEET.md) |
| Model card | [`MODEL_CARD.md`](MODEL_CARD.md) |
| Main notebook | [`notebooks/BBO_Capstone_Optimized.ipynb`](notebooks/BBO_Capstone_Optimized.ipynb) |
| Approach presentation (PDF text) | [`docs/approach_presentation.md`](docs/approach_presentation.md) |
| Visual gallery | [`reports/analysis/README.md`](reports/analysis/README.md) |
| Week 13 final queries | [`weeks/WEEK13_STRATEGY.md`](weeks/WEEK13_STRATEGY.md) |
| Project reflection | [`weeks/project_reflection.md`](weeks/project_reflection.md) |
| Successful strategies | [`weeks/successful_strategies_reflection.md`](weeks/successful_strategies_reflection.md) |
| Final-round RL reflection | [`weeks/final_round_rl_reflection.md`](weeks/final_round_rl_reflection.md) |
| Course file map | [`docs/COURSE_INDEX.md`](docs/COURSE_INDEX.md) |

---

## Repository structure

```text
Bayesian_Optimisation/
├── README.md                 # This page
├── DATASHEET.md              # Dataset transparency
├── MODEL_CARD.md             # Method transparency
├── docs/                     # Presentation text, course index, technical notes
├── weeks/                    # Weekly strategy, reflections, discussions
├── reports/analysis/         # Current gallery (Markdown + PNG; GitHub-friendly)
├── reports/progress/         # Early-weeks HTML log + snapshot images
├── notebooks/                # GP + acquisition pipeline
├── scripts/                  # Append results, regenerate figures
└── data/function_1…8/        # Evaluation history (.npy) + analysis + notes
```

---

## How to reproduce

```bash
pip install numpy scikit-learn scipy matplotlib
python scripts/make_cluster_gallery.py
python scripts/make_function_analysis.py
python scripts/make_explanations.py
```

Open [`notebooks/BBO_Capstone_Optimized.ipynb`](notebooks/BBO_Capstone_Optimized.ipynb) from the repository root (it expects `data/` beside `notebooks/`).
