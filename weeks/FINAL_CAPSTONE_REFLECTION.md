# Final BBO Capstone Reflection

*Discussion-board post. First person. Under 2000 words. Structured like a full end-of-project reflection; content is our actual GP + trust-region pipeline (not peer ensembles/NN).*

**Repository:** https://github.com/Neuroxa-Labs/Bayesian_Optimisation

---

**Initial codebase**

I began with a relatively simple Gaussian Process (GP)-based Bayesian optimisation implementation. I built the initial codebase myself from the module concepts and scikit-learn’s `GaussianProcessRegressor`, rather than forking a full BoTorch/Optuna project. Developing the loop myself was the best way to understand how the surrogate, acquisition function and weekly budget fit together.

I chose this starting point because GPs are well suited to black-box optimisation when evaluations are expensive and only a limited number of observations are available. They provide both a predicted mean and an estimate of uncertainty, which makes it possible to balance exploitation of promising regions with exploration of uncertain areas — exactly the constraint of one query per function per week.

The first version was intentionally simple. It loaded the per-function `.npy` histories, fitted a Matérn GP (with ARD), scored candidates with EI or UCB, and emitted a portal-formatted query string. That baseline lived in a notebook that later became `notebooks/BBO_Capstone_Optimized.ipynb`, with small helper scripts for appending results and regenerating reports. My code is publicly available here:

https://github.com/Neuroxa-Labs/Bayesian_Optimisation

**Code modifications**

The implementation developed considerably over the course of the project. Each block of weeks added functionality in response to limitations identified in the previous iteration — but I stayed with a GP core rather than stacking many surrogates.

**Weeks 1–3.** I established a working BO pipeline: one GP per function, EI/UCB acquisition, and broad exploration while the maps were empty. This taught scale and sign for each y, but also produced boundary artefacts and occasional over-confident jumps into empty space. I began separating **per-function configs** (kernel smoothness ν, acquisition type, exploration parameter) instead of treating F1–F8 as identical.

**Weeks 4–6.** I introduced **trust regions** around incumbents, soft **boundary penalties**, and the first hard locks (notably F3’s safe x₃ band). Reporting improved: progress charts, per-function analysis figures, and written `EXPLANATION_F*.md` notes so each decision was auditable. Exact incumbent replays were banned after they wasted budget without new information.

**Weeks 7–8.** Policy became more specialised. F5 received a **log-y** transform because raw chemical yields dominated the fit; F2 received a **WhiteKernel** noise term on a sharp ridge. F5’s search locked onto the high x₂–x₄ face and began an explicit **x₁ ridge climb**. Week 8 delivered the first clear mid-project streak (new bests on F4, F5, F8), which validated tight local exploit over global acquisition.

**Weeks 9–10.** I compressed steps further and treated ARD length scales as a PCA-style guide to which dimensions deserve movement. Week 10 was the strongest single round (**5/8** improved), including a large F6 jump to −0.136 and F1’s first measurable reading in the peer-supported (0.64, 0.68) lobe after months of near-zero returns near (0.73, 0.73). F1 also gained an explicit **trust gate**: refuse GP exploitation while every label is ~0; only exploit after a real signal cluster appears.

**Weeks 11–12.** Clustering / PCA discussion lenses matched what the code already did — stay inside proven basins; move only sensitive axes. Week 11 improved F4/F5/F7/F8 again but **collapsed F6** (−0.136 → −0.372) after a small step off the Week 10 centroid; the code/policy response was a hard-return rule. Week 12 continued the F5 ridge (x₁=0.44 → ≈3801), micro-gains on F4/F7/F8, and a partial F6 recovery (−0.205), while F2 again missed the 0.777 needle. Repository work matured in parallel: Module 21 datasheet/model card, HTML dashboard, and an ARD-axis cluster gallery.

The changes with the greatest practical impact were **per-function GP policies**, **trust regions + locks**, **F1’s trust gate**, **F5’s ridge discipline**, **noise/log handling on F2/F5**, and the late-project rule **never leave a validated basin without evidence**. Diagnostics and weekly markdown (strategy / reflection / discussion) mattered almost as much as the optimiser, because they forced an evidence-based portal string instead of “whatever acquisition ranked first.”

**Final result**

The final weeks produced more consistent and targeted queries than the early rounds because the strategy shifted from predominantly exploratory behaviour toward greater exploitation. Initially many queries were exploratory because there was little information about each landscape. As the dataset grew past ~20 points per function, I concentrated on regions associated with high observed values, using EI/UCB mainly to rank **tiny offsets inside a trust region** rather than to invent new modes across the box.

Score evolution in the last stretch was clear if uneven. **Week 10:** 5/8 new bests (including F6 −0.136 and F1 signal). **Week 11:** 4/8 (F4 0.675, F5 ≈3790, F7 1.866, F8 9.872) but F6 and F2 failed. **Week 12:** again 4/8 (F4 0.679, F5 ≈3801, F7 1.872, F8 9.873), F6 partial return, F2 still off the 0.777 peak. Some landscapes rewarded the local policy strongly (F4/F5/F7/F8); others stayed fragile (F2’s razor ridge; F1’s sparse detection problem; F6’s sharp cake basin).

If I had more time, I would allocate more of the early budget to learning global structure with a stricter experiment log, and I would test the weekly policy on known synthetic functions before spending portal queries. With a fresh start I would build idempotent data-append and config tracking from Week 1, and I would enforce “no leave basin without evidence” earlier on F2 and F6. I would still keep a GP surrogate at this sample size rather than replace it with a deep model.

**Trade-offs and decisions**

The main trade-off was between exploration and exploitation. Exploitation was attractive once high-reward neighbourhoods existed and the remaining budget was small. Excessive exploitation, however, could polish a null lobe (early F1) or over-trust a smooth GP step on a sharp ridge (F2/F6). I therefore used a hybrid that favoured proven clusters while preserving controlled exploration only where the surrogate was untrusted or a sensitive axis was still climbing (F5’s x₁).

Another trade-off concerned **automation versus human veto**. A fully automatic acquisition argmax would have been faster, but the best decisions — F1’s lobe switch, F5’s ridge lock, F6’s hard-return — required overriding a confident-looking posterior. A third trade-off was **model complexity**: a single interpretable GP per function versus ensembles or neural surrogates. I chose interpretability and ARD diagnostics over stacking models on n≈20–50 points.

Finally, **short-term greed versus long-term structure**: chasing the global acquisition surface sometimes looked clever for one week and destroyed a known peak the next. I balanced that by shrinking trust-region radius late in the project and by freezing ARD-inactive dimensions.

**Learning and application**

The most important lesson was that Bayesian optimisation is not just about picking EI or UCB. Pipeline quality depends on data handling, surrogate assumptions, constraints, diagnostics, and how much uncertainty you are willing to spend budget on. A theoretically neat method still fails if you leave a sharp basin, replay an incumbent, or exploit when every label is zero.

I would apply this to future work by starting with a reliable baseline, recording every configuration and outcome, and making one controlled change at a time. In real ML projects — hyperparameter tuning, A/B tests, expensive experimental design — the same sample-efficient loop matters whenever each trial costs time or money. Surrogate modelling plus uncertainty-aware acquisition reduces wasteful grid search; trust regions and ARD-style dimension focus speed convergence by freezing irrelevant knobs.

What surprised me most was how quickly early decisions shaped the apparent structure of the search space, and how **sharp** some functions were: millimetre-scale misses on F2 erased large apparent gains, and a “nearby” F6 step collapsed a hard-won best. Peer strategies also surprised me — some used heavier stacks (ensembles, SVM filters, neural surrogates, PCA dashboards). The useful overlap was the shared idea of compressing search onto a few active directions; my version of that idea was ARD + trust regions rather than a multi-model zoo.

Overall, the capstone changed my view of optimisation from repeatedly trying promising values to **managing uncertainty and information gain under a hard budget**. The final system was more systematic, more interpretable, and better at adapting its behaviour as new evidence arrived.
