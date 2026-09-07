# Black-Box Bayesian Optimisation — Capstone

Imperial PCMLAI Stage 2: maximise **eight unknown black-box functions** (2D–8D) with **one query per function per week**.

This repository is both a **portfolio artefact** (clear method, results, and docs) and the **course submission** (all required materials linked below).

| | |
|--|--|
| **Surrogate** | Gaussian Process (Matérn + ARD; WhiteKernel on F2; log-y on F5) |
| **Acquisition** | EI / UCB + trust-region exploit; trust gate when signal is absent (F1) |
| **Status** | **Week 12 complete** · Final-round queries ready · Public portfolio |
| **Repo** | https://github.com/Neuroxa-Labs/Bayesian_Optimisation |

---

## For a general audience (~100 words)

We ran a careful series of experiments on eight hidden scoring problems (from finding a radiation source to tuning ML models and chemical recipes). Each week we could try only one setting per problem, so guessing at random would waste the budget. Instead we used past results to decide the next try: focus where scores were already improving, change course quickly when a region looked dead, and keep steps small near the best known settings. Over the project this raised several of the scores steadily — especially chemical yield and the warehouse / hyperparameter tasks — and left a clear public record of what we tried and why.

---

## Start here

| Resource | Link |
|----------|------|
| **Datasheet** | [`DATASHEET.md`](DATASHEET.md) |
| **Model card** | [`MODEL_CARD.md`](MODEL_CARD.md) |
| **Main pipeline (Jupyter)** | [`notebooks/BBO_Capstone_Optimized.ipynb`](notebooks/BBO_Capstone_Optimized.ipynb) |
| **Approach presentation** | [`docs/approach_presentation.md`](docs/approach_presentation.md) |
| **Project reflection** | [`weeks/project_reflection.md`](weeks/project_reflection.md) |
| **Successful strategies** | [`weeks/successful_strategies_reflection.md`](weeks/successful_strategies_reflection.md) |
| **Final-round RL reflection** | [`weeks/final_round_rl_reflection.md`](weeks/final_round_rl_reflection.md) |
| **Final-round portal queries** | [`weeks/final_round_strategy.md`](weeks/final_round_strategy.md) |
| **Week 12 results** | [`weeks/WEEK12_REFLECTION.md`](weeks/WEEK12_REFLECTION.md) |
| **Cluster & progress gallery** | [`reports/analysis/cluster_gallery.html`](reports/analysis/cluster_gallery.html) |
| **Interactive dashboard** | [`reports/progress/bbo_progress_report.html`](reports/progress/bbo_progress_report.html) |
| **Course ↔ file map** | [`docs/COURSE_INDEX.md`](docs/COURSE_INDEX.md) |

---

## Repository layout

```text
Bayesian_Optimisation/
├── README.md
├── DATASHEET.md              # Data transparency
├── MODEL_CARD.md             # Method transparency
├── docs/                     # Technical notes, presentation, course index
├── weeks/                    # Weekly strategy / reflection / discussions
├── reports/                  # Dashboards + cluster gallery
├── notebooks/                # GP + acquisition pipeline
├── scripts/                  # Reproducible utilities
└── data/function_1…8/        # .npy history + per-function notes
```

**Data note.** Histories are small NumPy arrays in `data/function_*/` (course portal outputs). No large external dataset is hosted on GitHub; see [`DATASHEET.md`](DATASHEET.md).

### Visual analysis

| Figure | File |
|--------|------|
| 3D cluster gallery (F1–F8) | [`cluster_gallery_3d.png`](reports/analysis/cluster_gallery_3d.png) |
| Best-so-far progress | [`progress_best_so_far.png`](reports/analysis/progress_best_so_far.png) |
| Hull + progress pairs (F3/F5/F7) | [`cluster_progress_pairs.png`](reports/analysis/cluster_progress_pairs.png) |
| HTML viewer | [`cluster_gallery.html`](reports/analysis/cluster_gallery.html) |

---

## Best so far (after Week 12)

| Fn | Task | Dim | Best y (approx.) | Note |
|----|------|-----|------------------|------|
| F1 | Radiation | 2 | ~0 | Signal lobe ~0.64/0.68 (W10–W12) |
| F2 | Noisy ML | 2 | **0.777** | Sharp ridge; late misses ~0.54 |
| F3 | Drug side-effects | 3 | **−0.011** | Safe x₃ band |
| F4 | Warehouse | 4 | **0.679** | W12 |
| F5 | Chemical yield | 4 | **3801** | Ridge x₁→0.44 |
| F6 | Cake recipe | 5 | **−0.136** | W10 best; W12 partial return |
| F7 | HP tuning 6D | 6 | **1.872** | W12 |
| F8 | 8-param ML | 8 | **9.873** | W12 |

**Week 8:** 3/8 · **Week 9:** 4/8 · **Week 10:** 5/8 · **Week 11:** 4/8 · **Week 12:** **4/8** (F4, F5, F7, F8).

---

## Weekly notes

Under [`weeks/`](weeks/): `WEEK*_STRATEGY.md`, `WEEK*_REFLECTION.md`, `WEEK*_DISCUSSION.md`, plus final-round and project-level reflections.

---

## How to reproduce

```bash
pip install numpy scikit-learn scipy matplotlib

# From repo root:
python scripts/append_week12.py
python scripts/make_cluster_gallery.py
```

Open [`notebooks/BBO_Capstone_Optimized.ipynb`](notebooks/BBO_Capstone_Optimized.ipynb).

---

## Method (short)

1. Fit a per-function GP on `data/function_*/`.  
2. Score candidates with EI or UCB (trust-region radius by phase).  
3. Apply constraints (F3 x₃ lock, F5 high face, F1 trust gate).  
4. Submit one `0.xxxxxx-...` string per function; append `y`; repeat.

Details: [`docs/TECHNICAL_JUSTIFICATION.md`](docs/TECHNICAL_JUSTIFICATION.md).
