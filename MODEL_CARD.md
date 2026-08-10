# Model Card — BBO Capstone Optimisation Approach

*Documentation for the optimisation “model” (surrogate + acquisition + weekly policy) used in the Imperial PCMLAI BBO capstone. Follows the Mini-lesson 21.2 model card framework.*

---

## 1. Overview

| Field | Detail |
|-------|--------|
| **Name** | GP–BO Capstone Pipeline (v5) |
| **Type** | Bayesian optimisation with Gaussian Process surrogate and EI/UCB acquisition |
| **Version** | v5 unified pipeline (`BBO_Capstone_Optimized.ipynb`) + weekly human-audited trust regions |
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

**Evolution (≈ ten rounds)**

| Phase | What changed |
|-------|----------------|
| Early | Broad exploration; learn sign/scale; avoid 0/1 artefacts |
| Mid | Per-function AF; WhiteKernel on F2; log-y on F5; degenerate length-scale locks |
| Later | Trust-region exploit around incumbents; trust gate on F1; hyperparameter / LLM-module reflections mapped onto BO knobs (κ, radius, constraints) |
| Weeks 8–9 | Confirmed gains on F4/F5/F8 (and F7 by W9); F2 remains noise-sensitive near \(x_1\approx 0.72\) |

**Techniques used.** GP + EI/UCB; ARD; WhiteKernel; log transform; trust regions; signal thresholds; soft-signal / space-fill when GP untrusted; documented manual overrides in `WEEK*_STRATEGY.md`.

**Training data for the surrogate.** The growing evaluation history described in [`DATASHEET.md`](DATASHEET.md) — not an external public corpus.

---

## 4. Performance

**Primary metrics**

- Best-so-far \(y\) per function after each round.
- Whether the weekly query **improves** the incumbent.
- Qualitative diagnostics: length scales, boundary drift, trust-gate pass/fail.

**Summary after Week 9 (best observed ≈)**

| Fn | Best \(y\) (approx.) | Comment |
|----|----------------------|---------|
| F1 | \(\sim 10^{-15}\)–\(0\) | No usable peak; trust-gate case |
| F2 | **0.777** | Sharp/noisy ridge; later returns often lower |
| F3 | **−0.011** | Safe \(x_3\) band; local moves mixed |
| F4 | **0.642** | Strong Week 8–9 emergence in basin |
| F5 | **3769** | Ridge climb \(x_1\): 0.38→0.40→0.41 |
| F6 | **−0.240** | Sensitive to step size |
| F7 | **1.858** | Local peak; small W9 gain |
| F8 | **9.869** | Slow late improvements |

Week 8: 3/8 improved (F4, F5, F8). Week 9: 4/8 improved (F4, F5, F7, F8). Progress is **uneven** — consistent with diminishing returns and occasional discontinuous jumps.

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

**Transparency.** Datasheet + this model card + public GitHub (`WEEK*` notes, notebook, reports) let peers reproduce decisions and challenge assumptions.

**Reproducibility.** Seeds/restarts and human overrides should be read from weekly files; the notebook is the executable core. Adding endless card prose does not replace those artefacts — the current structure is sufficient if the repo links stay accurate.

**Real-world adaptation.** The same discipline applies outside the course: document data provenance, intended use, failure modes, and evaluation cost before trusting an optimiser. Do not hide manual overrides.

**Risks.** Misreading near-zero F1 outputs as “optimised”; over-trusting a single noisy F2 max; presenting course black boxes as validated industrial models.
