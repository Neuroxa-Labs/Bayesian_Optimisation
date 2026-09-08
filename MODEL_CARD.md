# Model card — BBO optimisation approach

*Transparency documentation for the optimisation “model” (surrogate + acquisition + weekly policy). Written for the Imperial PCMLAI BBO capstone and kept as a portfolio artefact.*

---

## 1. Overview

| Field | Detail |
|-------|--------|
| **Name** | GP–BO Capstone Pipeline (v5) |
| **Type** | Bayesian optimisation with Gaussian Process surrogate and EI/UCB acquisition |
| **Version** | v5 unified pipeline (`notebooks/BBO_Capstone_Optimized.ipynb`) + weekly human-audited trust regions |
| **Task** | Maximise 8 unknown black-box functions, one query each per week |
| **Developer** | Student researcher, PCMLAI BBO capstone |
| **License** | Academic / course use via public GitHub repo |

---

## 2. Intended use

**Suitable for**

- Expensive black-box maximisation in \([0,1]^d\) with very few evaluations.
- Problems where calibrated uncertainty matters (explore/exploit).
- Per-function policies (noise, constraints, transforms).

**Target users.** Capstone peers, facilitators, and anyone reproducing the weekly loop from this repository.

**Avoid**

- Using the GP posterior as ground truth when signal is absent (especially F1).
- Replacing the pipeline with an unconstrained neural net on \(n \approx 20\) points as the sole decider (corner hallucinations).
- Safety-critical deployment without domain re-validation.

**Decision aid, not oracle.** Each portal \(y\) is the only ground truth; the model only proposes the next \(x\).

---

## 3. Details — strategy across rounds

**Core stack (unchanged backbone)**

1. Fit a **Matérn GP** (ARD length scales; multi-restart LML fit).
2. Choose **EI** or **UCB** (κ/ξ tuned per function and phase).
3. Optimise the acquisition (global + **trust-region** local search).
4. Apply constraints: F3 \(x_3\) lock, F5 high-face ridge, boundary penalties, anti-duplicate.
5. Submit six-decimal portal strings; append \(y\); repeat.

**Evolution (through Week 13 queries)**

| Phase | What changed |
|-------|----------------|
| Early | Broad exploration; learn sign/scale; avoid 0/1 artefacts |
| Mid | Per-function AF; WhiteKernel on F2; log-y on F5; locks / trust regions |
| Weeks 8–9 | Confirmed gains on F4/F5/F8 (and F7 by W9) |
| Weeks 10–12 | Strong local exploit (W10: 5/8; W11–W12: 4/8 on F4/F5/F7/F8); F1 signal lobe; F6 hard-return after W11 collapse; PCA/ARD discussion lens |
| Week 13 (final) | Near-pure exploit queries locked — see [`weeks/WEEK13_STRATEGY.md`](weeks/WEEK13_STRATEGY.md); portal `y` pending |

**Techniques used.** GP + EI/UCB; ARD; WhiteKernel; log transform; trust regions; signal thresholds / F1 trust gate; documented manual overrides in `weeks/WEEK*_STRATEGY.md`.

**Training data for the surrogate.** The growing evaluation history described in [`DATASHEET.md`](DATASHEET.md) — not an external public corpus.

---

## 4. Performance

**Primary metrics**

- Best-so-far \(y\) per function after each round.
- Whether the weekly query **improves** the incumbent.
- Qualitative diagnostics: length scales, boundary drift, trust-gate pass/fail.

**Summary after Week 12 (best observed ≈)**

| Fn | Best \(y\) (approx.) | Comment |
|----|----------------------|---------|
| F1 | \(\sim 0\) (signal lobe open) | Non-null lobe ~0.64/0.68 validated W10–W12 |
| F2 | **0.777** | Sharp/noisy ridge; late returns often ~0.54 |
| F3 | **−0.011** | Safe \(x_3\) band |
| F4 | **0.679** | Trust-region climb through W12 |
| F5 | **3801** | Ridge climb \(x_1\): 0.38→0.44 |
| F6 | **−0.136** | W10 incumbent; W11 collapse then partial W12 return |
| F7 | **1.872** | Local peak; W12 gain |
| F8 | **9.873** | Slow late improvements |

Week 10: 5/8 improved. Weeks 11–12: 4/8 improved (F4, F5, F7, F8). Progress is **uneven** — consistent with diminishing returns, sharp ridges, and occasional discontinuous jumps.

**Fairness metrics.** Not applicable (no demographic groups). “Fairness” here means not wasting budget on hallucinated corners and not over-claiming F1.

---

## 5. Assumptions and limitations

**Assumptions**

- One dominant smooth basin / ridge is often enough to climb with local BO.
- Stationary Matérn structure is adequate except where signal is null (F1) or noise dominates (F2).
- Six-decimal portal inputs are exact; outputs may be noisy (F2).

**Constraints / failure modes**

- **One query per function per week** — no inner real-function line search.
- GP can be confidently wrong in empty regions (inflated σ → boundary chase).
- Clustered sampling can miss a distant second peak.
- LOO/\(R^2\) style trust metrics are unstable at small \(n\).
- Observed best on noisy F2 may be an optimistic draw.

**Strengths.** Uncertainty-aware proposals; transparent weekly logs; strong recent gains where basins exist (F4/F5/F8).

---

## 6. Ethical considerations

**Transparency.** Datasheet + this model card + public GitHub (`weeks/` notes, notebook, reports) let peers reproduce decisions and challenge assumptions.

**Reproducibility.** Seeds/restarts and human overrides should be read from weekly files; the notebook is the executable core. Adding endless card prose does not replace those artefacts — the current structure is sufficient if the repo links stay accurate.

**Real-world adaptation.** The same discipline applies outside the course: document data provenance, intended use, failure modes, and evaluation cost before trusting an optimiser. Do not hide manual overrides.

**Risks.** Misreading near-zero F1 outputs as “optimised”; over-trusting a single noisy F2 max; presenting course black boxes as validated industrial models.
