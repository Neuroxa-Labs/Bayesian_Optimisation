# Technical Justification — Prior Work & Tooling

*Discussion-board write-up: grounding the BBO strategy in literature and libraries (<700 words).*

---

My current BBO approach is deliberate: a **Gaussian Process (GP)** surrogate plus **Expected Improvement (EI)** or **Upper Confidence Bound (UCB)** acquisition, with light per-function engineering (Matérn ν, WhiteKernel on F2, log-y on F5, boundary penalties, occasional locks such as F3’s x₃). With one expensive query per function per week and only tens of points, I need a model that (1) fits small data and (2) returns uncertainty so I can decide where to sample next. That combination is the classical Bayesian optimisation loop, not an ad-hoc neural net.

**Main technical justification.** The core idea is well established: place a GP prior over the unknown function, update it with observed `(x, y)`, then maximise an acquisition function that balances predicted mean and uncertainty (Shahriari et al., 2016). I chose this over a neural surrogate because calibrated predictive variance is built into the GP. EI and UCB are the operational “loss → next query” maps; without σ(x), those acquisitions are not well defined. Prior research on expensive black-box optimisation therefore supports keeping the GP as the workhorse and treating deep learning as a source of *strategy analogies* (feature hierarchy, explore/exploit), not as the weekly model.

**Academic papers and ideas that guide the design.**

- **Rasmussen & Williams (2006), *Gaussian Processes for Machine Learning*** — kernels, length scales, and predictive equations. My per-dimension length-scale diagnostics and Matérn choices come directly from this framing.
- **Jones, Schonlau & Welch (1998)** — Efficient Global Optimisation / Expected Improvement. EI is my default when I want improvement relative to the current best (F2, F5, F6, F7).
- **Srinivas et al. (2010), GP-UCB** — regret-aware exploration via μ + κσ. UCB with tunable κ supports multimodal or high-dimensional cases (F4, F8) and early exploration.
- **Shahriari et al. (2016)** survey — “taking the human out of the loop”: reinforces the loop I actually run (fit → acquire → evaluate → append) and the need to document acquisition choices.
- **Snoek, Larochelle & Adams (2012)** — practical BO for ML hyperparameters: motivates treating F7/F8 as noisy ML-score landscapes and using noise-aware kernels where needed.

These references strengthen the project by showing that weekly overrides (locks, log transforms, coverage on F1 when signal is absent) sit *on top of* a standard foundation rather than replacing it.

**Libraries and why not the alternatives.** The stack is **NumPy** (data), **scikit-learn** (`GaussianProcessRegressor`, Matérn, WhiteKernel), **SciPy** (acquisition optimisation), and **Matplotlib** (diagnostics). scikit-learn was the right GP choice for this course scale: stable, readable, and enough for eight weekly fits. I considered **GPyTorch / BoTorch** (more modern BO stacks) and **PyTorch / TensorFlow** NN surrogates. Those are excellent at larger scale, but with ~15–50 points they add complexity and overfitting risk without a clear gain in acquisition quality. An **SVM** shares the kernel idea but does not give calibrated σ for EI/UCB. So sklearn GP stays central; PyTorch appears only in reflections.

**How I document this on GitHub.** Justifications live where reviewers look first:

1. **`README.md`** — pipeline, per-function AF table, preprocessing, and why GP not NN/SVM.
2. **`WEEK*_STRATEGY.md` / `WEEK*_REFLECTION.md`** — weekly decisions tied to results.
3. **`GITHUB_REPOSITORY_REFLECTION.md`** — structure and library trade-offs.
4. **This file** — explicit literature and tooling rationale.
5. Per-function **`EXPLANATION_F*.md`** and analysis figures — local evidence for each black box.

The aim is that a peer, facilitator, or employer can open the repo and see *what* I did and *why*, not only the latest portal string.

**Looking ahead.** To refine further I would consult: **BoTorch / Ax** docs and examples for acquisition variants; **Frazier (2018)** BO tutorial for cleaner theory–practice links; sparse/peak and constrained BO papers if F1 remains signal-free; and simple **baselines** (random, Sobol) as sanity checks against GP proposals. If data grow late in the schedule, I would revisit a hybrid (GP locally, broader screening elsewhere) rather than swapping the whole stack overnight.

In short: the literature justifies GP + EI/UCB for expensive small-data optimisation; sklearn makes that reproducible; the GitHub docs make the reasoning auditable.
