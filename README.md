# Black-Box Bayesian Optimisation — Capstone

Imperial PCMLAI Stage 2: maximise **eight unknown black-box functions** (2D–8D) with **one query per function per week**.

| | |
|--|--|
| **Surrogate** | Gaussian Process (Matérn + ARD; WhiteKernel on F2; log-y on F5) |
| **Acquisition** | EI / UCB + trust-region exploit; trust gate when signal is absent (F1) |
| **Status** | **Week 10 done (5/8 improved)** · **Week 11 ready** (clustering lens) |

---

## Start here

| Resource | Link |
|----------|------|
| **Datasheet** (Module 21) | [`DATASHEET.md`](DATASHEET.md) |
| **Model card** (Module 21) | [`MODEL_CARD.md`](MODEL_CARD.md) |
| **Cluster & progress gallery** | [`reports/analysis/cluster_gallery.html`](reports/analysis/cluster_gallery.html) |
| **Interactive dashboard** | [`reports/progress/bbo_progress_report.html`](reports/progress/bbo_progress_report.html) |
| **23.2 presentation draft** | [`docs/BBO_PRESENTATION_23_2.md`](docs/BBO_PRESENTATION_23_2.md) |
| **Main pipeline** | [`notebooks/BBO_Capstone_Optimized.ipynb`](notebooks/BBO_Capstone_Optimized.ipynb) |
| **Week 10 reflection** | [`weeks/WEEK10_REFLECTION.md`](weeks/WEEK10_REFLECTION.md) |
| **Week 11 portal queries** | [`weeks/WEEK11_STRATEGY.md`](weeks/WEEK11_STRATEGY.md) |
| **Week 11 discussion** | [`weeks/WEEK11_DISCUSSION.md`](weeks/WEEK11_DISCUSSION.md) |

---

## Repository layout

```text
Bayesian_Optimisation/
├── README.md                 # This file
├── DATASHEET.md              # Dataset documentation (stable Module 21 URL)
├── MODEL_CARD.md             # Optimisation approach card (stable Module 21 URL)
├── docs/                     # Extra write-ups + 23.2 presentation draft
├── weeks/                    # All weekly strategy / reflection / discussion notes
├── reports/
│   ├── progress/             # Dashboard HTML + progress charts
│   └── analysis/             # Cluster gallery + per-function PNGs
├── notebooks/                # GP + acquisition pipeline
├── scripts/                  # append / generate / make_* utilities
└── data/
    └── function_1/ … function_8/   # .npy history, EXPLANATION_*, analysis_F*.png
```

### Visual analysis (Week 10 data)

KMeans hulls on ARD-selected axes + best-so-far trends (same idea as the Module 23 clustering / PCA discussion lens):

| Figure | File |
|--------|------|
| 3D cluster gallery (F1–F8) | [`cluster_gallery_3d.png`](reports/analysis/cluster_gallery_3d.png) |
| Best-so-far progress | [`progress_best_so_far.png`](reports/analysis/progress_best_so_far.png) |
| Hull + progress pairs (F3/F5/F7) | [`cluster_progress_pairs.png`](reports/analysis/cluster_progress_pairs.png) |
| HTML viewer | [`cluster_gallery.html`](reports/analysis/cluster_gallery.html) |

Regenerate: `python scripts/make_cluster_gallery.py`

---

## Best so far (after Week 10)

| Fn | Task | Dim | Best y (approx.) | Note |
|----|------|-----|------------------|------|
| F1 | Radiation | 2 | ~0 | Signal cluster ~0.64/0.68 (W10) |
| F2 | Noisy ML | 2 | **0.777** | W10 recovered to 0.72 |
| F3 | Drug side-effects | 3 | **−0.011** | Safe x₃ band |
| F4 | Warehouse | 4 | **0.667** | W10 |
| F5 | Chemical yield | 4 | **3779** | Ridge x₁→0.42 |
| F6 | Cake recipe | 5 | **−0.136** | W10 jump |
| F7 | HP tuning 6D | 6 | **1.863** | W10 |
| F8 | 8-param ML | 8 | **9.871** | W10 |

**Week 8:** 3/8 · **Week 9:** 4/8 · **Week 10:** **5/8** (F4–F8).

---

## Weekly notes

All live under [`weeks/`](weeks/):

- `WEEK*_STRATEGY.md` — portal queries + rationale  
- `WEEK*_REFLECTION.md` — post-result analysis  
- `WEEK*_DISCUSSION.md` — forum posts  

Latest: [`WEEK11_STRATEGY.md`](weeks/WEEK11_STRATEGY.md) · [`WEEK11_DISCUSSION.md`](weeks/WEEK11_DISCUSSION.md)

---

## How to reproduce

```bash
pip install numpy scikit-learn scipy matplotlib

# From repo root:
python scripts/append_weeks_8_10.py   # sync W8–W10 into data/ (idempotent)
python scripts/make_cluster_gallery.py
python scripts/make_progress_chart.py
python scripts/make_function_analysis.py
```

Open `notebooks/BBO_Capstone_Optimized.ipynb` (expects `data/` beside `notebooks/`).

---

## Method (short)

1. Fit a per-function GP on `data/function_*/`.  
2. Score candidates with EI or UCB (κ/ξ and trust-region radius tuned by phase).  
3. Apply constraints (F3 x₃ lock, F5 high face, boundary penalties).  
4. Submit one `0.xxxxxx-...` string per function; append `y`; repeat.

Literature / tooling: [`docs/TECHNICAL_JUSTIFICATION.md`](docs/TECHNICAL_JUSTIFICATION.md).
