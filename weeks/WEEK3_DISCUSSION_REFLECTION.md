# Week 3 Discussion Reflection — BBO Capstone (Stage 2)

*Under 900 words — for portal discussion board. Written in first person.*

---

After two rounds of queries, my dataset has grown from the initial design points to 12–42 observations per function (depending on dimension). That is still tiny compared to the search space, but it is enough to see patterns: some strategies clearly paid off, others looked reasonable on the GP and still disappointed on the real black box. Week 3 is less about reinventing my pipeline and more about refining how I read the surrogate and when I trust it.

## How my strategy has changed

In Week 1 I leaned heavily on broad exploration — high-κ UCB for multimodal and high-dimensional functions, pure uncertainty-style coverage for the sparse radiation task (F1), and EI with a White noise kernel for the noisy 2D log-likelihood (F2). That worked unusually well: five of eight functions improved, including a large jump on chemical yield (F5, roughly 1089 → 2497).

Week 2 was a deliberate refinement pass, not a framework change. I kept per-function acquisition choices but added targeted fixes: coverage plus boundary penalties for F1, narrow local bounds on sensitive dimensions for drug side-effects (F3), and boundary penalties for the 8D ML task (F8). I also tightened exploitation on F5 once its output crossed a signal threshold. The week was weaker in raw outcomes (only F3 improved), but it taught me something important: a good GP recommendation is not always a good *experiment*, especially near box edges or when exploitation is pointed at the wrong peak neighbourhood.

Going into Week 3, I rely more on model predictions in low-dimensional functions with clear signal (F2, F5, F6) and still treat high-dimensional or multimodal ones (F4, F7, F8) as exploration-heavy. I tune hyperparameters per function — Matérn smoothness ν, GP noise α, κ for UCB — but several decisions remain heuristic: signal thresholds for F1/F5, local search radii for sensitive length scales, and explicit “do not hug the boundary” rules where GP uncertainty is misleading. Those heuristics came from failed queries, not from the textbook.

## Exploration vs exploitation

I use a calendar phase (weeks 1–4 exploration, later balanced, then exploit) but override it when the data justify that. F1 stays in exploration until any reading exceeds a tiny signal threshold; F5 switches to exploitation once yield passes 2000. Everything else follows the schedule with function-specific κ or EI.

The balance is asymmetric by design. After Week 1’s positive basin on warehouse placement (F4), Week 2 exploration wandered back into a deep negative region (−3.3). That reminded me that “exploit the model” and “exploit the best *observation*” are different things. For Week 3 I narrowed F4 search to a band around the best positive basin rather than the exact Week 1 coordinates — partly because multimodal landscapes punish greedy moves, and partly because I cannot assume every function is deterministic at the same x.

For F3, the opposite lesson applied: narrow exploitation around my current best (−0.02, closest yet to the safety target of 0) beat another wide exploratory jump. Exploration versus exploitation is not one global dial for me; it is a per-function choice driven by dimensionality, noise, and how much of the space I have already mapped.

## Would SVMs change my approach?

My surrogate is a Gaussian Process, not an SVM, but the course prompt is useful: both are kernel methods — they assume similarity in input space implies similarity in output.

A **soft-margin SVM** could classify regions as “promising” vs “unpromising” based on whether y is above or below a threshold (e.g. median or top quartile). That might be attractive for F1, where almost all labels are near zero and I mainly need to avoid wasting queries on dead zones. Classification would not give me a full response surface, but it could pre-filter candidate points before a finer GP or local search. The cost is losing graded information: a point with y = −0.02 and y = −0.4 would both be “low” even though F3 cares deeply about that gap.

A **kernel SVM regressor** (or SVR) could handle non-linear structure, similar to my Matérn GP. The practical blocker for Bayesian optimisation is **uncertainty**: UCB and expected improvement need μ and σ at candidate points. Standard SVMs do not provide calibrated predictive variance. I could ensemble SVMs or use distance-to-support-vector heuristics, but that adds complexity without clearly beating a GP on my small-N regime. Where SVM thinking *does* help is interpretability: support vectors highlight which observed runs actually constrain the decision boundary — analogous to which observations dominate the GP posterior.

If I integrated SVMs, the most realistic hybrid would be: SVM for coarse region screening (especially sparse or multimodal cases), GP for local refinement and acquisition. I have not implemented that in code; my Week 3 iteration instead strengthened GP-side heuristics (boundary penalties, local bounds, log-transform on F5 yield).

## Limitations as data grow

With only one new point per week, the GP can look confident while being wrong. I see this in **degenerate length scales** — dimensions hitting the upper bound, meaning the model treats them as flat and locks them to the current best. That helps in 6D/8D (F7, F8) but can also freeze me near suboptimal boundary values.

**Overfitting** is subtle here: with 12–32 points in 4–6 dimensions, the GP can interpolate idiosyncrasies. F5’s Week 2 exploit query was GP-plausible but returned 1811 vs my best 2497 — the model extrapolated a peak shape that the true yield surface did not support. I responded by switching exploitation to EI (which weights improvement over the incumbent f*) and constraining x₁ to the band where the true best was found.

**Irrelevant dimensions** are emerging via length scales: F3’s x₂ often looks degenerate while x₃ is highly sensitive; F7 locks several dimensions while I search locally in the rest. I treat small length scales as “move carefully” and large ones as “lock or explore broadly,” which is a manual form of feature relevance without explicit sparsity.

## Thinking like a data scientist under incomplete knowledge

This capstone mirrors real ML work for me: I rarely get unlimited evaluations, labels are noisy or expensive, and the true mechanism is hidden. Progress comes from documenting what each experiment ruled out, updating strategy when the model and reality disagree, and making assumptions explicit (my boundary penalties, signal thresholds, and per-function kernels are all assumptions I can defend or revise).

Two weeks of mixed results did not invalidate Week 1; they showed me that iteration is the product. My README, weekly reflections, and per-function analysis figures are as much part of the deliverable as the next x vector — they prove I can explain *why* I queried where I did, not just submit numbers.

---

*Word count: ~780*
