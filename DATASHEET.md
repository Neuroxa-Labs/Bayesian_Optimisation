# Datasheet — BBO Capstone Query History

*Documentation for the black-box optimisation dataset (query inputs and function evaluations) used in the Imperial PCMLAI BBO capstone. Follows the Mini-lesson 21.1 datasheet framework.*

---

## 1. Motivation

**Purpose.** I created this dataset to support Stage 2 of the Bayesian Black-Box Optimisation (BBO) capstone: iteratively maximising eight unknown continuous functions under a strict evaluation budget (one query per function per week).

**Task supported.** Continuous global optimisation in the unit hypercube \([0,1]^d\) (\(d \in \{2,\ldots,8\}\)). Each record is an expensive black-box evaluation \((x, y)\) used to fit surrogates and choose the next query.

**Gap filled.** The true functions are hidden by the course portal. Without a growing, well-documented evaluation history, the optimisation loop cannot be audited, reproduced, or improved week to week.

**Creator / funding.** Created and maintained by me as a student researcher on the PCMLAI programme. No external commercial funding; evaluations are provided by the course capstone portal.

---

## 2. Composition

**Contents.** For each of eight functions (F1–F8):

| Field | Description |
|-------|-------------|
| `x` | Continuous input vector in \([0,1]^d\) (2D–8D depending on function) |
| `y` | Scalar objective value returned by the portal (higher is better) |

**Real-world labels (course framing).** F1 radiation detection; F2 noisy ML log-likelihood; F3 drug side-effects; F4 warehouse placement; F5 chemical yield; F6 cake recipe; F7 6-D hyperparameter tuning; F8 8-D ML model score.

**Size (after Week 9 / ~10 portal rounds + initial seed data).** Approximately:

| Function | Dim | Approx. observations | Notes |
|----------|-----|----------------------|--------|
| F1 | 2 | ~19 | Mostly near-zero outputs |
| F2 | 2 | ~19 | Noisy; best ≈ 0.777 |
| F3 | 3 | ~24 | Sensitive \(x_3\) |
| F4 | 4 | ~40 | Strong recent gains |
| F5 | 4 | ~30 | High-face ridge |
| F6 | 5 | ~30 | Interior basin |
| F7 | 6 | ~40 | Sharp local peak |
| F8 | 8 | ~50 | Slow late gains |

Exact counts live in `data/function_*/initial_inputs.npy` and `initial_outputs.npy` (plus weekly append scripts / strategy logs for portal rounds not yet merged into `.npy`).

**Format.** NumPy `.npy` arrays; weekly portal strings in `weeks/WEEK*_STRATEGY.md` (`0.xxxxxx-...` to six decimal places); narrative in `data/function_*/EXPLANATION_F*.md` and `weeks/` reflections.

**Completeness / gaps.** No missing labels for submitted queries. **Spatial gaps** remain large: sampling is clustered near incumbents (especially F5 high face, F3 safe \(x_3\) band, F4/F6/F7/F8 basins). F1 is sparse with almost no usable signal. Higher-D boxes (F7/F8) are under-sampled relative to volume.

**Splits.** Not a supervised train/test product. Chronological rounds act as the natural sequence; leave-one-out style checks are used only as internal GP diagnostics when needed.

**Privacy.** No personal data. Synthetic course black-box outputs only.

---

## 3. Collection process

**Method.** Each week I propose one \(x\) per function via the capstone portal and receive one \(y\). Points are chosen by a Gaussian Process + acquisition pipeline (`notebooks/BBO_Capstone_Optimized.ipynb`), with per-function constraints and occasional manual overrides documented in `weeks/WEEK*_STRATEGY.md`.

**Sampling strategy.** Sequential, adaptive, **not** i.i.d. random. Early rounds more exploratory; later rounds increasingly trust-region exploitation around incumbents. F1 uses a trust gate (explore / narrow exploit when space-fill fails).

**Time frame.** Stage 2 weekly cycles across the module calendar (initial seed data from the course plus roughly ten query rounds through Week 9/10).

**Ethics.** Course-sanctioned academic use only; no human subjects; no IRB required.

---

## 4. Preprocessing and uses

**Transformations.**

- Inputs already in \([0,1]^d\) (portal scale).
- **F5:** \(\log(y)\) (or log10) when fitting the GP because yields span large magnitudes.
- **F2:** WhiteKernel / noise modelling; treat \(y\) as potentially stochastic.
- No deletion of observed points; failures stay in the history.

Raw portal \((x,y)\) pairs are preserved in strategy/reflection files and `.npy` stores.

**Intended uses.**

- Fitting and auditing Bayesian optimisation surrogates.
- Reproducing weekly query decisions.
- Teaching/demo of BO under tight budgets.

**Inappropriate uses.**

- Treating the dataset as a complete map of each function.
- Deploying learned surrogates as safety-critical controllers without new real-world calibration.
- Claiming demographic fairness properties (not applicable; no people in the data).

---

## 5. Distribution

**Availability.** Public GitHub repository for this capstone (linked from the course discussion board). Primary paths: `data/function_*/`, `weeks/WEEK*_STRATEGY.md`, `weeks/WEEK*_REFLECTION.md`, dashboard `reports/progress/bbo_progress_report.html`.

**License / terms.** Academic sharing for peer review and programme assessment. Redistribute with attribution; do not present portal outputs as proprietary production data.

**Fees.** None.

---

## 6. Maintenance

**Maintainer.** Me (repository owner).

**Updates.** After each portal round: append results, refresh strategy/reflection notes, regenerate reports when needed (`make_*.py`).

**Versioning.** Git history is the version control. Weekly markdown files act as round-level changelogs.

**Long-term storage.** GitHub remote; local clones for development.
