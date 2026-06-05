# Week 1 Reflection — Black-Box Bayesian Optimisation

*Module 13 Capstone — reflecting on early results before refining the Week 2 strategy.*

## 1. Setup recap

We optimise **8 unknown black-box functions** (F1–F8, ranging from 2D to 8D). We never see the
function form — we send one query point `x` per week and receive a single output `y`, which we
add to our data and use to update the model. The pipeline uses a **Gaussian Process (GP)**
surrogate plus a per-function **acquisition function (AF)** to decide where to look next.

After Week 1, each function now has **11 data points** (10–40 initial samples + 1 new point).
This reflection asks one question for each function: *did our Week 1 choice teach us something,
and does it change what we should do next?*

## 2. Week 1 results at a glance

| Fn | Dim | Profile | AF used (Week 1) | Initial best | **Week 1 y** | Improved? |
|----|-----|---------|------------------|-------------:|-------------:|:---------:|
| F1 | 2 | Sparse peak (radiation) | UNCERTAINTY | 7.7e-16 | 4.8e-214 | ❌ no signal |
| F2 | 2 | Noisy log-likelihood | EI | 0.611 | 0.490 | ❌ |
| F3 | 3 | Negative (drug) | UCB κ=2.576 | −0.035 | −0.168 | ❌ |
| F4 | 4 | Multimodal (warehouse) | UCB κ=3.0 | −4.03 | **0.257** | ✅ big |
| F5 | 4 | Unimodal (chem. yield) | UCB → exploit | 1088.9 | **2497.3** | ✅ huge |
| F6 | 5 | Negative (cake) | EI | −0.714 | **−0.478** | ✅ |
| F7 | 6 | High-dim (HP tuning) | EI | 1.365 | **1.451** | ✅ |
| F8 | 8 | High-dim (8-param ML) | UCB κ=2.576 | 9.598 | **9.796** | ✅ |

**Score: 5 of 8 functions improved on the first query.** The three that did not (F1, F2, F3) each
tell a different — and useful — story.

## 3. What worked, and why

- **F5 — the standout (1089 → 2497, +129%).** This is a single broad peak. Once our data crossed
  the signal threshold, the strategy correctly flipped from exploration to **exploitation** and
  climbed the hill aggressively. This validates the "find the signal, then commit" logic.
- **F4 — escaped a bad region (−4.03 → +0.257).** The high exploration setting (UCB κ=3.0) was the
  right call for a multimodal landscape: it jumped out of a poor basin into a positive one.
- **F6, F7, F8 — steady, incremental gains.** EI (F6, F7) and high-dimensional UCB (F8) each
  produced small but real improvements. In high dimensions, modest steady progress is exactly what
  we expect — there is no shortcut through a large space.

## 4. What did not improve, and why it is still informative

- **F1 — still zero, and that is fine.** A sparse, sharp peak means ~99% of the space reads zero.
  A "0" is not a failure; it is **elimination** — we now know 11 locations where the source is
  *not*. Pure uncertainty (exploration) remains the only rational move until any non-zero reading
  appears. No change needed.
- **F2 — noise, not a bad choice (0.611 → 0.490).** This function is genuinely noisy, so a single
  lower reading does **not** mean the region is worse — it may just be a noisy draw. EI plus a
  noise (White) kernel is still appropriate; we should keep sampling near the promising region
  rather than abandoning it.
- **F3 — explored a worse spot (−0.035 → −0.168), as designed.** In an early exploration phase with
  high κ, occasionally landing on a worse point is expected: we are mapping the space, not yet
  exploiting. The information gained narrows future search.

## 5. Key lessons (the "thoughtful iteration" part)

1. **A worse `y` is still data.** F1, F2 and F3 did not "fail" — each return refined the GP's belief.
   In black-box optimisation, ruling regions out is progress.
2. **Match the AF to the function's nature, not a one-size-fits-all rule.** Pure exploration for
   sparse peaks (F1), noise-robust EI for noisy targets (F2/F6/F7), and tunable UCB where we need a
   controllable explore/exploit knob (F3/F4/F5/F8). This per-function design paid off.
3. **Signal detection should drive the explore→exploit switch, not just the calendar.** F5 proved
   this: it exploited as soon as it found signal, rather than waiting for a fixed week.
4. **Dimensionality sets expectations.** Low-dim functions (F2, F5) can converge fast; high-dim ones
   (F7, F8) need patience and sustained exploration.

## 6. Implications for Week 2 (handoff)

- **F1:** keep pure exploration — probe the largest uncovered gap; no change.
- **F2:** keep EI but refine *around* the known-good region (treat the dip as noise).
- **F3:** continue UCB exploration; the worse point was an expected exploration cost.
- **F4:** keep high-κ UCB — multimodal space still needs coverage, but begin tracking the new
  positive basin.
- **F5:** **exploit** — tighten the search around the best point (note some coordinates sit near the
  bounds, so the true optimum may lie at the edge).
- **F6 / F7 / F8:** stay the course (EI / high-dim UCB); steady gains, exploration still valuable.

> **Bottom line:** The Week 1 strategy behaved as intended. Five functions improved immediately, and
> the three that did not each produced actionable information. Week 2 is about *refinement, not
> redesign*: exploit where we found a clear signal (F5), keep exploring where the space is still
> mostly unknown (F1, high-dim functions), and treat noise as noise (F2).
