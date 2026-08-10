# Week 4 Discussion Reflection — BBO Capstone

**Word count:** ~680 (under 700)

---

This week I kept a **Gaussian Process (GP)** with Matérn kernel as my main surrogate, plus **Expected Improvement (EI)** or **UCB** to pick each query. I did **not** train a neural network or SVM as the primary model for choosing points — for three concrete reasons:

1. **Sample size (~13–43 points per function):** A small MLP or RBF-SVM can fit past y values but tends to **memorise** rather than generalise. Several peers saw NNs push queries to box corners (0 or 1) — a classic overfitting artefact, not a real peak.
2. **Uncertainty:** Bayesian optimisation needs **where to sample next**, not just a point prediction. GP gives μ(x) and σ(x) natively; standard SVM/NN regression does **not** give calibrated uncertainty for UCB/EI without extra machinery (ensembles, MC dropout, etc.).
3. **Goal mismatch:** SVM classification draws a **good vs bad boundary**; useful conceptually, but our weekly decision is **one acquisition score** (EI/UCB). GP + acquisition is the standard BO tool; I use SVM/NN ideas only as reflection, not as the query engine.

I am not rejecting NNs forever — if n grows (e.g. later weeks on F8), a net as a **second opinion** in empty regions could help. At Week 4, GP is the better trade-off between flexibility and reliability.

## What I did and why

**Function 1 (radiation, 2D):** Almost all readings are still ~0. A GP cannot reliably rank regions when there is no signal, so I used **random grid search** with a rule: stay at least 10% away from points I already tried, and prefer the **interior** of the box. This alternates with GP-based weeks — exploration without trusting a flat surrogate.

**Function 2 (noisy ML, 2D):** My best so far sits at high x₂ (~0.93). Peers suggested a **second peak** at low x₂. I sent **0.700000–0.020000** to test that hypothesis in one query rather than repeating the known region.

**Function 3 (drug side-effects, 3D):** Data show that **x₃ near 1.0 is dangerous** (very negative y), while good points have x₃ below ~0.5. I constrained x₃ < 0.5 and used **EI** in a narrow band around my best (−0.020) so the query does not get pulled into high-variance, risky corners.

**Function 4 (warehouse, 4D):** This landscape is **multimodal**. Wide exploration once dropped me to y ≈ −3.3; my best positive basin (y ≈ 0.26) came from staying local. Week 4 uses **EI within ±0.04** of that basin — exploit, not global UCB.

**Function 5 (chemical yield, 4D):** Yield jumped to **3108** after **log(y)** GP fitting and **EI exploit** on the upper face (high x₃, x₄). Week 4 query **0.380000–0.980000–0.980000–0.980000** pushes x₁ along the ridge while keeping x₃, x₄ high — not blind corner (0,0,1,1), which our data reject for x₁.

**Functions 6–7:** **EI** with **boundary penalties** and small search boxes around the current best. F7 improved to **1.525** in Week 3; the surface drops sharply nearby, so I take **small steps** (support-vector idea: bracket sharp changes, then exploit).

**Function 8 (8D):** **UCB** with penalty on box edges; **degenerate length scales** lock flat dimensions and only free sensitive axes — same idea as ARD: vary what matters, freeze what does not.

## Support vectors and gradients

Informative points are those where **y changes fast** between neighbours — e.g. F5 low vs high x₁, F3 safe vs toxic x₃. They act like **support vectors**: they tell me where a small **exploitative** step beats blind exploration.

I did not use **backprop on a neural net**. With only ~13–43 points per function, a net tends to **overfit** and push queries to **0 or 1** artefact boundaries. Instead, the GP gives a smooth posterior mean μ(x) and uncertainty σ(x); **EI and UCB** use both — that is a gradient-like climb tempered by variance.

## Classification framing (conceptual)

If I label top-quartile y as “good” and bottom as “bad”, the problem becomes a **decision boundary** search. **Logistic regression** is too linear for multimodal F4. An **RBF-SVM** could sketch boundaries but gives no calibrated σ for “where to sample next”. A **small NN** could fit patches but would likely **memorise** at this sample size. I kept classification as a **thought experiment**; the operational choice remains **GP + acquisition**.

## Model choice and complexity

**GP wins** for this budget because the decision is **where to sample**, not just fit past y. Kernels give non-linearity; length scales show **which inputs matter** (short ls on F3 x₃ and F5 x₁; on F8, x₃ and x₁ among the most sensitive — I vary those finely and lock flat dimensions). Neural nets may help later when n grows; here extra tuning, no σ, and overfit risk mean the added complexity is **not justified** yet.

## Boundary approximation (NN / classification)

I did not train a classifier or plot an NN decision boundary this week — the data are too sparse for an honest boundary. Conceptually, the steepest jumps in y between neighbouring points (F3 x₃ safe vs toxic, F5 x₁ low vs high yield) mark where a good/bad boundary would sit; backprop on a net would play a similar role (gradient = steepest ascent), but on our n that gradient would be **noise**. The GP posterior mean plays that role instead, tempered by σ in EI/UCB.

## Closing

Week 4 balances **peer insights** (F1 grid, F2 dual peak, F3 x₃ cap, F5 ridge) with **our own failures** (F4 global explore, F5 log-y success). One query per function forces clear, defensible choices under uncertainty.
