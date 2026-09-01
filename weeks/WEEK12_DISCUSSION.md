# Week 12 Discussion — PCA / variance lens (12th round)

*Copy-paste for the discussion board. First person. Under 700 words.*

---

**How my optimisation strategy has evolved**

In the early rounds I treated each black box more uniformly: fit a Gaussian Process, maximise EI or UCB over a wide box, and hope the acquisition surface pointed somewhere useful. That taught me sign and scale, but it also produced boundary artefacts and wasted steps in empty regions. As the history grew past ~20 points per function, the process became far more structured. I now keep a per-function policy: Matérn smoothness and noise settings, ARD length-scale diagnostics, explicit locks (F3’s safe x₃ band, F5’s high x₂–x₄ face), boundary penalties, and a trust-region radius around the incumbent. Weeks 8–11 rewarded that discipline: repeated gains on F4, F5, F7 and F8 when I stayed local, plus an F1 signal lobe near (0.64, 0.68) that space-fill never found. Week 11’s F6 collapse (−0.136 → −0.372) after a small step off the Week 10 cake centroid was the reminder that “nearby” is not enough if the principal basin is sharp — so Week 12 returns hard to that centroid.

**Which variables drive the most variation (PCA ↔ ARD)**

I do not run PCA as my weekly optimiser, but ARD length scales play the same role as principal components: they say which coordinates explain variation in y and which are nearly redundant. Empirically:

- **F5:** almost all late progress rides on x₁ along a locked high face — a one-dimensional ridge, like a dominant PC.
- **F2:** a thin ridge near high x₁ and very low x₂; tiny misses drop from 0.777 to ~0.55.
- **F3:** x₃ separates safe from toxic; other coords are secondary once that band is set.
- **F7 / F8:** a few active knobs plus flatter ones I largely freeze.
- **F4 / F6:** local basins in a low-dimensional active set; moving orthogonal to that set burns the weekly budget (F6 Week 11).

**Explore vs simplify — what I keep and what I lock**

I still explore only where the model is untrusted or a sensitive axis is still climbing (F1’s signal lobe; F5’s x₁ walk). Everywhere else I simplify: freeze inactive dimensions, shrink the trust radius, and query inside the proven cluster. Week 12 queries follow that split — ridge continue on F5, micros on F4/F7/F8, and **recovery** to historical centroids on F2/F3/F6 rather than fresh global search.

**Influence on the Module 24 final round**

If Week 12 keeps raising F4/F5/F7/F8 and repairs F6, the final round should be near-pure exploitation on compressed neighbourhoods. If a recovery fails, I allow one pivot to a secondary cluster — the same decision a PCA pipeline makes when a putative component stops explaining variance. I will not reopen full-box exploration this late unless a function is still null.

**How PCA-style thinking changes how I read BBO results**

Focusing on variance and redundancy reframes each portal return: a new best on a sensitive axis confirms that component; a drop after moving a “flat” coordinate suggests I spent budget on noise. The unit hypercube is not eight independent knobs — it is a low-effective-dimensional manifold of basins and ridges. My job is to identify that manifold, discard orthogonal motion, and spend the last queries where the data already say the variation lives.
