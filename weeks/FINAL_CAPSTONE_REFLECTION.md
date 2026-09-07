# Final Capstone Reflection — BBO Project

*Discussion-board post after the optimisation phase. First person. Under 2000 words. Answers all five prompts.*

**Repository:** https://github.com/Neuroxa-Labs/Bayesian_Optimisation

---

**Initial codebase**

I did not start from a full off-the-shelf Bayesian optimisation package such as BoTorch or Optuna. I built the pipeline myself in Python around **scikit-learn’s** `GaussianProcessRegressor`, with **NumPy** for the `.npy` histories, **SciPy** for acquisition maximisation (for example differential evolution over candidate points), and **Matplotlib** for diagnostics and progress charts. The living centre of the work is `notebooks/BBO_Capstone_Optimized.ipynb`, supported by small scripts (`append_week*.py`, `run_week.py`, `make_*.py`) and per-function folders under `data/function_*/`.

I chose this stack for three reasons. First, with only one evaluation per function per week, a Gaussian Process with a Matérn kernel and ARD is a standard, honest surrogate — calibrated uncertainty matters more than a flashy neural net on ~20 points. Second, scikit-learn kept the code readable for markers and for my own weekly audits; I could see length scales, noise terms, and acquisition scores directly. Third, starting light let me add per-function policy on top (WhiteKernel on F2, log-y on F5, trust regions, locks) without fighting a heavy framework’s defaults. The public repository above documents that choice in the README, model card, and datasheet.

**Code modification — week by week**

The biggest changes were not random refactors; they were responses to portal feedback.

Early weeks: a relatively uniform GP + EI/UCB loop across functions, with more exploration and occasional high-uncertainty queries. That taught scale and sign but produced boundary artefacts and wasted steps. I then introduced **per-function configs** (kernel smoothness, acquisition type, exploration parameter) and stopped treating F1–F8 as identical.

Mid project: **trust regions** around incumbents, **boundary penalties**, and hard locks (F3’s safe x₃ band; F5’s high x₂–x₄ face). F5 gained a **log transform** because raw yields were huge; F2 gained a **WhiteKernel** because the ridge was noisy. I also stopped exact incumbent replays after learning they wasted a week of budget.

Late project (Weeks 8–12): the code and the human policy both compressed toward **local exploit**. F5 became an explicit ridge climb on x₁; F1 gained a **trust gate** that refused GP exploit while every label was ~0, then switched to the (0.64, 0.68) signal lobe once a non-null reading appeared. Repository hygiene matured in parallel: weekly `WEEK*_STRATEGY.md` / `REFLECTION.md` / `DISCUSSION.md`, Module 21 datasheet and model card, an HTML dashboard, and a cluster/progress gallery driven by ARD-selected axes. The most significant engineering change was treating the notebook as a proposer and the weekly markdown + human audit as the decision layer — the model suggests; I lock the portal string.

Those modifications show up in the scoreboard. Local trust-region exploit produced repeated bests on F4, F5, F7 and F8 from Week 8 onward. Leaving a sharp basin without evidence (F2’s 0.777 needle; F6’s −0.136 centroid in Week 11) hurt immediately — and the code response was smaller steps and hard-return logic, not a bigger model.

**Final result — last weeks and what I would change**

In the final stretch the score evolved unevenly but in a clear pattern. **Week 10** was the strongest single round (**5/8** new bests), including a large F6 jump to −0.136 and F1’s first measurable lobe reading. **Weeks 11 and 12** each delivered **4/8** again on F4, F5, F7 and F8: F5’s ridge climbed through x₁=0.43 then 0.44 to ≈**3801**; F4 reached **0.679**; F7 **1.872**; F8 **9.873**. F6 partially recovered in Week 12 (−0.372 → −0.205) but the Week 10 incumbent still stands. F2 never stably reclaimed 0.777 despite queries near [0.718, 0.02]. F1’s signal lobe is validated three times, yet under pure maximisation those readings remain below the near-zero historical max.

If I started over — or had more time — I would (1) instrument ARD length scales and incumbent distance as first-class weekly diagnostics from Week 1, (2) keep a stricter “no leave basin without evidence” rule earlier on F2/F6, (3) treat F1 as a detection problem (find any non-null cluster) before maximisation, and (4) automate idempotent append scripts sooner so the `.npy` history never lagged the forum notes. I would still keep GPs rather than switch to a deep surrogate at this sample size.

**Trade-offs and decisions**

The central trade-off was **exploration versus exploitation** under a one-query-per-week budget — classic multi-armed-bandit tension. Early exploration bought map coverage; late exploitation bought the compounding gains on F4–F8. A second trade-off was **short-term greed versus long-term structure**: chasing global acquisition sometimes looked clever for one week and destroyed a known peak the next. A third was **automation versus human veto**: full auto-BO would have been faster to run, but the trust gate on F1 and the hard-return on F6 only happened because I overrode a confident-looking posterior. I balanced these by phase (explore early, exploit late), by evidence (ARD-sensitive axes only), and by failure response (shrink, return, do not invent a new mode).

**Learning and application**

The most important lesson is that **sample-efficient sequential decisions beat clever models when evaluations are scarce**. A simple GP plus honest uncertainty, plus discipline about which dimensions move, outperformed the temptation to overfit with flashy architectures. I will take that into future ML work — hyperparameter tuning, A/B tests, experimental design — wherever each trial is expensive. I will also keep the habit of writing decisions down (strategy / reflection) so the next query is auditable.

What surprised me most was how **sharp** some landscapes were: millimetre-scale misses on F2 erased large apparent gains, and a “nearby” F6 step collapsed a hard-won best. Peer strategies also surprised me — some leaned on PCA/clustering narratives or heavier ML stacks; the useful overlap was the shared idea of compressing search onto a few active directions, which matched my ARD/trust-region practice even when the tooling differed.

Overall, this capstone taught me to treat optimisation as a closed loop of propose → observe → update policy, not as a one-shot fit. That mindset, more than any single hyperparameter, is what I will carry forward.
