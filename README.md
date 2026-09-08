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

## Impact — best-so-far through Week 12

Blue step = incumbent; grey points = each evaluation; red dashed line = first weekly BO query (after the seed set).

![Best-so-far trends for F1–F8](reports/analysis/progress_best_so_far.png)

| What the charts show | Takeaway |
|----------------------|----------|
| **F5** chemical yield | Large jump once the high face / \(x_1\) ridge was found (~3801) |
| **F4 / F7 / F8** | Steady late climbs under trust-region exploit |
| **F2** | Sharp ridge to **0.777**; later neighbour steps often miss |
| **F6** | Strong Week-10 basin (−0.136); fragile to off-centroid steps |
| **F1** | Long null phase; measurable lobe only late near (0.64, 0.68) |
| **F3** | Safe band held near **−0.011** |

Full visual pack (3D cluster hulls + pair panels): [`reports/analysis/README.md`](reports/analysis/README.md).

![3D promising clusters F1–F8](reports/analysis/cluster_gallery_3d.png)

---

## Results — best-so-far by week

Values are the **incumbent** (running max of \(y\)) after each round. Bold = improved that week.

### Late rounds (Weeks 8–12)

| Fn | Task | Dim | Seed | W8 | W9 | W10 | W11 | W12 |
|----|------|-----|------|----|----|-----|-----|-----|
| F1 | Radiation | 2 | **7.711×10⁻¹⁶** | 7.711×10⁻¹⁶ | 7.711×10⁻¹⁶ | 7.711×10⁻¹⁶ | 7.711×10⁻¹⁶ | 7.711×10⁻¹⁶ |
| F2 | Noisy ML | 2 | 0.611 | **0.777** | 0.777 | 0.777 | 0.777 | 0.777 |
| F3 | Drug side-effects | 3 | −0.035 | **−0.011** | −0.011 | −0.011 | −0.011 | −0.011 |
| F4 | Warehouse | 4 | −4.026 | 0.572 | **0.642** | **0.667** | **0.675** | **0.679** |
| F5 | Chemical yield | 4 | 1089 | 3760 | **3769** | **3779** | **3790** | **3801** |
| F6 | Cake recipe | 5 | −0.714 | −0.240 | −0.240 | **−0.136** | −0.136 | −0.136 |
| F7 | HP tuning | 6 | 1.365 | 1.857 | **1.858** | **1.863** | **1.866** | **1.872** |
| F8 | 8-param ML | 8 | 9.598 | 9.868 | **9.869** | **9.871** | **9.872** | **9.873** |

**Improved count:** W8 **3/8** · W9 **4/8** · W10 **5/8** · W11 **4/8** · W12 **4/8** (F4, F5, F7, F8).

### Notes on the incumbents

| Fn | Detail |
|----|--------|
| **F1** | Absolute best remains the seed reading **7.711×10⁻¹⁶**. Weeks 10–12 opened a measurable signal lobe near (0.64, 0.68) with readings **−0.00807 → −0.00623 → −0.00512** (still below the seed max, but the first non-null basin). |
| F2 | Sharp ridge peak **0.776645**; late neighbour steps often land ~0.54. |
| F3 | Safe \(x_3\) band; best **−0.011366**. |
| F4 / F7 / F8 | Trust-region micro-gains through Week 12. |
| F5 | High-face ridge; \(x_1\) climb to ≈0.44 → **3800.74**. |
| F6 | Week-10 basin **−0.136** still stands after a Week-11 collapse and partial return. |

Per-function 9-panel diagnostics: `data/function_*/analysis_F*.png` · write-ups: `EXPLANATION_F*.md`.

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
