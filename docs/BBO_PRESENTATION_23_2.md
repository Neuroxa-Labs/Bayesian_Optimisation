# BBO Capstone Presentation (Component 23.2) — Fill-in text

*Copy each section into the PDF template. First person. Based on work through Week 10 (5/8 improved) and Week 11 submitted.*

---

## 1. Overview of your BBO approach

I am trying to maximise eight unknown black-box functions (2D to 8D) under a hard budget: one query per function per week. I never see the true formula — only the input I send and the scalar output I get back. The goal is to climb each function’s best-so-far value as efficiently as possible, the same way an engineer would run expensive experiments when each trial costs time and money.

My overall strategy is Bayesian optimisation. I fit a Gaussian Process surrogate to the growing history of (x, y) pairs, then use an acquisition function (Expected Improvement or Upper Confidence Bound) to propose the next point. Per-function rules sit on top of that loop: noise modelling on F2, a log transform on F5’s large yields, locks on sensitive coordinates (for example F3’s safe x₃ band and F5’s high-face ridge), boundary penalties, and a trust region around the current best. When the surrogate has no usable signal (early F1), I refuse blind exploitation. Each week I submit, observe, update the data, and repeat.

---

## 2. How your strategy has evolved

Early rounds were broad: one GP + acquisition style for most functions, with more exploration and occasional queries pulled toward empty high-uncertainty corners. That taught me scale and sign, but it also produced wasted steps and boundary artefacts.

Data and failed weeks drove the change. Leaving a known good region without evidence hurt F2 and F6; micro-steps that were too large underperformed on F7; F1 stayed near zero until I stopped polishing a null lobe near (0.73, 0.73) and tested a peer-supported basin near (0.64, 0.68), which finally returned a measurable reading. Wins on F4, F5 and F8 from Week 8 onward rewarded tight local exploit.

Heuristics that now guide my queries: (1) stay inside a proven high-y cluster unless diagnostics say otherwise; (2) move only the sensitive dimensions (ARD length scales); (3) keep trust-region steps small late in the budget; (4) treat F1 with a trust gate — exploit only after non-null signal appears.

---

## 3. Patterns, data and insights

The clearest trend is uneven progress: mid-to-late weeks brought repeated gains on F4, F5, F6, F7 and F8 when I stayed local, while F1 and F2 needed special handling (sparse peak / noise). Week 10 was especially strong — five new bests — and opened an F1 signal cluster that earlier space-fill never found.

Variables that matter most differ by function. F5 is driven by x₁ along a high x₂–x₄ face (ridge climb 0.38→0.42→…). F2 lives on a sharp ridge near high x₁ and very low x₂. F3 is dominated by x₃ (safe vs toxic). F7/F8 behave like a few active coordinates plus flatter ones I largely freeze. That matches an ARD / “principal direction” view of the box: not every input deserves equal movement.

These observations changed how I see search: the unit hypercube is not eight independent knobs. It is a set of local basins and ridges. My job is to identify which cluster is real, compress the search around it, and stop spending queries on orthogonal noise.

---

## 4. Decision-making and iteration

I balance exploration and exploitation by phase and by evidence. Early weeks explored more; with ~20+ points I skew to exploitation inside trust regions. Exploration remains only where the model is untrusted (historical F1) or where a sensitive axis still moves best-y (F5’s x₁ walk).

Example that worked: Week 8–10 local exploit on F4/F5/F8 (and F6’s return-to-basin in Week 10) produced sustained best-y gains because the neighbourhood was already validated. Example that failed: chasing global acquisition or leaving F2’s 0.777 peak for a slightly wrong x₁ (the 0.72 “cliff”) dropped performance — the landscape was sharper than a smooth GP step assumed.

When results disagree with expectation, I do not inflate the model’s confidence. I shrink the step, return toward the incumbent with a new tiny offset, check noise (WhiteKernel on F2), or reopen a different cluster (F1’s switch from the null 0.73 lobe to 0.64/0.68). Uncertainty is used as a reason to sample carefully, not as a licence to jump to box corners.

---

## 5. Next steps and reflection

Next I will keep compressing trust regions around the Week 10 incumbents, continue the F5 ridge in small x₁ steps, pull F2 toward the historical 0.777 centroid, and micro-exploit F1’s signal lobe. For the final Module 24 round I plan near-pure exploitation if the next returns keep improving, with only a one-step pivot to a secondary cluster if a subspace bet goes flat.

In the wider ML landscape this project is sequential decision-making under a tiny data budget — the same setting as hyperparameter tuning, A/B tests, and experimental design. Gaussian Processes with acquisition functions are a standard tool when evaluations are expensive and uncertainty must drive the next trial.

For a non-technical stakeholder: we are running a careful series of experiments on eight hidden scoring systems. Each week we get only one trial per system, so we use past results to decide the next setting — focusing effort where we already see improvement, and changing course quickly when a region looks dead — instead of guessing randomly across the whole space.
