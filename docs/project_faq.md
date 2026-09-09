# Bayesian Black-Box Optimisation — Project FAQ

**Imperial College London · PCMLAI Stage 2 capstone**  
**Author:** Erkan Keskin · **Organisation:** Neuroxa-Labs  
**Repository:** https://github.com/Neuroxa-Labs/Bayesian_Optimisation  

This FAQ answers common questions about *this* repository and how the weekly black-box challenge was run. It is a portfolio companion to the final research report, not a substitute for the official course FAQ / brief.

---

## A. Challenge basics

### A1. What is the task?

Maximise eight unknown continuous black-box functions \(f_i : [0,1]^{d_i} \rightarrow \mathbb{R}\) (dimensions 2 through 8). Each week you may submit **one** query per function. The portal returns a scalar \(y\). Higher \(y\) is always better. The true formulas are withheld.

### A2. What counts as a “query”?

A six-decimal portal string such as `0.440000-0.980000-0.980000-0.980000`. Coordinates must lie in \([0,1]\). After the portal returns \(y\), that pair is appended to the function’s history and used for the next decision.

### A3. Do we need to recover the formula?

No. The goal is sample-efficient sequential decisions that find high-performing \(x\) values under a tiny weekly budget — not symbolic identification.

### A4. How many observations do we have?

Each function starts with an initial design (seed points in `data/function_*/`). Weekly portal points are appended. After Week 12, typical totals are roughly 22–52 points depending on dimension and seed size (see the final report table). Function 3 currently has 11 weekly rows in `data/` (no fabricated Week-12 point).

---

## B. Method

### B1. What is the primary optimiser?

A **Gaussian Process** with a **Matérn** kernel and **ARD** length scales, scored with **Expected Improvement (EI)** or **Upper Confidence Bound (UCB)**, plus a **trust region** around the incumbent for late exploit.

### B2. Why not a neural net as the weekly decider?

With \(n \approx 20\)–50 points, calibrated uncertainty matters more than flexible curve-fitting. Neural nets / large ensembles were used by some peers as diagnostics; they were **not** our primary portal decider.

### B3. What is the F1 “trust gate”?

Most of the F1 map reads ~0 (near-null labels). Exploiting a GP on a null map wastes budget on boundary artefacts. The trust gate refuses aggressive exploit until a measurable signal cluster appears; Weeks 10–12 opened a lobe near \((0.64, 0.68)\).

### B4. Why hard-return on F2 and F6?

Both have sharp basins. A “nearby” neighbour step can collapse \(y\) (F2 ~0.54 vs peak ~0.78; F6 Week-11 collapse after leaving the Week-10 centroid). Late policy returns toward the historical best after a failed neighbour.

### B5. What changed in Weeks 10–13?

Near-pure exploitation of proven regions: shrink trust regions, move only ARD-sensitive axes, hard-return after misses, and (F5) continue the ridge climb on \(x_1\).

---

## C. Results (after Week 12)

### C1. What are the best-so-far values?

| Fn | Best \(y\) | Status note |
|----|------------|-------------|
| F1 | 7.711×10⁻¹⁶ | Unresolved absolute peak; late signal lobe |
| F2 | 0.776645 | Strong sharp ridge |
| F3 | −0.011366 | Safe local band |
| F4 | 0.678600 | Strong late climb (W12) |
| F5 | 3800.74 | Clearest ridge success |
| F6 | −0.136 | W10 basin; fragile |
| F7 | 1.872233 | Strong late climb (W12) |
| F8 | 9.872928 | Strong late climb (W12) |

### C2. Did late weeks still improve?

Yes. Improve counts: W8 3/8 · W9 4/8 · W10 **5/8** · W11 4/8 · W12 4/8 (F4, F5, F7, F8).

### C3. Is F1 “solved”?

Not in this repository. Seed max remains the official best. Peers who found a large positive peak (e.g. ~0.5–2) demonstrate that a true spike exists; our Weeks 10–12 lobe is the first usable local basin we observed.

### C4. When will Week 13 results appear?

Week 13 queries are locked in `weeks/WEEK13_STRATEGY.md`. Portal \(y\) values are pending; append with `scripts/append_week13.py` and update the final report table when they arrive.

---

## D. Repository map

### D0. Where is the strategy hub?

Root [`STRATEGY.md`](../STRATEGY.md) — per-function GP/AF parameters, locks, late policy, and links into weekly notes.

### D1. Where is the executable code?

[`notebooks/BBO_Capstone_Optimized.ipynb`](../notebooks/BBO_Capstone_Optimized.ipynb)

### D2. Where is the written evidence pack?

- Markdown: [`docs/final_report.md`](final_report.md)
- PDF: [`docs/final_report.pdf`](final_report.pdf)
- This FAQ (PDF): [`docs/project_faq.pdf`](project_faq.pdf)

### D3. Where are figures and progress dashboards?

- Gallery: [`reports/analysis/README.md`](../reports/analysis/README.md)
- Progress: [`reports/progress/README.md`](../reports/progress/README.md)
- Per-function plots: `data/function_*/analysis_F*.png`

### D4. Where are transparency artefacts?

[`DATASHEET.md`](../DATASHEET.md) · [`MODEL_CARD.md`](../MODEL_CARD.md) · [`docs/TECHNICAL_JUSTIFICATION.md`](TECHNICAL_JUSTIFICATION.md)

### D5. How do I navigate course-style deliverables?

[`docs/COURSE_INDEX.md`](COURSE_INDEX.md)

---

## E. Practical / reproducibility

### E1. Can I reproduce a weekly decision?

Yes in spirit: reload that week’s history from `data/function_*/`, fit the GP with the notebook settings, and re-score candidates. Exact floating-point portal strings are logged in weekly strategy notes under `weeks/`.

### E2. Are random seeds fixed?

GP multi-restart fits and candidate searches can retain stochasticity. Treat weekly notes + locked portal strings as the audit trail for what was actually submitted.

### E3. What should I read first as a new visitor?

1. Root [`README.md`](../README.md)  
2. This FAQ or [`final_report.pdf`](final_report.pdf)  
3. [`reports/analysis/README.md`](../reports/analysis/README.md) for visuals  

---

## F. Honest limitations

- One query per function per week — no inner real-function line search.
- GPs can be confidently wrong in empty regions (inflated σ → boundary chase).
- Clustered sampling can miss a distant second mode (especially F1).
- F2’s observed peak may be an optimistic draw under noise.
- F3 weekly count in `data/` is 11; we did not fabricate a missing row.

---

*Version: v1 (pre–Week-13 portal results). Update C1 / C4 when Week 13 \(y\) values arrive.*
