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

## Quick links

| What | Where |
|------|--------|
| Datasheet | [`DATASHEET.md`](DATASHEET.md) |
| Model card | [`MODEL_CARD.md`](MODEL_CARD.md) |
| Main notebook | [`notebooks/BBO_Capstone_Optimized.ipynb`](notebooks/BBO_Capstone_Optimized.ipynb) |
| Approach presentation (PDF text) | [`docs/approach_presentation.md`](docs/approach_presentation.md) |
| Visual gallery (renders on GitHub) | [`reports/analysis/README.md`](reports/analysis/README.md) |
| Progress notes / early HTML | [`reports/progress/README.md`](reports/progress/README.md) |
| Week 13 final queries | [`weeks/WEEK13_STRATEGY.md`](weeks/WEEK13_STRATEGY.md) |
| Project reflection | [`weeks/project_reflection.md`](weeks/project_reflection.md) |
| Successful strategies | [`weeks/successful_strategies_reflection.md`](weeks/successful_strategies_reflection.md) |
| Final-round RL reflection | [`weeks/final_round_rl_reflection.md`](weeks/final_round_rl_reflection.md) |
| Course file map | [`docs/COURSE_INDEX.md`](docs/COURSE_INDEX.md) |

---

## Results after Week 12

| Fn | Task | Dim | Best y | Note |
|----|------|-----|--------|------|
| F1 | Radiation | 2 | ~0 | Signal lobe ~0.64 / 0.68 |
| F2 | Noisy ML | 2 | **0.777** | Sharp ridge |
| F3 | Drug side-effects | 3 | **−0.011** | Safe x₃ band |
| F4 | Warehouse | 4 | **0.679** | Week 12 |
| F5 | Chemical yield | 4 | **3801** | Ridge x₁ → 0.44 |
| F6 | Cake recipe | 5 | **−0.136** | Week 10 incumbent |
| F7 | HP tuning | 6 | **1.872** | Week 12 |
| F8 | 8-param ML | 8 | **9.873** | Week 12 |

Late streak: Week 10 **5/8** · Weeks 11–12 **4/8** each (F4, F5, F7, F8).

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
└── data/function_1…8/        # Evaluation history (.npy) + notes
```

Evaluation histories are small NumPy files under `data/` (course portal outputs). There is no large external dataset to host off-GitHub.

---

## How to reproduce

```bash
pip install numpy scikit-learn scipy matplotlib
python scripts/make_cluster_gallery.py
```

Open [`notebooks/BBO_Capstone_Optimized.ipynb`](notebooks/BBO_Capstone_Optimized.ipynb) from the repository root (it expects `data/` beside `notebooks/`).

Weekly notes live under [`weeks/`](weeks/). Method detail: [`docs/TECHNICAL_JUSTIFICATION.md`](docs/TECHNICAL_JUSTIFICATION.md).
