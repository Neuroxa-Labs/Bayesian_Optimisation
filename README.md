# Black-Box Bayesian Optimisation — Capstone

Imperial PCMLAI Stage 2: maximise **eight unknown black-box functions** (2D–8D) with **one query per function per week**.

| | |
|--|--|
| **Surrogate** | Gaussian Process (Matérn + ARD; WhiteKernel on F2; log-y on F5) |
| **Acquisition** | EI / UCB + trust-region exploit; trust gate when signal is absent (F1) |
| **Status** | Through **Week 9** results; **Week 10** queries ready |

---

## Start here

| Resource | Link |
|----------|------|
| **Datasheet** (Module 21) | [`DATASHEET.md`](DATASHEET.md) |
| **Model card** (Module 21) | [`MODEL_CARD.md`](MODEL_CARD.md) |
| **Interactive dashboard** | [`reports/progress/bbo_progress_report.html`](reports/progress/bbo_progress_report.html) |
| **Main pipeline** | [`notebooks/BBO_Capstone_Optimized.ipynb`](notebooks/BBO_Capstone_Optimized.ipynb) |
| **Week 10 portal queries** | [`weeks/WEEK10_STRATEGY.md`](weeks/WEEK10_STRATEGY.md) |
| **Week 10 discussion** | [`weeks/WEEK10_DISCUSSION.md`](weeks/WEEK10_DISCUSSION.md) |

---

## Repository layout

```text
Bayesian_Optimisation/
├── README.md                 # This file
├── DATASHEET.md              # Dataset documentation (stable Module 21 URL)
├── MODEL_CARD.md             # Optimisation approach card (stable Module 21 URL)
├── docs/                     # Extra write-ups
│   ├── TECHNICAL_JUSTIFICATION.md
│   └── GITHUB_REPOSITORY_REFLECTION.md
├── weeks/                    # All weekly strategy / reflection / discussion notes
├── reports/
│   ├── progress/             # Dashboard HTML + progress charts
│   └── analysis/             # Weekly per-function analysis PNGs
├── notebooks/                # GP + acquisition pipeline
├── scripts/                  # append / generate / make_* utilities
└── data/
    └── function_1/ … function_8/   # .npy history, EXPLANATION_*, analysis_F*.png
```

---

## Best so far (after Week 9)

| Fn | Task | Dim | Best y (approx.) | Note |
|----|------|-----|------------------|------|
| F1 | Radiation | 2 | ~0 | Local peak hunt (W10 → peer basin ~0.64/0.68) |
| F2 | Noisy ML | 2 | **0.777** | Noise-sensitive ridge |
| F3 | Drug side-effects | 3 | **−0.011** | Safe x₃ band |
| F4 | Warehouse | 4 | **0.642** | Strong W8–W9 gains |
| F5 | Chemical yield | 4 | **3769** | Ridge x₁ 0.38→0.41 |
| F6 | Cake recipe | 5 | **−0.240** | Step-size sensitive |
| F7 | HP tuning 6D | 6 | **1.858** | Local peak |
| F8 | 8-param ML | 8 | **9.869** | Slow late gains |

**Week 8:** 3/8 improved (F4, F5, F8). **Week 9:** 4/8 improved (F4, F5, F7, F8).

---

## Weekly notes

All live under [`weeks/`](weeks/):

- `WEEK*_STRATEGY.md` — portal queries + rationale  
- `WEEK*_REFLECTION.md` — post-result analysis  
- `WEEK*_DISCUSSION.md` — forum posts (Modules 16–21 themes)  

Latest: [`WEEK10_STRATEGY.md`](weeks/WEEK10_STRATEGY.md) · [`WEEK10_DISCUSSION.md`](weeks/WEEK10_DISCUSSION.md)

---

## How to reproduce

```bash
pip install numpy scikit-learn scipy matplotlib

# From repo root:
python scripts/run_week.py 10
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
