# Successful Optimisation Strategies — Discussion

*Copy-paste for the discussion board. First person. Under 2000 words. Peer example: Matt (public Capstone repo / multi-model pipeline).*

**Repository:** https://github.com/Neuroxa-Labs/Bayesian_Optimisation

---

**Which strategies led to my strongest results — and why**

My strongest results came from a small set of disciplined habits, not from stacking more models.

1. **Trust-region local exploitation once a basin was validated.** From Week 8 onward, almost every new best on F4, F5, F7 and F8 came from tiny offsets inside a neighbourhood that had already returned high y. Global EI/UCB into empty corners looked clever early, but late in the budget it burned queries. Compressing the search radius made the GP useful as a *local ranker* of nearby candidates rather than as a global oracle.

2. **Move only sensitive axes (ARD / “principal direction” thinking).** F5 is the clearest example: locking the high x₂–x₄ face and climbing x₁ (0.38→0.44) produced a sustained yield run to ≈3801 by Week 12. Freezing flat dimensions stopped me from spending the weekly shot on orthogonal noise — the same intuition PCA gives, implemented through GP length scales.

3. **Per-function policy instead of one recipe for all eight.** WhiteKernel + caution on F2’s noisy ridge; log-y on F5; hard x₃ lock on F3; a **trust gate** on F1 that refused exploitation while every label was ~0, then switched to the (0.64, 0.68) signal lobe once a non-null reading appeared. Treating radiation detection as “find signal first, maximise later” changed my decisions more than any acquisition tweak.

4. **Hard-return after a failed neighbour step.** Week 11’s F6 collapse (−0.136 → −0.372) was expensive proof that “nearby” is not enough on a sharp cake basin. Week 12’s return toward the Week 10 centroid (−0.205) did not reclaim the best, but it restored the right *policy*: do not invent a second mode without evidence.

These strategies influenced the challenge as a phase shift: early weeks bought map coverage; mid weeks specialised the surrogate and constraints; late weeks (10–12) were almost pure exploit on F4/F5/F7/F8, with recovery pulls on F2/F3/F6. The leaderboard ticks followed that shift — Week 10’s 5/8, then two more 4/8 rounds on the same exploit set.

**What makes a strategy ‘successful’**

Outcomes matter — new bests are the only ground truth the portal gives. But outcomes alone are a thin definition of success in a 13-week, one-query budget. I also count:

- **Adaptability:** changing policy when feedback contradicts the model (F1 lobe switch; F6 hard-return).
- **Reasoning quality:** being able to explain *why* this x, in writing, before submitting.
- **Efficiency:** information or improvement per scarce evaluation — not FLOPs spent on an ensemble that the sample size cannot support.

A run that climbs steadily with auditable decisions is more “successful” for professional transfer than a lucky spike I cannot reproduce. Conversely, a sophisticated pipeline that repeatedly leaves a sharp peak is unsuccessful even if it looks impressive in a notebook.

**Application beyond the BBO capstone**

The same pattern applies wherever evaluations are expensive: hyperparameter tuning, A/B tests, chemical or materials experiments, calibration of production ML systems. Start with a simple uncertainty-aware baseline (often a GP or a well-regularised surrogate), keep a trust region around incumbents, freeze irrelevant knobs (feature / parameter ARD or ablation), and treat every trial as a policy update. When a nearby change fails, return to the last verified configuration instead of wandering. In industry that discipline saves GPU hours and calendar time the same way it saved weekly portal shots here.

**Peer reflection — Matt’s approach**

I looked closely at Matt’s public Capstone work (https://github.com/Matt-H77/Capstone). His successful strategies differ in tooling but overlap in *intent*. He built a richer stack week by week: GP ensembles across kernels, SVM filtering of high-yield candidates, neural-net views as a second opinion, cross-model comparison reports, duplicate/noise handling, KD-tree distance filters to stop redundant queries, PCA diagnostics, and a clear **terminal-exploitation** switch for the final round (posterior mean over exploration-weighted acquisition). That progression is itself a successful meta-strategy: each week answered a concrete failure mode from the last.

What made those ideas effective, in my view, was not “more models = better,” but **evidence-based candidate comparison** and **explicit late-game exploitation**. Preventing near-duplicate submissions and comparing GP / Thompson / NN / SVM recommendations reduces the chance that one overconfident acquisition score dominates. His Week 12 stance — disable exploratory Thompson when no future budget remains — is exactly the bandit logic I used more quietly through trust-region shrinkage.

Overlap with my strategy: both of us ended in compressed, high-reward neighbourhoods; both used diagnostics (his PCA/cross-model tables; my ARD, trust regions, and weekly reflections) to decide what to freeze; both treated F1-like sparse problems as special. Divergence: I kept a single interpretable GP per function and put complexity into *policy* (locks, trust gate, hard-return). Matt put more complexity into *model plurality*. On n≈20–50 points I still prefer the lighter surrogate; his stack is a strong reminder that **candidate hygiene and terminal exploitation** can matter as much as the kernel.

**Suggestions and how peer work broadens ‘success’**

If I were suggesting a perspective to strengthen an approach like Matt’s, I would keep the cross-model comparison but add an explicit “basin loyalty” rule for sharp ridges (my F2/F6 lesson): when several models disagree, prefer the incumbent neighbourhood unless a secondary basin has already produced a competitive *observed* y, not only a high predicted mean. Conversely, his duplicate-distance filtering and final-round “no exploration budget left” framing are perspectives I would borrow more formally into my own scripts.

Peers broadened my definition of success: it is not only climbing the leaderboard on one function, but building a **repeatable decision system** — clear reports, public repos, and a story of why the last query was chosen. Matt’s write-ups show that transparency and staged improvement are part of professional-grade optimisation practice, not extras. That sits alongside raw y: a successful strategy is one you can defend, adapt, and carry into the next expensive experiment.
