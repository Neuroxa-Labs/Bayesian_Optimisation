# STRATEGY.md — Per-function structures, hyperparameters & weekly progress

Imperial College London · PCMLAI Stage 2 · Black-Box Bayesian Optimisation  
**Same level as** [`README.md`](README.md) **and** [`DATASHEET.md`](DATASHEET.md) — this is the main strategy document for the repository.

| | |
|--|--|
| **Author** | Erkan Keskin · Neuroxa-Labs |
| **Status** | Weeks 1–12 complete · Week 13 queries locked · portal \(y\) pending |
| **Code source of truth** | [`notebooks/BBO_Capstone_Optimized.ipynb`](notebooks/BBO_Capstone_Optimized.ipynb) — `FUNCTIONS`, `STRATEGY`, `GP_CONFIG` |
| **Weekly detail files** | [`weeks/WEEK*_STRATEGY.md`](weeks/) (portal strings + that week’s rationale) |
| **Evidence pack** | [`docs/final_report.md`](docs/final_report.md) · [`docs/final_report.pdf`](docs/final_report.pdf) |

This file answers, **for every function**: what structures we used, which hyperparameters / locks applied, how acquisition-function (AF) choices behaved, and how the approach progressed week by week.

**Not in scope:** recovering a closed-form \(f(x)\). The portal is a black box; we only ever observe \((x,y)\). The GP supplies a **surrogate** \(\mu(x),\sigma(x)\), not the true formula.

---

## Contents

1. [Shared pipeline & global hyperparameters](#1-shared-pipeline--global-hyperparameters)
2. [Acquisition functions — formulas & effects](#2-acquisition-functions--formulas--effects)
3. [Quick map (all eight)](#3-quick-map-all-eight)
4. [F1 — Radiation](#4-f1--radiation-source-2d)
5. [F2 — Noisy ML](#5-f2--noisy-ml-score-2d)
6. [F3 — Drug / adverse](#6-f3--drug--adverse-3d)
7. [F4 — Warehouse](#7-f4--warehouse-4d)
8. [F5 — Chemical yield](#8-f5--chemical-yield-4d)
9. [F6 — Cake recipe](#9-f6--cake-recipe-5d)
10. [F7 — HP tuning](#10-f7--hyperparameter-tuning-6d)
11. [F8 — 8-param ML](#11-f8--eight-parameter-ml-8d)
12. [Late policy (W10–13)](#12-late-policy-weeks-1013)
13. [Week file index](#13-week-file-index)

---

## 1. Shared pipeline & global hyperparameters

### Structure (every function)

```text
history (x, y)
    → Matérn GP + ARD length scales (multi-restart LML)
    → acquisition score (EI or UCB; F1 may use uncertainty / coverage)
    → candidate search (global + local / trust region)
    → per-function locks, trust gate, boundary penalty, anti-duplicate
    → one six-decimal portal string
    → append portal y → next week
```

Neural nets / Optuna / TuRBO were **not** the primary weekly portal decider. The GP remained the core structure; weekly files record tactical changes around that core.

### Global `GP_CONFIG` (notebook defaults)

| Hyperparameter | Value | Meaning |
|----------------|------:|---------|
| Kernel family | Matérn + ARD | Independent length scale per dimension |
| `nu` (default) | 2.5 | Smoothness (overridden on F1 / F3 / F8) |
| `n_restarts_optimizer` | 10 | Restarts for length-scale fit |
| `normalize_y` | True | Standardise \(y\) before GP fit |
| `length_scale_bounds` | (1e−2, 10) | ARD search box |
| `degenerate_threshold` | 8.0 | Large LS → lock that dimension to incumbent |
| `boundary_buffer` | 0.02 | Soft keep-away from \([0,1]\) edges |
| `boundary_penalty_weight` | 0.5 | Penalty weight on near-edge candidates |
| `local_explore_radius` | 0.15 | Default local / trust-region radius |
| `sensitive_ls_thr` | 0.2 | Small LS → “move carefully” |
| `sensitive_bound_k` | 2.5 | Local bound ≈ \(k \times\) length scale |
| `sensitive_bound_min_radius` | 0.08 | Floor on that local bound |

### Calendar phases (guideline, overridden per function when needed)

| Phase | Weeks | Intent |
|-------|-------|--------|
| Explore | 1–4 | Map basins, coverage, avoid premature lock |
| Balanced | 5–9 | Exploit where signal exists; keep options open |
| Exploit | 10–13 | Trust-region micro-steps, hard-return, ridge continue |

---

## 2. Acquisition functions — formulas & effects

The GP posterior at a candidate \(x\) is summarised by mean \(\mu(x)\) and std \(\sigma(x)\). An **acquisition function** turns that into a score; we pick \(\arg\max_x a(x)\) (then apply locks / penalties). Changing the AF changes *where* the next query lands — not the black-box \(f\) itself.

### Formulas (what we maximise)

| AF | Score (conceptually) | Dial |
|----|----------------------|------|
| **EI** (Expected Improvement) | \(a_{\mathrm{EI}}(x) = \mathbb{E}\big[\max(0,\ f(x)-y^\star)\big]\) under the GP — prefers points likely to beat the incumbent \(y^\star\) | Implicit explore/exploit via \(\sigma\); no κ |
| **UCB** (Upper Confidence Bound) | \(a_{\mathrm{UCB}}(x) = \mu(x) + \kappa\,\sigma(x)\) | **κ large** → chase uncertainty (explore); **κ small** → trust \(\mu\) (exploit) |
| **Uncertainty / σ** | \(a(x) \propto \sigma(x)\) (or related coverage heuristics) | Pure exploration — ignore \(\mu\) |
| **Coverage / space-fill** | Prefer candidates far from past \(x\) (plus boundary penalty) | Exploration when the GP is untrusted |

We never write down a closed form for the true \(f_i(x)\). After each portal return we only update the dataset and refit \(\mu,\sigma\).

### What changes when you pick each AF

| If you choose… | Typical query behaviour | Upside | Downside we actually saw |
|----------------|-------------------------|--------|---------------------------|
| **EI** | Balances “beat best” vs uncertainty; often near the incumbent once a peak exists | Good on noisy / sharp ridges (F2) and interior cake steps (F6); natural for “improve \(y^\star\)” | Can overshoot a razor ridge (F2 W6) or step just off a sharp basin (F6 W11) |
| **UCB, high κ** (~2.5–3) | Pulls toward high-\(\sigma\) regions / second modes | Escapes local traps early (F4 W1 basin discovery; F3/F8 early map) | Expensive bad samples on multimodal maps (F4 W2 deep negatives) |
| **UCB, low κ** (~0.5–1.5) | Stays near high \(\mu\) | Stable late climb (F8 light exploit; F5 signal-triggered exploit) | If \(\mu\) is wrong, reinforces a bad neighbourhood |
| **Uncertainty / coverage** | Spreads queries; ignores peak hunting | Necessary on F1 while all labels ~null (trust gate) | Alone never “solves” a sparse peak — needs a later exploit mode once signal appears |
| **Switch EI ↔ UCB mid-project** | Re-aims the search when landscape knowledge changes | F3/F4/F5: explore with UCB, then EI (or low-κ UCB) once a basin/ridge is proven | Switching too early freezes on a weak basin; switching too late wastes budget |

### AF → effect on each function (summary)

| Fn | AF path | What that AF choice did in practice |
|----|---------|-------------------------------------|
| **F1** | Uncertainty / coverage early → **refuse GP AF exploit** (trust gate) → late **local micro** in signal lobe | High-σ / coverage stopped wasted “null-map exploit”. Once a lobe appeared (~0.64/0.68), AF no longer drove global jumps — geometry + trust gate did. |
| **F2** | **EI** + WhiteKernel all the way | EI found the sharp ridge (W5, \(y≈0.777\)). Same EI later proposed “nearby” points that missed (~0.54) → we added **hard-return**, i.e. overrode AF when neighbour EI was unsafe. |
| **F3** | **UCB** (κ≈2.576) → **EI** + \(x_3\) lock | UCB mapped sensitive \(x_3\); EI + lock tightened to \(y≈-0.011\). Without the lock, AF alone kept drifting \(x_3\) into unsafe bands. |
| **F4** | High-κ **UCB** → local **EI** / low-radius trust region | High κ found a usable basin (costly misses early). Local EI produced the late climb 0.47→0.68; global UCB would have kept jumping. |
| **F5** | **UCB** + signal threshold → **EI + log-\(y\)** + face lock | UCB/threshold got the first big yield jump; log-y EI + locked \(x_2..x_4\) turned AF into a **1D ridge walk on \(x_1\)** (3744→3801). |
| **F6** | **EI** + interior / boundary penalty | EI improved toward −0.136 (W10). After W11 collapse, hard-return overrode AF — EI’s “local improve” proposal was too wide for a razor basin. |
| **F7** | **EI** + boundary soft + ARD locks | EI gave steady 6D gains; degenerate dims removed from the AF search so budget stayed on sensitive axes (late 1.857→1.872). |
| **F8** | **UCB** κ≈2.576 → κ≈1.5 light exploit | High κ mapped 8D early; lowering κ turned AF into slow ~0.001 ticks (9.86→9.87) instead of edge-chasing σ artefacts. |

**Takeaway.** AF choice sets the *default* explore/exploit bias. On this budget, the largest gains often came from **pairing** AF with structures (trust gate, locks, log-\(y\), hard-return) that stop the AF from acting on a wrong GP belief.

---

## 3. Quick map (all eight)

| Fn | \(d\) | Seed `n_init` | Profile | Key structures | Best \(y\) (W12) |
|----|------:|--------------:|---------|----------------|------------------|
| F1 | 2 | 10 | sparse_peak | Trust gate · coverage · late lobe micro | 7.711×10⁻¹⁶ |
| F2 | 2 | 10 | noisy | WhiteKernel · EI · hard-return | 0.776645 |
| F3 | 3 | 15 | negative | UCB→EI · \(x_3\) lock ≈0.401 | −0.011366 |
| F4 | 4 | 30 | multimodal | UCB→local EI · trust-region micro | 0.678600 |
| F5 | 4 | 20 | unimodal | log-\(y\) · high-face lock · \(x_1\) climb | 3800.74 |
| F6 | 5 | 20 | negative | EI · interior · hard-return to W10 | −0.136 |
| F7 | 6 | 30 | high_dim | EI · boundary soft · ARD micro | 1.872233 |
| F8 | 8 | 40 | high_dim | UCB · boundary · ARD micro | 9.872928 |

---

## 4. F1 — Radiation source (2D)

### Structures & hyperparameters

| Item | Setting |
|------|---------|
| Task | Locate hidden radiation source; most map ~0 |
| Dim / seed | 2D · `n_init` = 10 |
| Profile | `sparse_peak` |
| `gp_alpha` | 1e−12 |
| Matérn `nu` | **0.5** (rougher than global 2.5) |
| Notebook AF | Explore: **uncertainty** · Exploit: **UCB** (`kappa_expl` = 3.0) |
| `signal_thr` | 1e−4 |
| WhiteKernel / log-\(y\) | No |
| **Special structure** | **Trust gate** — refuse GP exploit while labels are ~null |
| **AF effect here** | Uncertainty/coverage stops null-map “fake peaks”; after W10 lobe, queries are lobe micro-steps (AF not free to roam) |

### Weekly progress

| Week | Strategy / structure used | Outcome note |
|------|---------------------------|--------------|
| 1 | Uncertainty / pure exploration | All ~null; no usable signal |
| 2–3 | Coverage + boundary penalty; interior probes | Still ~null |
| 4–5 | Random / coverage grid (≥10% from past) | Still no signal |
| 6 | Manual refine near warm seed `[0.731, 0.733]` | Seed null remains “best” |
| 7 | Soft-signal heuristics (log10 ranking / SVM / IF) | Warm UR band probe |
| 8–9 | **Trust gate on** — GP exploit refused; space-fill | No false exploit |
| 10 | Pivot to peer-informed lobe **~0.64 / 0.68** | First measurable: ≈ −0.008 |
| 11 | Tight exploit in confirmed lobe | ≈ −0.006 |
| 12 | Signal-lobe micro-step | ≈ −0.005 |
| 13 | Locked: `0.635000-0.688000` | Portal \(y\) pending |

**Incumbent (official max):** \(y = 7.711\times10^{-16}\) at `[0.731024, 0.733000]` (seed) — never beaten. Late lobe is the first **usable basin**, not the absolute max.

**Detail:** [`data/function_1/EXPLANATION_F1.md`](data/function_1/EXPLANATION_F1.md) · `analysis_F1.png`

---

## 5. F2 — Noisy ML score (2D)

### Structures & hyperparameters

| Item | Setting |
|------|---------|
| Task | Two ML knobs; noisy log-likelihood |
| Dim / seed | 2D · `n_init` = 10 |
| Profile | `noisy` |
| `gp_alpha` | 1e−8 |
| Matérn `nu` | default 2.5 |
| **WhiteKernel** | **True** (noise model) |
| AF | **EI** throughout |
| **Special structure** | Sharp ridge + **hard-return** after neighbour misses |
| **AF effect here** | EI discovered the W5 ridge; the same EI later proposed unsafe neighbours → hard-return overrides AF |

### Weekly progress

| Week | Strategy / structure used | Outcome note |
|------|---------------------------|--------------|
| 1–3 | EI; noise-aware; don’t abandon on one bad draw | Building ridge map |
| 4 | Manual low-\(x_2\) peak test | Best ≈ **0.660** |
| 5 | EI exploit high-\(x_1\) / low-\(x_2\) | **Record 0.777** at `[0.717869, 0.020000]` |
| 6 | EI overshoot (\(x_1\)≈0.75) | Collapse ≈ 0.403 |
| 7–8 | Return toward W5 ridge; probe left of “cliff” | Ridge fragile |
| 9 | Tiny offset toward incumbent (no exact replay) | Protect peak |
| 10 | Toward historical 0.777 | Partial |
| 11 | Neighbour toward centroid | Miss ≈ 0.548 |
| 12 | **Hard-return** tighter to `[0.7179, 0.02]` | Protect |
| 13 | Locked: `0.717870-0.020000` | Portal \(y\) pending |

**Incumbent:** \(y = 0.776645\) (Week 5) — held; never reclaimed after misses.

**Detail:** [`data/function_2/EXPLANATION_F2.md`](data/function_2/EXPLANATION_F2.md) · `analysis_F2.png`

---

## 6. F3 — Drug / adverse (3D)

### Structures & hyperparameters

| Item | Setting |
|------|---------|
| Task | Three mixture ratios; nearer zero = safer |
| Dim / seed | 3D · `n_init` = 15 |
| Profile | `negative` |
| `gp_alpha` | 1e−6 |
| Matérn `nu` | **1.5** |
| Notebook AF | **UCB** κ = 2.576 (early); practice shifted to **EI** + locks mid-project |
| **Special structure** | **Safe \(x_3\) lock ≈ 0.401** (from Week 5) |
| Data note | 11 weekly rows in `data/` (no fabricated W12 point) |
| **AF effect here** | UCB mapped \(x_3\) risk; EI+lock converted AF into safe-band refine (without lock, AF drifted \(x_3\)) |

### Weekly progress

| Week | Strategy / structure used | Outcome note |
|------|---------------------------|--------------|
| 1 | UCB explore; \(x_3\) already sensitive | Mapping |
| 2 | UCB + narrow bounds on \(x_3\) | Best ≈ **−0.020** |
| 3 | Local bounds; \(x_2\) often locked | \(x_3\) drift hurt |
| 4 | EI; keep \(x_3 < 0.5\) safe band | Discipline |
| 5 | EI + **manual \(x_3\) lock ≈ 0.401** | Override pipeline drift |
| 6 | Hold lock; refine \(x_1,x_2\) | **Best −0.011** |
| 7–9 | Protect W6; safe-band micro only | Hold |
| 10–12 | Exact-neighbour of −0.011; \(x_3\) locked | Hold |
| 13 | Locked: `0.492580-0.691590-0.401000` | Portal \(y\) pending |

**Incumbent:** \(y = -0.011366\) at `[0.492581, 0.691593, 0.401000]` (≈ Week 6).

**Detail:** [`data/function_3/EXPLANATION_F3.md`](data/function_3/EXPLANATION_F3.md) · `analysis_F3.png`

---

## 7. F4 — Warehouse (4D)

### Structures & hyperparameters

| Item | Setting |
|------|---------|
| Task | Multimodal warehouse efficiency |
| Dim / seed | 4D · `n_init` = 30 |
| Profile | `multimodal` |
| `gp_alpha` | 1e−4 |
| Matérn `nu` | default 2.5 |
| Notebook AF | **UCB** κ ≈ 2.5 |
| Practice AF | High-κ UCB early → **local EI** + trust region late |
| **Special structure** | Shrinking **trust-region micro-steps** once basin proven |
| **AF effect here** | High-κ UCB found a basin (paid with bad samples); local EI produced the late 0.47→0.68 climb |

### Weekly progress

| Week | Strategy / structure used | Outcome note |
|------|---------------------------|--------------|
| 1 | UCB κ≈3 multimodal explore | Escaped to ≈ **0.257** |
| 2 | High-κ UCB | Exploration cost (deep negatives) |
| 3–5 | Lower κ / local ± around positive basin | Basin forming |
| 6 | UCB basin exploit | Jump ≈ **0.470** |
| 7–8 | Local exploit in W6 basin | W8 ≈ **0.572** |
| 9 | Tight exploit after signal | ≈ **0.642** |
| 10 | Trust-region micro | ≈ **0.667** |
| 11 | Local cluster micro | ≈ **0.675** |
| 12 | Micro from W11 | ≈ **0.679** |
| 13 | Locked: `0.405000-0.412000-0.354000-0.414000` | Portal \(y\) pending |

**Incumbent:** \(y = 0.678600\) (Week 12).

**Detail:** [`data/function_4/EXPLANATION_F4.md`](data/function_4/EXPLANATION_F4.md) · `analysis_F4.png`

---

## 8. F5 — Chemical yield (4D)

### Structures & hyperparameters

| Item | Setting |
|------|---------|
| Task | Maximise reaction yield (ridge) |
| Dim / seed | 4D · `n_init` = 20 |
| Profile | `unimodal` |
| `gp_alpha` | 1e−6 |
| **`log_transform_y`** | **True** (from Week 3) |
| Notebook AF | UCB explore κ=2.576 → UCB exploit κ=0.5 when \(y\) > `signal_thr` = 2000 |
| Practice AF | Shifted to **EI + log-\(y\)** once ridge found |
| **Special structure** | Lock high face \(x_2=x_3=x_4=0.98\); climb **\(x_1\)** only |
| **AF effect here** | UCB/threshold opened the yield jump; log-y EI + face lock reduced AF to a 1D \(x_1\) ridge walk |

### Weekly progress

| Week | Strategy / structure used | Outcome note |
|------|---------------------------|--------------|
| 1 | UCB → signal-threshold exploit | ≈ **2497** |
| 2 | Aggressive exploit mis-step | Dip ≈ 1811 |
| 3 | **EI + log-\(y\)**; bound \(x_1\) | ≈ **3108** |
| 4 | High-face lock; \(x_1\)→**0.38** | ≈ **3744** |
| 5–6 | Ridge walk; some \(x_1\) too low | Protect / adjust |
| 7 | Return exact W4 ridge \(x_1=0.38\) | Re-confirm 3744 |
| 8 | Flagship: first probe **\(x_1>0.38\)** | ≈ **3760** |
| 9 | Continue \(x_1=0.41\) | Climb |
| 10 | \(x_1=0.42\) | ≈ **3779** |
| 11 | \(x_1=0.43\) | ≈ **3790** |
| 12 | \(x_1=0.44\) | ≈ **3801** |
| 13 | Locked: `0.450000-0.980000-0.980000-0.980000` | Portal \(y\) pending |

**Incumbent:** \(y = 3800.74\) at `[0.44, 0.98, 0.98, 0.98]` — clearest sustained success (seed ~1089 → ~3801).

**Detail:** [`data/function_5/EXPLANATION_F5.md`](data/function_5/EXPLANATION_F5.md) · `analysis_F5.png`

---

## 9. F6 — Cake recipe (5D)

### Structures & hyperparameters

| Item | Setting |
|------|---------|
| Task | Five ingredients; nearer zero better |
| Dim / seed | 5D · `n_init` = 20 |
| Profile | `negative` |
| `gp_alpha` | 1e−6 |
| Matérn `nu` | default 2.5 |
| AF | **EI** throughout |
| **Special structures** | Interior policy (avoid edges) · **hard-return** to W10 centroid after W11 collapse |
| **AF effect here** | EI improved to −0.136; after W11 miss, hard-return overrides EI’s too-wide local proposal |

### Weekly progress

| Week | Strategy / structure used | Outcome note |
|------|---------------------------|--------------|
| 1 | EI | ≈ **−0.478** |
| 2–4 | EI + boundary penalty | Edge hits hurt (esp. W4) |
| 5 | EI **interior** exploit | ≈ **−0.265** |
| 6–7 | Interior local EI | ≈ **−0.240** |
| 8–9 | Local EI; retract after miss | Fragile basin |
| 10 | Micro toward improved centroid | **Best −0.136** |
| 11 | “Next to” W10 centroid | Collapse ≈ **−0.372** |
| 12 | **Hard-return** toward W10 | Partial ≈ −0.205 |
| 13 | Locked: `0.441200-0.249200-0.590800-0.728700-0.131200` | Portal \(y\) pending |

**Incumbent:** \(y = -0.136\) (Week 10) at `[0.441, 0.249, 0.591, 0.729, 0.131]`.

**Detail:** [`data/function_6/EXPLANATION_F6.md`](data/function_6/EXPLANATION_F6.md) · `analysis_F6.png`

---

## 10. F7 — Hyperparameter tuning (6D)

### Structures & hyperparameters

| Item | Setting |
|------|---------|
| Task | Six ML training knobs |
| Dim / seed | 6D · `n_init` = 30 |
| Profile | `high_dim` |
| `gp_alpha` | 1e−6 |
| Matérn `nu` | default 2.5 |
| AF | **EI** throughout |
| **Special structures** | Soft **boundary penalty** · degenerate lock on flat dims · late **ARD-sensitive micro-steps** only |
| **AF effect here** | EI + locking flat dims keeps acquisition on sensitive axes → slow compound late gains |

### Weekly progress

| Week | Strategy / structure used | Outcome note |
|------|---------------------------|--------------|
| 1–2 | EI (explore-lean W2) | ≈ 1.45 |
| 3 | Soft boundary on free dims | ≈ **1.525** |
| 4 | EI local refine | ≈ **1.857** (long plateau starts) |
| 5–8 | Local EI; prefer \(x_1≈0.07\) not edge 0.02 | Hold / tiny moves |
| 9 | Tiny offset toward incumbent | Protect |
| 10 | Trust-region micro | ≈ **1.863** |
| 11 | Micro in cluster (ARD lens) | ≈ **1.866** |
| 12 | Micro from W11 | ≈ **1.872** |
| 13 | Locked: `0.074000-0.424000-0.299000-0.158000-0.346000-0.672000` | Portal \(y\) pending |

**Incumbent:** \(y = 1.872233\) (Week 12).

**Detail:** [`data/function_7/EXPLANATION_F7.md`](data/function_7/EXPLANATION_F7.md) · `analysis_F7.png`

---

## 11. F8 — Eight-parameter ML (8D)

### Structures & hyperparameters

| Item | Setting |
|------|---------|
| Task | Highest-dimensional ML score |
| Dim / seed | 8D · `n_init` = 40 |
| Profile | `high_dim` |
| `gp_alpha` | 1e−5 |
| Matérn `nu` | **1.5** |
| AF | **UCB** κ = 2.576 early → **κ ≈ 1.5** light exploit from Week 5 |
| **Special structures** | **Boundary penalty** · degenerate locks · trust-region ticks on sensitive axes only |
| **AF effect here** | High-κ UCB explores 8D; lowering κ ≈1.5 turns AF into slow ticks instead of edge-σ chase |

### Weekly progress

| Week | Strategy / structure used | Outcome note |
|------|---------------------------|--------------|
| 1–4 | UCB κ≈2.576 + boundary penalty | ≈ **9.796** early |
| 5 | Light exploit κ≈1.5 | ≈ **9.864** |
| 6–7 | Light exploit from incumbent | ≈ **9.865** |
| 8 | New vector (not clone); avoid bad edge | ≈ **9.868** |
| 9 | Tight exploit after signal | Climb |
| 10 | Light exploit micro | ≈ **9.871** |
| 11 | Plateau micro | ≈ **9.872** |
| 12 | Micro from W11 | ≈ **9.873** |
| 13 | Locked: `0.144000-0.060000-0.210000-0.050000-0.414000-0.510000-0.216000-0.917000` | Portal \(y\) pending |

**Incumbent:** \(y = 9.872928\) (Week 12) — slow ~0.001 ticks late.

**Detail:** [`data/function_8/EXPLANATION_F8.md`](data/function_8/EXPLANATION_F8.md) · `analysis_F8.png`

---

## 12. Late policy (Weeks 10–13)

| Mode | Functions | Action |
|------|-----------|--------|
| Signal-lobe micro | F1 | Stay ~0.64 / 0.68; trust gate still respected |
| Hard return | F2, F3, F6 | Historical / W10 best neighbourhood |
| Trust-region micro | F4, F7, F8 | Tiny offsets from latest incumbent |
| Ridge continue | F5 | High face locked; \(x_1\) 0.44 → 0.45 |

**Late improve counts:** W8 3/8 · W9 4/8 · W10 **5/8** · W11 4/8 · W12 4/8 (F4, F5, F7, F8).

Full Week-13 block + rationale: [`weeks/WEEK13_STRATEGY.md`](weeks/WEEK13_STRATEGY.md).

---

## 13. Week file index

| Week | Strategy | Reflection |
|------|----------|------------|
| 1–9 | [`weeks/WEEK*_STRATEGY.md`](weeks/) | [`WEEK*_REFLECTION.md`](weeks/) |
| 10 | [`WEEK10_STRATEGY.md`](weeks/WEEK10_STRATEGY.md) | [`WEEK10_REFLECTION.md`](weeks/WEEK10_REFLECTION.md) — **5/8** |
| 11 | [`WEEK11_STRATEGY.md`](weeks/WEEK11_STRATEGY.md) | [`WEEK11_REFLECTION.md`](weeks/WEEK11_REFLECTION.md) — 4/8 |
| 12 | [`WEEK12_STRATEGY.md`](weeks/WEEK12_STRATEGY.md) | [`WEEK12_REFLECTION.md`](weeks/WEEK12_REFLECTION.md) — 4/8 |
| 13 | [`WEEK13_STRATEGY.md`](weeks/WEEK13_STRATEGY.md) | portal \(y\) pending |

Folder guide: [`weeks/README.md`](weeks/README.md).

---

## Related root documents

| File | Role |
|------|------|
| [`README.md`](README.md) | Project home |
| [`STRATEGY.md`](STRATEGY.md) | **This file** — structures, hyperparameters, weekly progress |
| [`DATASHEET.md`](DATASHEET.md) | Dataset transparency |
| [`MODEL_CARD.md`](MODEL_CARD.md) | Method transparency |
| [`docs/COURSE_INDEX.md`](docs/COURSE_INDEX.md) | Course activity map |

*Version: v3 — adds AF formulas, choice→effect tables, and per-function AF-effect notes. Update best-\(y\) cells when portal results arrive.*
