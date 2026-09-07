# Black-Box Bayesian Optimisation — Capstone

Imperial PCMLAI Stage 2 final deliverable: maximise **eight unknown black-box functions** (2D–8D) with **one query per function per week**.

| | |
|--|--|
| **Surrogate** | Gaussian Process (Matérn + ARD; WhiteKernel on F2; log-y on F5) |
| **Acquisition** | EI / UCB + trust-region exploit; trust gate when signal is absent (F1) |
| **Status** | **Week 12 complete** · Final repository submission ready |
| **Public repo** | https://github.com/Neuroxa-Labs/Bayesian_Optimisation |

---

## For a general audience (~100 words)

We ran a careful series of experiments on eight hidden scoring problems (from finding a radiation source to tuning ML models and chemical recipes). Each week we could try only one setting per problem, so guessing at random would waste the budget. Instead we used past results to decide the next try: focus where scores were already improving, change course quickly when a region looked dead, and keep steps small near the best known settings. Over the project this raised several of the scores steadily — especially chemical yield and the warehouse / hyperparameter tasks — and left a clear public record of what we tried and why.

---

## Start here

| Resource | Link |
|----------|------|
| **Datasheet** (Module 21) | [`DATASHEET.md`](DATASHEET.md) |
| **Model card** (Module 21) | [`MODEL_CARD.md`](MODEL_CARD.md) |
| **Main pipeline (Jupyter)** | [`notebooks/BBO_Capstone_Optimized.ipynb`](notebooks/BBO_Capstone_Optimized.ipynb) |
| **23.2 presentation text** | [`docs/BBO_PRESENTATION_23_2.md`](docs/BBO_PRESENTATION_23_2.md) |
| **Final project reflection** | [`weeks/FINAL_CAPSTONE_REFLECTION.md`](weeks/FINAL_CAPSTONE_REFLECTION.md) |
| **Successful strategies discussion** | [`weeks/SUCCESSFUL_STRATEGIES_DISCUSSION.md`](weeks/SUCCESSFUL_STRATEGIES_DISCUSSION.md) |
| **Module 24 RL discussion** | [`weeks/MODULE24_DISCUSSION.md`](weeks/MODULE24_DISCUSSION.md) |
| **Week 12 reflection** | [`weeks/WEEK12_REFLECTION.md`](weeks/WEEK12_REFLECTION.md) |
| **Cluster & progress gallery** | [`reports/analysis/cluster_gallery.html`](reports/analysis/cluster_gallery.html) |
| **Interactive dashboard** | [`reports/progress/bbo_progress_report.html`](reports/progress/bbo_progress_report.html) |

---

## Repository layout

```text
Bayesian_Optimisation/
├── README.md                 # This file (incl. non-technical summary)
├── DATASHEET.md              # Dataset documentation (Module 21)
├── MODEL_CARD.md             # Optimisation approach card (Module 21)
├── docs/                     # Technical notes + 23.2 presentation draft
├── weeks/                    # Strategy / reflection / discussion posts
├── reports/
│   ├── progress/             # Dashboard HTML + progress charts
│   └── analysis/             # Cluster gallery + analysis PNGs
├── notebooks/                # GP + acquisition pipeline (Jupyter)
├── scripts/                  # append / generate / make_* utilities
└── data/
    └── function_1/ … function_8/   # .npy history, EXPLANATION_*, analysis_F*.png
```

**Data note.** Evaluation histories are small NumPy arrays in `data/function_*/` (course portal outputs). There is no large external dataset to host off-GitHub; counts and framing are documented in [`DATASHEET.md`](DATASHEET.md).

### Visual analysis

| Figure | File |
|--------|------|
| 3D cluster gallery (F1–F8) | [`cluster_gallery_3d.png`](reports/analysis/cluster_gallery_3d.png) |
| Best-so-far progress | [`progress_best_so_far.png`](reports/analysis/progress_best_so_far.png) |
| Hull + progress pairs (F3/F5/F7) | [`cluster_progress_pairs.png`](reports/analysis/cluster_progress_pairs.png) |
| HTML viewer | [`cluster_gallery.html`](reports/analysis/cluster_gallery.html) |

Regenerate: `python scripts/make_cluster_gallery.py`

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

All live under [`weeks/`](weeks/):

- `WEEK*_STRATEGY.md` — portal queries + rationale  
- `WEEK*_REFLECTION.md` — post-result analysis  
- `WEEK*_DISCUSSION.md` / `MODULE24_*` / `FINAL_*` / `SUCCESSFUL_*` — forum posts  

Latest results: [`WEEK12_REFLECTION.md`](weeks/WEEK12_REFLECTION.md)

---

## How to reproduce

```bash
pip install numpy scikit-learn scipy matplotlib

# From repo root:
python scripts/append_week12.py          # ensure W12 in data/ (idempotent)
python scripts/make_cluster_gallery.py
python scripts/make_progress_chart.py
```

Open [`notebooks/BBO_Capstone_Optimized.ipynb`](notebooks/BBO_Capstone_Optimized.ipynb) (expects `data/` at repo root).

---

## Method (short)

1. Fit a per-function GP on `data/function_*/`.  
2. Score candidates with EI or UCB (κ/ξ and trust-region radius tuned by phase).  
3. Apply constraints (F3 x₃ lock, F5 high face, boundary penalties, F1 trust gate).  
4. Submit one `0.xxxxxx-...` string per function; append `y`; repeat.

Literature / tooling: [`docs/TECHNICAL_JUSTIFICATION.md`](docs/TECHNICAL_JUSTIFICATION.md).
