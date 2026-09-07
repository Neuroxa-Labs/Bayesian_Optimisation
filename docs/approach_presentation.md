# Approach presentation — fill-in text

*Portfolio write-up of the BBO method (also used for the course presentation component). First person. Updated after Week 12 results (4/8 improved: F4, F5, F7, F8).*

---

## 1. Overview of your BBO approach

I am trying to maximise eight unknown black-box functions (2D to 8D) under a hard budget: one query per function per week. I never see the true formula — only the input I send and the scalar output I get back. The goal is to climb each function’s best-so-far value as efficiently as possible, the same way an engineer would run expensive experiments when each trial costs time and money.

Each function is framed as a different real-world task, which shapes how I interpret x and y. F1 is radiation-source detection on a 2-D map (sparse peak; most locations read ~0). F2 is tuning a noisy machine-learning log-likelihood. F3 is drug discovery aimed at reducing adverse reactions (three mixture components). F4 is warehouse item placement (four factors). F5 is chemical reaction yield (four process settings). F6 is cake-recipe optimisation (five ingredients). F7 is six-dimensional ML hyperparameter tuning. F8 is an eight-parameter ML model score. In every case I only observe a scalar performance signal, so the “true” industrial objective stays hidden behind the black box.

My overall strategy is Bayesian optimisation. I fit a Gaussian Process surrogate (Matérn kernel with Automatic Relevance Determination) to the growing history of (x, y) pairs, then use an acquisition function — Expected Improvement or Upper Confidence Bound — to propose the next point. That surrogate–acquisition loop is the spine of the project, but it is not used blindly: each function has its own rules layered on top.

Those rules include a WhiteKernel noise model on F2, a log transform on F5’s large chemical yields, hard locks on sensitive coordinates (F3’s safe x₃ band; F5’s high x₂–x₄ face), soft boundary penalties, and a shrinking trust region around the current best. When the surrogate has no usable signal — as with early F1, where almost every reading was ~0 — I refuse blind exploitation and route that function to controlled exploration until a real lobe appears. Each week I submit one formatted query string per function, observe the portal return, append it to the dataset, refit, and repeat.

---

## 2. How your strategy has evolved

Early rounds were broad. I used a similar GP + acquisition recipe across most functions, with higher exploration and occasional queries pulled toward empty high-uncertainty corners of the unit hypercube. That phase was useful: it taught me the scale and sign of each y, and it ruled out some dead regions. It also produced wasted steps, boundary artefacts, and over-confident jumps into space the model had never validated.

Data and failed weeks forced the change. Leaving a known good region without evidence hurt F2 and F6; micro-steps that were still too large underperformed on F7; F1 stayed near zero for a long time while I polished a null lobe near (0.73, 0.73). The turning point on F1 was testing a peer-supported basin near (0.64, 0.68), which returned measurable readings across Weeks 10–12 (down to ≈−0.005). From Week 8 onward, tight local exploit repeatedly lifted F4, F5 and F8, and Weeks 10–12 extended that pattern to F7. Week 11’s F6 collapse (−0.136 → −0.372) showed that “nearby” is not enough on a sharp basin; Week 12’s hard-return improved F6 to −0.205 but still short of the Week 10 incumbent — so recovery continues into the final round.

The heuristics that now guide my queries are concrete: (1) stay inside a proven high-y cluster unless diagnostics say otherwise; (2) move only the sensitive dimensions identified by ARD length scales (a PCA-style view of which axes carry variance); (3) keep trust-region steps small late in the budget; (4) keep a trust gate on F1 — exploit only after non-null signal appears; (5) hard-return to the incumbent centroid after a failed neighbour step. Week 12 applied this under a PCA/variance lens and confirmed the climb on F5 (x₁=0.44 → ≈3801) plus micro-gains on F4/F7/F8.

---

## 3. Patterns, data and insights

The clearest trend is uneven but compounding progress when I stay local. Weeks 8–12 repeatedly lifted F4, F5, F7 and F8. Week 10 was the strongest single week (5/8); Weeks 11 and 12 each added four more bests on the same exploit set. Week 12 specifically: F4 0.679, F5 ≈3801, F7 1.872, F8 9.873. F6 partially recovered (−0.372 → −0.205) but the Week 10 best (−0.136) still stands. F2 again missed the 0.777 needle (≈0.54). F1’s signal lobe near (0.64, 0.68) is now validated three times.

Which variables matter most differs by function. F5 is essentially a one-dimensional ridge: late progress rides on x₁ along a locked high x₂–x₄ face (0.38→0.44 and still climbing). F2 lives on a thin noisy ridge near high x₁ and very low x₂. F3 is dominated by x₃. F7 and F8 behave like a few active knobs plus flatter coordinates I freeze. F4 and F6 are local basins; orthogonal motion burns the weekly budget.

That matches an ARD / “principal component” reading of the box: not every input deserves equal movement. The unit hypercube is a set of basins and ridges on a lower-dimensional manifold. My job is to identify which cluster is real, compress search around it, and stop spending queries on orthogonal noise.

---

## 4. Decision-making and iteration

I balance exploration and exploitation by phase and by evidence. Early weeks explored more. With roughly twenty or more points per function I skew heavily to exploitation inside trust regions. Exploration remains only where the model is still untrusted (historical F1) or where a sensitive axis is still moving best-y (F5’s x₁ walk). Everywhere else, inactive dimensions are locked and the step size shrinks.

What worked: Weeks 8–12 local exploit on F4, F5, F7 and F8 produced sustained best-y gains because each neighbourhood was already validated; the GP ranked tiny offsets inside a basin rather than inventing a new mode. What failed: leaving F2’s 0.777 peak, or stepping slightly off F6’s −0.136 centroid, dropped performance — sharper than a smooth acquisition step assumed. Exact incumbent replays also wasted earlier weeks, so I always take a new offset even when returning to a cluster.

When results disagree with expectation, I shrink the step, return toward the incumbent, check noise (WhiteKernel on F2), or reassign the active cluster (F1’s switch from the null 0.73 lobe to 0.64/0.68; F6’s multi-week return after −0.372). Uncertainty is a reason to sample carefully inside a trusted region, not a licence to jump to box corners this late.

---

## 5. Next steps and reflection

Week 12 is complete (4/8 improved). For the **final round** I plan near-pure exploitation: continue the F5 ridge one more small x₁ step, micro-exploit the new F4/F7/F8 incumbents, pull F2 even closer to the historical [≈0.7179, 0.02] peak, protect F3’s −0.011 neighbourhood, finish F6’s return toward the Week 10 cake centroid, and stay inside F1’s signal lobe. I allow only a one-step pivot to a secondary cluster if a recovery goes flat; I will not reopen full-box exploration unless a function is still effectively null.

In the wider machine-learning landscape this project is sequential decision-making under a tiny data budget — the same setting as hyperparameter tuning, A/B testing, and experimental design. Gaussian Processes with acquisition functions are a standard tool when each evaluation is expensive and uncertainty must drive the next trial. The ARD / principal-axis view also mirrors dimensionality-reduction practice: spend effort where the variance in outcomes actually lives.

For a non-technical stakeholder: we are running a careful series of experiments on eight hidden scoring systems. Each week we get only one trial per system, so we use past results to decide the next setting — focusing effort where we already see improvement, returning quickly when a nearby guess fails, and changing course when a region looks dead — instead of guessing randomly across the whole space.
