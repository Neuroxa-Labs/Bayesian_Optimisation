# BBO Capstone Presentation (Component 23.2) — Fill-in text

*Copy each section into the PDF template. First person. Moderately expanded after Week 11 results + Week 12 queries submitted (awaiting y).*

---

## 1. Overview of your BBO approach

I am trying to maximise eight unknown black-box functions (2D to 8D) under a hard budget: one query per function per week. I never see the true formula — only the input I send and the scalar output I get back. The goal is to climb each function’s best-so-far value as efficiently as possible, the same way an engineer would run expensive experiments when each trial costs time and money.

My overall strategy is Bayesian optimisation. I fit a Gaussian Process surrogate (Matérn kernel with Automatic Relevance Determination) to the growing history of (x, y) pairs, then use an acquisition function — Expected Improvement or Upper Confidence Bound — to propose the next point. That surrogate–acquisition loop is the spine of the project, but it is not used blindly: each function has its own rules layered on top.

Those rules include a WhiteKernel noise model on F2, a log transform on F5’s large chemical yields, hard locks on sensitive coordinates (F3’s safe x₃ band; F5’s high x₂–x₄ face), soft boundary penalties, and a shrinking trust region around the current best. When the surrogate has no usable signal — as with early F1, where almost every reading was ~0 — I refuse blind exploitation and route that function to controlled exploration until a real lobe appears. Each week I submit one formatted query string per function, observe the portal return, append it to the dataset, refit, and repeat.

---

## 2. How your strategy has evolved

Early rounds were broad. I used a similar GP + acquisition recipe across most functions, with higher exploration and occasional queries pulled toward empty high-uncertainty corners of the unit hypercube. That phase was useful: it taught me the scale and sign of each y, and it ruled out some dead regions. It also produced wasted steps, boundary artefacts, and over-confident jumps into space the model had never validated.

Data and failed weeks forced the change. Leaving a known good region without evidence hurt F2 and F6; micro-steps that were still too large underperformed on F7; F1 stayed near zero for a long time while I polished a null lobe near (0.73, 0.73). The turning point on F1 was testing a peer-supported basin near (0.64, 0.68), which finally returned measurable readings (Week 10 ≈−0.008, Week 11 ≈−0.006). From Week 8 onward, tight local exploit repeatedly lifted F4, F5 and F8, and Weeks 10–11 extended that pattern to F7 as well. Week 11’s F6 collapse (−0.136 → −0.372) after a small step off the Week 10 cake centroid was equally important: it showed that “nearby” is not enough when the principal basin is sharp.

The heuristics that now guide my queries are therefore concrete: (1) stay inside a proven high-y cluster unless diagnostics say otherwise; (2) move only the sensitive dimensions identified by ARD length scales (a PCA-style view of which axes carry variance); (3) keep trust-region steps small late in the budget; (4) keep a trust gate on F1 — exploit only after non-null signal appears; (5) hard-return to the incumbent centroid after a failed neighbour step. Week 12 applies exactly this policy under a PCA/variance lens: climb the active axis on F5, micro-exploit new bests on F4/F7/F8, and recover F2/F3/F6 toward their true centroids.

---

## 3. Patterns, data and insights

The clearest trend is uneven but compounding progress when I stay local. Weeks 8–11 repeatedly lifted F4, F5, F7 and F8. Week 10 was the strongest single week (5/8 new bests, including a large F6 jump to −0.136). Week 11 added four more bests (F4 0.675, F5 ≈3790, F7 1.866, F8 9.872) while F6 failed badly and F2 missed the historical 0.777 needle (returning 0.55). F1’s signal cluster near (0.64, 0.68) is now validated twice, even though under pure maximisation those readings are still not the global best.

Which variables matter most differs by function — and that is the main insight. F5 is essentially a one-dimensional ridge: almost all late progress rides on x₁ along a locked high x₂–x₄ face (climb 0.38→0.43, with Week 12 probing x₁=0.44). F2 lives on a thin noisy ridge near high x₁ and very low x₂; millimetre-scale misses drop performance sharply. F3 is dominated by x₃ (safe versus toxic). F7 and F8 behave like a few active knobs plus flatter coordinates I largely freeze. F4 and F6 are local basins in a low-effective-dimensional active set; moving orthogonal to that set burns the weekly budget, as Week 11 showed on F6.

That pattern matches an ARD / “principal component” reading of the box: not every input deserves equal movement. The unit hypercube is not eight independent knobs. It is a set of local basins and ridges on a lower-dimensional manifold. My job is to identify which cluster is real, compress search around it, and stop spending queries on orthogonal noise.

---

## 4. Decision-making and iteration

I balance exploration and exploitation by phase and by evidence. Early weeks explored more, because the posterior was weak and the map was empty. With roughly twenty or more points per function I skew heavily to exploitation inside trust regions. Exploration remains only where the model is still untrusted (historical F1) or where a sensitive axis is still moving best-y (F5’s x₁ walk). Everywhere else, inactive dimensions are locked and the step size shrinks.

Concrete examples make the trade-off clear. What worked: Weeks 8–11 local exploit on F4, F5, F7 and F8 produced sustained best-y gains because each neighbourhood was already validated by previous returns; the GP was used to rank tiny offsets inside a basin, not to invent a new mode across the box. What failed: leaving F2’s 0.777 peak or F6’s −0.136 centroid for a slightly wrong neighbour dropped performance — the landscape was sharper than a smooth acquisition step assumed. Exact incumbent replays also wasted weeks earlier, so I always take a new offset even when returning to a cluster.

When results disagree with expectation, I do not inflate the model’s confidence. I shrink the step, return toward the incumbent with a fresh tiny offset, check noise modelling (WhiteKernel on F2), or reassign the active cluster (F1’s switch from the null 0.73 lobe to 0.64/0.68; F6’s Week 12 hard-return after the −0.372 miss). Uncertainty is treated as a reason to sample carefully inside a trusted region, not as a licence to jump to unexplored box corners this late in the budget.

---

## 5. Next steps and reflection

Week 12 queries are already submitted under a PCA/ARD lens and await portal returns. They encode the current policy explicitly: F1 stays in the signal lobe (`0.636–0.687`); F2 returns toward the historical 0.777 peak (`0.7179–0.0200`); F3 protects the −0.011 neighbourhood with x₃ locked; F4, F7 and F8 take micro-steps from the Week 11 incumbents; F5 continues the ridge at x₁=`0.44` on the locked high face; F6 hard-returns toward the Week 10 cake centroid after the −0.372 miss. For Module 24’s final round I plan near-pure exploitation on these compressed neighbourhoods if Week 12 confirms the climbs and recoveries, with only a one-step pivot to a secondary cluster if a subspace bet goes flat again. I do not intend to reopen full-box exploration this late unless a function is still effectively null.

In the wider machine-learning landscape this project is sequential decision-making under a tiny data budget — the same setting as hyperparameter tuning, A/B testing, and experimental design. Gaussian Processes with acquisition functions are a standard tool when each evaluation is expensive and uncertainty must drive the next trial. The ARD / principal-axis view also mirrors dimensionality-reduction practice: spend effort where the variance in outcomes actually lives.

For a non-technical stakeholder: we are running a careful series of experiments on eight hidden scoring systems. Each week we get only one trial per system, so we use past results to decide the next setting — focusing effort where we already see improvement, returning quickly when a nearby guess fails, and changing course when a region looks dead — instead of guessing randomly across the whole space.
