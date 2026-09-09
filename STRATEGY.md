# STRATEGY.md â€” Per-function structures, hyperparameters & weekly progress

Imperial College London Â· PCMLAI Stage 2 Â· Black-Box Bayesian Optimisation  
**Same level as** [`README.md`](README.md) **and** [`DATASHEET.md`](DATASHEET.md) â€” this is the main strategy document for the repository.

| | |
|--|--|
| **Author** | Erkan Keskin Â· Neuroxa-Labs |
| **Status** | Weeks 1â€“12 complete Â· Week 13 queries locked Â· portal \(y\) pending |
| **Code source of truth** | [`notebooks/BBO_Capstone_Optimized.ipynb`](notebooks/BBO_Capstone_Optimized.ipynb) â€” `FUNCTIONS`, `STRATEGY`, `GP_CONFIG` |
| **Weekly detail files** | [`weeks/WEEK*_STRATEGY.md`](weeks/) (portal strings + that weekâ€™s rationale) |
| **Evidence pack** | [`docs/final_report.md`](docs/final_report.md) Â· [`docs/final_report.pdf`](docs/final_report.pdf) |

This file answers, **for every function**: what structures we used, which hyperparameters / locks applied, how acquisition-function (AF) choices behaved, and how the approach progressed week by week.

**Not in scope:** recovering a closed-form \(f(x)\). The portal is a black box; we only ever observe \((x,y)\). The GP supplies a **surrogate** \(\mu(x),\sigma(x)\), not the true formula.

---

## Contents

1. [Shared pipeline & global hyperparameters](#1-shared-pipeline--global-hyperparameters)
2. [Acquisition functions â€” formulas & effects](#2-acquisition-functions--formulas--effects)
3. [Quick map (all eight)](#3-quick-map-all-eight)
4. [F1 â€” Radiation](#4-f1--radiation-source-2d)
5. [F2 â€” Noisy ML](#5-f2--noisy-ml-score-2d)
6. [F3 â€” Drug / adverse](#6-f3--drug--adverse-3d)
7. [F4 â€” Warehouse](#7-f4--warehouse-4d)
8. [F5 â€” Chemical yield](#8-f5--chemical-yield-4d)
9. [F6 â€” Cake recipe](#9-f6--cake-recipe-5d)
10. [F7 â€” HP tuning](#10-f7--hyperparameter-tuning-6d)
11. [F8 â€” 8-param ML](#11-f8--eight-parameter-ml-8d)
12. [Late policy (W10â€“13)](#12-late-policy-weeks-1013)
13. [Week file index](#13-week-file-index)

---

## 1. Shared pipeline & global hyperparameters

### Structure (every function)

```text
history (x, y)
    â†’ MatÃ©rn GP + ARD length scales (multi-restart LML)
    â†’ acquisition score (EI or UCB; F1 may use uncertainty / coverage)
    â†’ candidate search (global + local / trust region)
    â†’ per-function locks, trust gate, boundary penalty, anti-duplicate
    â†’ one six-decimal portal string
    â†’ append portal y â†’ next week
```

Neural nets / Optuna / TuRBO were **not** the primary weekly portal decider. The GP remained the core structure; weekly files record tactical changes around that core.

### Global `GP_CONFIG` (notebook defaults)

| Hyperparameter | Value | Meaning |
|----------------|------:|---------|
| Kernel family | MatÃ©rn + ARD | Independent length scale per dimension |
| `nu` (default) | 2.5 | Smoothness (overridden on F1 / F3 / F8) |
| `n_restarts_optimizer` | 10 | Restarts for length-scale fit |
| `normalize_y` | True | Standardise \(y\) before GP fit |
| `length_scale_bounds` | (1eâˆ’2, 10) | ARD search box |
| `degenerate_threshold` | 8.0 | Large LS â†’ lock that dimension to incumbent |
| `boundary_buffer` | 0.02 | Soft keep-away from \([0,1]\) edges |
| `boundary_penalty_weight` | 0.5 | Penalty weight on near-edge candidates |
| `local_explore_radius` | 0.15 | Default local / trust-region radius |
| `sensitive_ls_thr` | 0.2 | Small LS â†’ â€œmove carefullyâ€ |
| `sensitive_bound_k` | 2.5 | Local bound â‰ˆ \(k \times\) length scale |
| `sensitive_bound_min_radius` | 0.08 | Floor on that local bound |

### Calendar phases (guideline, overridden per function when needed)

| Phase | Weeks | Intent |
|-------|-------|--------|
| Explore | 1â€“4 | Map basins, coverage, avoid premature lock |
| Balanced | 5â€“9 | Exploit where signal exists; keep options open |
| Exploit | 10â€“13 | Trust-region micro-steps, hard-return, ridge continue |

---

## 2. Acquisition functions â€” formulas & effects

Portal black box: unknown map **f : [0,1]áµˆ â†’ â„**. We do **not** recover a closed form for **f**.  
We only observe pairs **(x, y)** with **y = f(x)**, fit a Gaussian process, and pick the next **x** by maximising an acquisition score **a(x)**.

Notation used below:

| Symbol | Meaning |
|--------|---------|
| **x** | candidate input in [0,1]áµˆ |
| **y** | portal score (= f(x), unknown formula) |
| **yâ˜…** | best score seen so far (incumbent) |
| **Î¼â‚™(x)** | GP predictive mean at **x** after n points |
| **Ïƒâ‚™(x)** | GP predictive standard deviation at **x** |
| **â„“â±¼** | ARD length scale for dimension j |
| **Îº** | UCB exploration weight |
| **Ï†, Î¦** | standard normal pdf and cdf |

---

### 2.1 Gaussian process posterior

After data Dâ‚™ = {(xáµ¢, yáµ¢)}áµ¢â‚Œâ‚â€¦â‚™:

> **f(x) | Dâ‚™  ~  ð’©( Î¼â‚™(x) , Ïƒâ‚™Â²(x) )**

Meaning: at any new **x**, the modelâ€™s belief about **f(x)** is a normal distribution with mean **Î¼â‚™** and variance **Ïƒâ‚™Â²**. Acquisition functions are built only from **Î¼â‚™** and **Ïƒâ‚™**, never from a known formula for **f**.

Next query (before locks / penalties):

> **xâ‚™â‚Šâ‚  =  arg max_{x âˆˆ [0,1]áµˆ}  a(x)**

---

### 2.2 MatÃ©rn kernel with ARD (what the GP uses)

Smoothness parameter **Î½**; signal variance **Ïƒ_fÂ²**; per-dimension length scales **â„“â‚,â€¦,â„“_d**.

Distance with ARD:

> **r  =  âˆš[ Î£â±¼â‚Œâ‚áµˆ  ((xâ±¼ âˆ’ xâ€²â±¼) / â„“â±¼)Â² ]**

MatÃ©rn covariance:

> **k(x, xâ€²)  =  Ïƒ_fÂ² Â· (2^{1âˆ’Î½} / Î“(Î½)) Â· (âˆš(2Î½) Â· r)^Î½ Â· K_Î½(âˆš(2Î½) Â· r)**

where **Î“** is the gamma function and **K_Î½** is the modified Bessel function of the second kind.

**What this means.** Small **â„“â±¼** â‡’ dimension j is sensitive (small moves change **y** a lot). Large **â„“â±¼** â‡’ flat / less important (we often lock that coordinate).

Extras in this project:

- **F2:** add WhiteKernel noise â†’ **k(x,xâ€²) + Ïƒ_ÎµÂ²** when **x = xâ€²** (noisy observations).
- **F5:** fit the GP on **log y**, then use the predictive surface for acquisition.

Default **Î½ = 2.5**; overrides: F1 **Î½ = 0.5**, F3/F8 **Î½ = 1.5**.

---

### 2.3 Expected Improvement (EI)

Improvement random variable:

> **I(x)  =  max( 0 , f(x) âˆ’ yâ˜… )**

Acquisition (expectation under the GP):

> **a_EI(x)  =  E[ I(x) | Dâ‚™ ]  =  E[ max(0, f(x) âˆ’ yâ˜…) | Dâ‚™ ]**

Closed form with **Î¼â‚™**, **Ïƒâ‚™**:

> **z  =  (Î¼â‚™(x) âˆ’ yâ˜…) / Ïƒâ‚™(x)**

> **a_EI(x)  =  (Î¼â‚™(x) âˆ’ yâ˜…) Â· Î¦(z)  +  Ïƒâ‚™(x) Â· Ï†(z)**   when **Ïƒâ‚™(x) > 0**

> **a_EI(x)  =  max(0, Î¼â‚™(x) âˆ’ yâ˜…)**   when **Ïƒâ‚™(x) = 0**

**Effect of choosing EI.**  
Pushes toward points that can beat **yâ˜…**. The term **Ïƒâ‚™Â·Ï†(z)** is the exploration piece; there is no separate **Îº**.  
In this project: found F2â€™s ridge (**y â‰ˆ 0.777**); also caused some â€œnearbyâ€ misses on sharp ridges (F2 W6, F6 W11) â†’ we overrode with hard-return.

---

### 2.4 Upper Confidence Bound (UCB)

> **a_UCB(x)  =  Î¼â‚™(x)  +  Îº Â· Ïƒâ‚™(x)**    with **Îº > 0**

**Effect of Îº.**

- **Large Îº** (â‰ˆ 2.5â€“3; F1 explore Îº = 3): chase uncertainty â†’ more exploration, can find new basins (F4 early) but also burn queries on bad regions (F4 W2).
- **Small Îº** (â‰ˆ 0.5â€“1.5 late): trust the mean â†’ local climb (F8 slow ticks; F5 exploit). If **Î¼â‚™** is wrong, it reinforces a bad neighbourhood.

Settings we used: **Îº = 2.576** on F3/F8 explore; **Îº â‰ˆ 1.5** light exploit on F8.

---

### 2.5 Uncertainty sampling (pure Ïƒ)

> **a_Ïƒ(x)  =  Ïƒâ‚™(x)**  
> (same idea: maximise predictive variance **Ïƒâ‚™Â²(x)**)

**Effect.** Ignores **Î¼â‚™**; spreads queries into unknown regions. Used on **F1** while almost all labels were ~0, so that exploiting **Î¼â‚™** would invent fake peaks (trust gate).

---

### 2.6 Coverage / space-fill (when GP is untrusted)

With past points {xáµ¢} and optional boundary penalty **P(x)**:

> **a_cov(x)  =  mináµ¢ â€–x âˆ’ xáµ¢â€–â‚‚  âˆ’  Î» Â· P(x)**

**Effect.** Geometric coverage of the box when **Î¼â‚™ / Ïƒâ‚™** are not trusted (F1 trust-gate weeks). Does not raise **y** by itself; prepares for a later exploit mode.

---

### 2.7 Decision rule used in the notebook

> **xâ‚™â‚Šâ‚  =  arg max_{x âˆˆ X_feasible}  [ a(x) âˆ’ Î»_bound Â· P_bound(x) ]**

**X_feasible** may: lock flat ARD dimensions, freeze coordinates (F3 **xâ‚ƒ**, F5 high face **xâ‚‚=xâ‚ƒ=xâ‚„=0.98**), stay inside a trust region around the incumbent, or â€” under the F1 trust gate â€” refuse exploit-style **a** until a real signal lobe appears.

---

### 2.8 Effects summary (which AF â†’ what happened)

| Choice | Behaviour | Upside we saw | Downside we saw |
|--------|-----------|---------------|-----------------|
| EI | Beat **yâ˜…** vs **Ïƒâ‚™** | F2 ridge; F6/F7 local gains | F2 overshoot; F6 off-centroid miss |
| UCB, high **Îº** | Pull to high **Ïƒâ‚™** | F4 basin; F3/F8 map | F4 deep negatives |
| UCB, low **Îº** | Stay near high **Î¼â‚™** | F8 ticks; F5 exploit | Wrong **Î¼â‚™** can stick |
| **a_Ïƒ** / coverage | Fill space | F1 null-map safety | Does not raise **y** alone |
| Switch EI â†” UCB | Re-aim after structure | F3/F4/F5 exploreâ†’exploit | Switch timing matters |

| Fn | AF path | Practical effect |
|----|---------|------------------|
| F1 | **a_Ïƒ** / coverage â†’ trust gate â†’ lobe micro | No fake null-map exploit; late local geometry |
| F2 | EI + WhiteKernel | Found **yâ‰ˆ0.777**; later hard-return after EI misses |
| F3 | UCB (**Îºâ‰ˆ2.576**) â†’ EI + **xâ‚ƒ** lock | Map risk, then safe-band refine |
| F4 | High-**Îº** UCB â†’ local EI | Basin then climb **0.47 â†’ 0.68** |
| F5 | UCB + threshold â†’ EI on **log y** + face lock | Yield jump then 1-D walk on **xâ‚** |
| F6 | EI + interior penalty | To **âˆ’0.136**; then hard-return |
| F7 | EI + ARD locks | Steady gains on sensitive axes only |
| F8 | UCB **Îºâ‰ˆ2.576 â†’ 1.5** | Map then slow **~0.001** ticks |

**Takeaway.** These are the **scoring formulas**. The unknown portal **f(x)** stays unknown; we only ever update **Î¼â‚™, Ïƒâ‚™** from observed **(x, y)**. Locks / trust regions / hard-return stop **a(x)** from acting on a wrong GP belief.

---

## 3. Quick map (all eight)

| Fn | \(d\) | Seed `n_init` | Profile | Key structures | Best \(y\) (W12) |
|----|------:|--------------:|---------|----------------|------------------|
| F1 | 2 | 10 | sparse_peak | Trust gate Â· coverage Â· late lobe micro | 7.711Ã—10â»Â¹â¶ |
| F2 | 2 | 10 | noisy | WhiteKernel Â· EI Â· hard-return | 0.776645 |
| F3 | 3 | 15 | negative | UCBâ†’EI Â· \(x_3\) lock â‰ˆ0.401 | âˆ’0.011366 |
| F4 | 4 | 30 | multimodal | UCBâ†’local EI Â· trust-region micro | 0.678600 |
| F5 | 4 | 20 | unimodal | log-\(y\) Â· high-face lock Â· \(x_1\) climb | 3800.74 |
| F6 | 5 | 20 | negative | EI Â· interior Â· hard-return to W10 | âˆ’0.136 |
| F7 | 6 | 30 | high_dim | EI Â· boundary soft Â· ARD micro | 1.872233 |
| F8 | 8 | 40 | high_dim | UCB Â· boundary Â· ARD micro | 9.872928 |

---

## 4. F1 â€” Radiation source (2D)

### Structures & hyperparameters

| Item | Setting |
|------|---------|
| Task | Locate hidden radiation source; most map ~0 |
| Dim / seed | 2D Â· `n_init` = 10 |
| Profile | `sparse_peak` |
| `gp_alpha` | 1eâˆ’12 |
| MatÃ©rn `nu` | **0.5** (rougher than global 2.5) |
| Notebook AF | Explore: **uncertainty** Â· Exploit: **UCB** (`kappa_expl` = 3.0) |
| `signal_thr` | 1eâˆ’4 |
| WhiteKernel / log-\(y\) | No |
| **Special structure** | **Trust gate** â€” refuse GP exploit while labels are ~null |
| **AF effect here** | Uncertainty/coverage stops null-map â€œfake peaksâ€; after W10 lobe, queries are lobe micro-steps (AF not free to roam) |

### Weekly progress

| Week | Strategy / structure used | Outcome note |
|------|---------------------------|--------------|
| 1 | Uncertainty / pure exploration | All ~null; no usable signal |
| 2â€“3 | Coverage + boundary penalty; interior probes | Still ~null |
| 4â€“5 | Random / coverage grid (â‰¥10% from past) | Still no signal |
| 6 | Manual refine near warm seed `[0.731, 0.733]` | Seed null remains â€œbestâ€ |
| 7 | Soft-signal heuristics (log10 ranking / SVM / IF) | Warm UR band probe |
| 8â€“9 | **Trust gate on** â€” GP exploit refused; space-fill | No false exploit |
| 10 | Pivot to peer-informed lobe **~0.64 / 0.68** | First measurable: â‰ˆ âˆ’0.008 |
| 11 | Tight exploit in confirmed lobe | â‰ˆ âˆ’0.006 |
| 12 | Signal-lobe micro-step | â‰ˆ âˆ’0.005 |
| 13 | Locked: `0.635000-0.688000` | Portal \(y\) pending |

**Incumbent (official max):** \(y = 7.711\times10^{-16}\) at `[0.731024, 0.733000]` (seed) â€” never beaten. Late lobe is the first **usable basin**, not the absolute max.

**Detail:** [`data/function_1/EXPLANATION_F1.md`](data/function_1/EXPLANATION_F1.md) Â· `analysis_F1.png`

---

## 5. F2 â€” Noisy ML score (2D)

### Structures & hyperparameters

| Item | Setting |
|------|---------|
| Task | Two ML knobs; noisy log-likelihood |
| Dim / seed | 2D Â· `n_init` = 10 |
| Profile | `noisy` |
| `gp_alpha` | 1eâˆ’8 |
| MatÃ©rn `nu` | default 2.5 |
| **WhiteKernel** | **True** (noise model) |
| AF | **EI** throughout |
| **Special structure** | Sharp ridge + **hard-return** after neighbour misses |
| **AF effect here** | EI discovered the W5 ridge; the same EI later proposed unsafe neighbours â†’ hard-return overrides AF |

### Weekly progress

| Week | Strategy / structure used | Outcome note |
|------|---------------------------|--------------|
| 1â€“3 | EI; noise-aware; donâ€™t abandon on one bad draw | Building ridge map |
| 4 | Manual low-\(x_2\) peak test | Best â‰ˆ **0.660** |
| 5 | EI exploit high-\(x_1\) / low-\(x_2\) | **Record 0.777** at `[0.717869, 0.020000]` |
| 6 | EI overshoot (\(x_1\)â‰ˆ0.75) | Collapse â‰ˆ 0.403 |
| 7â€“8 | Return toward W5 ridge; probe left of â€œcliffâ€ | Ridge fragile |
| 9 | Tiny offset toward incumbent (no exact replay) | Protect peak |
| 10 | Toward historical 0.777 | Partial |
| 11 | Neighbour toward centroid | Miss â‰ˆ 0.548 |
| 12 | **Hard-return** tighter to `[0.7179, 0.02]` | Protect |
| 13 | Locked: `0.717870-0.020000` | Portal \(y\) pending |

**Incumbent:** \(y = 0.776645\) (Week 5) â€” held; never reclaimed after misses.

**Detail:** [`data/function_2/EXPLANATION_F2.md`](data/function_2/EXPLANATION_F2.md) Â· `analysis_F2.png`

---

## 6. F3 â€” Drug / adverse (3D)

### Structures & hyperparameters

| Item | Setting |
|------|---------|
| Task | Three mixture ratios; nearer zero = safer |
| Dim / seed | 3D Â· `n_init` = 15 |
| Profile | `negative` |
| `gp_alpha` | 1eâˆ’6 |
| MatÃ©rn `nu` | **1.5** |
| Notebook AF | **UCB** Îº = 2.576 (early); practice shifted to **EI** + locks mid-project |
| **Special structure** | **Safe \(x_3\) lock â‰ˆ 0.401** (from Week 5) |
| Data note | 11 weekly rows in `data/` (no fabricated W12 point) |
| **AF effect here** | UCB mapped \(x_3\) risk; EI+lock converted AF into safe-band refine (without lock, AF drifted \(x_3\)) |

### Weekly progress

| Week | Strategy / structure used | Outcome note |
|------|---------------------------|--------------|
| 1 | UCB explore; \(x_3\) already sensitive | Mapping |
| 2 | UCB + narrow bounds on \(x_3\) | Best â‰ˆ **âˆ’0.020** |
| 3 | Local bounds; \(x_2\) often locked | \(x_3\) drift hurt |
| 4 | EI; keep \(x_3 < 0.5\) safe band | Discipline |
| 5 | EI + **manual \(x_3\) lock â‰ˆ 0.401** | Override pipeline drift |
| 6 | Hold lock; refine \(x_1,x_2\) | **Best âˆ’0.011** |
| 7â€“9 | Protect W6; safe-band micro only | Hold |
| 10â€“12 | Exact-neighbour of âˆ’0.011; \(x_3\) locked | Hold |
| 13 | Locked: `0.492580-0.691590-0.401000` | Portal \(y\) pending |

**Incumbent:** \(y = -0.011366\) at `[0.492581, 0.691593, 0.401000]` (â‰ˆ Week 6).

**Detail:** [`data/function_3/EXPLANATION_F3.md`](data/function_3/EXPLANATION_F3.md) Â· `analysis_F3.png`

---

## 7. F4 â€” Warehouse (4D)

### Structures & hyperparameters

| Item | Setting |
|------|---------|
| Task | Multimodal warehouse efficiency |
| Dim / seed | 4D Â· `n_init` = 30 |
| Profile | `multimodal` |
| `gp_alpha` | 1eâˆ’4 |
| MatÃ©rn `nu` | default 2.5 |
| Notebook AF | **UCB** Îº â‰ˆ 2.5 |
| Practice AF | High-Îº UCB early â†’ **local EI** + trust region late |
| **Special structure** | Shrinking **trust-region micro-steps** once basin proven |
| **AF effect here** | High-Îº UCB found a basin (paid with bad samples); local EI produced the late 0.47â†’0.68 climb |

### Weekly progress

| Week | Strategy / structure used | Outcome note |
|------|---------------------------|--------------|
| 1 | UCB Îºâ‰ˆ3 multimodal explore | Escaped to â‰ˆ **0.257** |
| 2 | High-Îº UCB | Exploration cost (deep negatives) |
| 3â€“5 | Lower Îº / local Â± around positive basin | Basin forming |
| 6 | UCB basin exploit | Jump â‰ˆ **0.470** |
| 7â€“8 | Local exploit in W6 basin | W8 â‰ˆ **0.572** |
| 9 | Tight exploit after signal | â‰ˆ **0.642** |
| 10 | Trust-region micro | â‰ˆ **0.667** |
| 11 | Local cluster micro | â‰ˆ **0.675** |
| 12 | Micro from W11 | â‰ˆ **0.679** |
| 13 | Locked: `0.405000-0.412000-0.354000-0.414000` | Portal \(y\) pending |

**Incumbent:** \(y = 0.678600\) (Week 12).

**Detail:** [`data/function_4/EXPLANATION_F4.md`](data/function_4/EXPLANATION_F4.md) Â· `analysis_F4.png`

---

## 8. F5 â€” Chemical yield (4D)

### Structures & hyperparameters

| Item | Setting |
|------|---------|
| Task | Maximise reaction yield (ridge) |
| Dim / seed | 4D Â· `n_init` = 20 |
| Profile | `unimodal` |
| `gp_alpha` | 1eâˆ’6 |
| **`log_transform_y`** | **True** (from Week 3) |
| Notebook AF | UCB explore Îº=2.576 â†’ UCB exploit Îº=0.5 when \(y\) > `signal_thr` = 2000 |
| Practice AF | Shifted to **EI + log-\(y\)** once ridge found |
| **Special structure** | Lock high face \(x_2=x_3=x_4=0.98\); climb **\(x_1\)** only |
| **AF effect here** | UCB/threshold opened the yield jump; log-y EI + face lock reduced AF to a 1D \(x_1\) ridge walk |

### Weekly progress

| Week | Strategy / structure used | Outcome note |
|------|---------------------------|--------------|
| 1 | UCB â†’ signal-threshold exploit | â‰ˆ **2497** |
| 2 | Aggressive exploit mis-step | Dip â‰ˆ 1811 |
| 3 | **EI + log-\(y\)**; bound \(x_1\) | â‰ˆ **3108** |
| 4 | High-face lock; \(x_1\)â†’**0.38** | â‰ˆ **3744** |
| 5â€“6 | Ridge walk; some \(x_1\) too low | Protect / adjust |
| 7 | Return exact W4 ridge \(x_1=0.38\) | Re-confirm 3744 |
| 8 | Flagship: first probe **\(x_1>0.38\)** | â‰ˆ **3760** |
| 9 | Continue \(x_1=0.41\) | Climb |
| 10 | \(x_1=0.42\) | â‰ˆ **3779** |
| 11 | \(x_1=0.43\) | â‰ˆ **3790** |
| 12 | \(x_1=0.44\) | â‰ˆ **3801** |
| 13 | Locked: `0.450000-0.980000-0.980000-0.980000` | Portal \(y\) pending |

**Incumbent:** \(y = 3800.74\) at `[0.44, 0.98, 0.98, 0.98]` â€” clearest sustained success (seed ~1089 â†’ ~3801).

**Detail:** [`data/function_5/EXPLANATION_F5.md`](data/function_5/EXPLANATION_F5.md) Â· `analysis_F5.png`

---

## 9. F6 â€” Cake recipe (5D)

### Structures & hyperparameters

| Item | Setting |
|------|---------|
| Task | Five ingredients; nearer zero better |
| Dim / seed | 5D Â· `n_init` = 20 |
| Profile | `negative` |
| `gp_alpha` | 1eâˆ’6 |
| MatÃ©rn `nu` | default 2.5 |
| AF | **EI** throughout |
| **Special structures** | Interior policy (avoid edges) Â· **hard-return** to W10 centroid after W11 collapse |
| **AF effect here** | EI improved to âˆ’0.136; after W11 miss, hard-return overrides EIâ€™s too-wide local proposal |

### Weekly progress

| Week | Strategy / structure used | Outcome note |
|------|---------------------------|--------------|
| 1 | EI | â‰ˆ **âˆ’0.478** |
| 2â€“4 | EI + boundary penalty | Edge hits hurt (esp. W4) |
| 5 | EI **interior** exploit | â‰ˆ **âˆ’0.265** |
| 6â€“7 | Interior local EI | â‰ˆ **âˆ’0.240** |
| 8â€“9 | Local EI; retract after miss | Fragile basin |
| 10 | Micro toward improved centroid | **Best âˆ’0.136** |
| 11 | â€œNext toâ€ W10 centroid | Collapse â‰ˆ **âˆ’0.372** |
| 12 | **Hard-return** toward W10 | Partial â‰ˆ âˆ’0.205 |
| 13 | Locked: `0.441200-0.249200-0.590800-0.728700-0.131200` | Portal \(y\) pending |

**Incumbent:** \(y = -0.136\) (Week 10) at `[0.441, 0.249, 0.591, 0.729, 0.131]`.

**Detail:** [`data/function_6/EXPLANATION_F6.md`](data/function_6/EXPLANATION_F6.md) Â· `analysis_F6.png`

---

## 10. F7 â€” Hyperparameter tuning (6D)

### Structures & hyperparameters

| Item | Setting |
|------|---------|
| Task | Six ML training knobs |
| Dim / seed | 6D Â· `n_init` = 30 |
| Profile | `high_dim` |
| `gp_alpha` | 1eâˆ’6 |
| MatÃ©rn `nu` | default 2.5 |
| AF | **EI** throughout |
| **Special structures** | Soft **boundary penalty** Â· degenerate lock on flat dims Â· late **ARD-sensitive micro-steps** only |
| **AF effect here** | EI + locking flat dims keeps acquisition on sensitive axes â†’ slow compound late gains |

### Weekly progress

| Week | Strategy / structure used | Outcome note |
|------|---------------------------|--------------|
| 1â€“2 | EI (explore-lean W2) | â‰ˆ 1.45 |
| 3 | Soft boundary on free dims | â‰ˆ **1.525** |
| 4 | EI local refine | â‰ˆ **1.857** (long plateau starts) |
| 5â€“8 | Local EI; prefer \(x_1â‰ˆ0.07\) not edge 0.02 | Hold / tiny moves |
| 9 | Tiny offset toward incumbent | Protect |
| 10 | Trust-region micro | â‰ˆ **1.863** |
| 11 | Micro in cluster (ARD lens) | â‰ˆ **1.866** |
| 12 | Micro from W11 | â‰ˆ **1.872** |
| 13 | Locked: `0.074000-0.424000-0.299000-0.158000-0.346000-0.672000` | Portal \(y\) pending |

**Incumbent:** \(y = 1.872233\) (Week 12).

**Detail:** [`data/function_7/EXPLANATION_F7.md`](data/function_7/EXPLANATION_F7.md) Â· `analysis_F7.png`

---

## 11. F8 â€” Eight-parameter ML (8D)

### Structures & hyperparameters

| Item | Setting |
|------|---------|
| Task | Highest-dimensional ML score |
| Dim / seed | 8D Â· `n_init` = 40 |
| Profile | `high_dim` |
| `gp_alpha` | 1eâˆ’5 |
| MatÃ©rn `nu` | **1.5** |
| AF | **UCB** Îº = 2.576 early â†’ **Îº â‰ˆ 1.5** light exploit from Week 5 |
| **Special structures** | **Boundary penalty** Â· degenerate locks Â· trust-region ticks on sensitive axes only |
| **AF effect here** | High-Îº UCB explores 8D; lowering Îº â‰ˆ1.5 turns AF into slow ticks instead of edge-Ïƒ chase |

### Weekly progress

| Week | Strategy / structure used | Outcome note |
|------|---------------------------|--------------|
| 1â€“4 | UCB Îºâ‰ˆ2.576 + boundary penalty | â‰ˆ **9.796** early |
| 5 | Light exploit Îºâ‰ˆ1.5 | â‰ˆ **9.864** |
| 6â€“7 | Light exploit from incumbent | â‰ˆ **9.865** |
| 8 | New vector (not clone); avoid bad edge | â‰ˆ **9.868** |
| 9 | Tight exploit after signal | Climb |
| 10 | Light exploit micro | â‰ˆ **9.871** |
| 11 | Plateau micro | â‰ˆ **9.872** |
| 12 | Micro from W11 | â‰ˆ **9.873** |
| 13 | Locked: `0.144000-0.060000-0.210000-0.050000-0.414000-0.510000-0.216000-0.917000` | Portal \(y\) pending |

**Incumbent:** \(y = 9.872928\) (Week 12) â€” slow ~0.001 ticks late.

**Detail:** [`data/function_8/EXPLANATION_F8.md`](data/function_8/EXPLANATION_F8.md) Â· `analysis_F8.png`

---

## 12. Late policy (Weeks 10â€“13)

| Mode | Functions | Action |
|------|-----------|--------|
| Signal-lobe micro | F1 | Stay ~0.64 / 0.68; trust gate still respected |
| Hard return | F2, F3, F6 | Historical / W10 best neighbourhood |
| Trust-region micro | F4, F7, F8 | Tiny offsets from latest incumbent |
| Ridge continue | F5 | High face locked; \(x_1\) 0.44 â†’ 0.45 |

**Late improve counts:** W8 3/8 Â· W9 4/8 Â· W10 **5/8** Â· W11 4/8 Â· W12 4/8 (F4, F5, F7, F8).

Full Week-13 block + rationale: [`weeks/WEEK13_STRATEGY.md`](weeks/WEEK13_STRATEGY.md).

---

## 13. Week file index

| Week | Strategy | Reflection |
|------|----------|------------|
| 1â€“9 | [`weeks/WEEK*_STRATEGY.md`](weeks/) | [`WEEK*_REFLECTION.md`](weeks/) |
| 10 | [`WEEK10_STRATEGY.md`](weeks/WEEK10_STRATEGY.md) | [`WEEK10_REFLECTION.md`](weeks/WEEK10_REFLECTION.md) â€” **5/8** |
| 11 | [`WEEK11_STRATEGY.md`](weeks/WEEK11_STRATEGY.md) | [`WEEK11_REFLECTION.md`](weeks/WEEK11_REFLECTION.md) â€” 4/8 |
| 12 | [`WEEK12_STRATEGY.md`](weeks/WEEK12_STRATEGY.md) | [`WEEK12_REFLECTION.md`](weeks/WEEK12_REFLECTION.md) â€” 4/8 |
| 13 | [`WEEK13_STRATEGY.md`](weeks/WEEK13_STRATEGY.md) | portal \(y\) pending |

Folder guide: [`weeks/README.md`](weeks/README.md).

---

## Related root documents

| File | Role |
|------|------|
| [`README.md`](README.md) | Project home |
| [`STRATEGY.md`](STRATEGY.md) | **This file** â€” structures, hyperparameters, weekly progress |
| [`DATASHEET.md`](DATASHEET.md) | Dataset transparency |
| [`MODEL_CARD.md`](MODEL_CARD.md) | Method transparency |
| [`docs/COURSE_INDEX.md`](docs/COURSE_INDEX.md) | Course activity map |

*Version: v5 — AF formulas in Unicode symbols (readable on GitHub without LaTeX). Update best-y when portal results arrive.*
