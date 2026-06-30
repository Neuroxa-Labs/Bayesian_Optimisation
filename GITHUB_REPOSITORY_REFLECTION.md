# GitHub Repository Reflection — BBO Capstone

*Forum post for Module 16 repository organisation activity.*

---

## Introduction

After five rounds of queries, I reorganised how I present this project on GitHub. The goal is not only working code, but a repository that an employer or collaborator can navigate, reproduce, and understand without guessing why each design choice was made.

---

## 1. Repository structure

**How it is organised today**

| Area | Location | Purpose |
|------|----------|---------|
| **Main pipeline** | `BBO_Capstone_Optimized.ipynb` | GP fitting, acquisition, weekly analysis |
| **Per-function data** | `function_1/` … `function_8/` | `initial_inputs.npy`, `initial_outputs.npy`, `EXPLANATION_F*.md`, `analysis_F*.png` |
| **Weekly strategy & reflection** | `WEEK*_STRATEGY.md`, `WEEK*_REFLECTION.md`, `WEEK*_DISCUSSION.md` | Decisions, portal queries, forum posts |
| **Query utilities** | `run_week.py`, `generate_week*.py`, `append_week*.py` | Reproduce and append portal results |
| **Report generators** | `make_*.py` | Dashboard PNG/HTML, progress charts |
| **Main dashboard** | `bbo_progress_report.html`, `.png`, `.jpg` | Single entry point for progress |

**Changes I made for clarity and reproducibility**

1. **Documented the weekly loop** in the README: append results → regenerate reports → generate next queries → submit.
2. **Separated concerns:** notebooks for exploration, scripts for repeatable report/query generation, markdown for reasoning.
3. **One folder per function** so data, analysis figures, and written explanations stay together.
4. **Ignored local cache files** (`*.pkl`) via `.gitignore` — query pickles stay local; approved queries live in `WEEK*_STRATEGY.md`.
5. **Linked all weekly docs** from the README so navigation does not depend on file search.

I considered a heavier `src/` package layout but kept a flatter structure appropriate for a weekly capstone: fewer import paths, easier for markers to open one notebook and one HTML report.

---

## 2. Coding libraries and packages

**Central stack**

| Library | Role |
|---------|------|
| **scikit-learn** | `GaussianProcessRegressor`, Matérn / White kernels — core surrogate |
| **scipy** | `differential_evolution` for acquisition optimisation |
| **numpy** | Data storage (`.npy`), vector operations |
| **matplotlib** | GP surfaces, acquisition plots, progress dashboards |

**Not used as surrogates (by design)**

- **PyTorch / TensorFlow:** discussed in Module 16 reflections; not used for portal queries because 14–44 points per function is too sparse for reliable NN training and uncertainty estimation.
- **SVM:** kernel-method parallel only; no calibrated σ for EI/UCB without extra machinery.

**Trade-offs considered**

- **GP vs NN:** GP gives μ and σ natively for acquisition; NN would need ensembles or dropout for uncertainty — high overfitting risk at this budget.
- **Single GP vs ensemble:** simpler, faster, easier to debug weekly; per-function ν, α, and log-y (F5) provide most of the flexibility I need.
- **Notebook vs scripts:** notebook for the full pipeline; scripts for one-command regeneration before submission.

This stack matches the problem: low-data, expensive queries, need for uncertainty-aware decisions — the same reason production BO systems often stay GP-based until data volume justifies deep surrogates.

---

## 3. Documentation

**What the README already describes**

- Project purpose, inputs (`x ∈ [0,1]ᵈ`), outputs (scalar `y`), and objective (maximise under query budget).
- Real-world meaning of F1–F8 and per-function acquisition choices.
- Stage 2 connection to course modules (kernels, regression, SVM parallel).
- Preprocessing table (`normalize_y`, log-y on F5, WhiteKernel on F2).

**Updates aligned with recent strategy and results**

1. **Repository layout tree** and weekly workflow commands.
2. **Week 5** strategy, discussion, and approved portal queries.
3. **Progress through Week 4** with links to reflection files (F5 3744, F7 1.857, etc.).
4. **`GITHUB_REPOSITORY_REFLECTION.md`** (this file) documenting structure and library choices for the Module 16 activity.

**Other documents**

- `EXPLANATION_F*.md` — per-function deep dives for learners.
- `bbo_progress_report.html` — interactive dashboard linking to all of the above.

Documentation now follows the same layered logic as the optimiser: README = overview, weekly markdown = iteration log, function folders = detail, HTML = visual summary.

---

## Conclusion

The repository is structured for **reproducibility** (scripts + `.npy` data), **transparency** (weekly strategy/reflection markdown), and **quick assessment** (HTML dashboard + main PNG). PyTorch-style flexibility lives in weekly overrides; production-style structure lives in the fixed pipeline and report generators. That balance is intentional for a capstone judged on both results and reasoning.
