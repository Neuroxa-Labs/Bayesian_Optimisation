# Week 2 Strategy — Black-Box Bayesian Optimisation

*Module 13 Capstone — refined per-function plan after Week 1, now working with 11 data points each.*

## 1. Guiding principle

Week 2 is **refinement, not redesign**. The Week 1 results (5 of 8 functions improved) confirmed
that our per-function acquisition-function (AF) choices are sound. So instead of changing the
framework, we let each function move along the **explore → exploit** axis at the pace its own data
justifies:

- **Exploit** where a clear signal has emerged (commit to the good region).
- **Keep exploring** where the space is still mostly unknown (sparse peaks, high dimensions).
- **Treat noise as noise** — do not over-react to a single lower reading.

Our pipeline encodes a phase schedule (`_phase`): **weeks 1–4 = exploration**, 5–9 = balanced,
10–13 = exploitation. So by the calendar, Week 2 is still an *exploration* week. The important
nuance: two functions self-adapt by **signal threshold** rather than the calendar (F1 and F5),
which is exactly the behaviour we want.

## 2. Per-function Week 2 plan

| Fn | Dim | Week 1 outcome | Week 2 AF (auto) | Mode | Rationale |
|----|-----|----------------|------------------|------|-----------|
| F1 | 2 | still ~0 (no signal) | **COVERAGE** + boundary penalty | Interior explore | Farthest from existing points; avoid GP boundary artefacts. Query: `0.421-0.464`. |
| F2 | 2 | 0.490 (noise dip) | **EI** | Explore-lean | Noisy target; refine *around* the known-good region (best ≈ 0.611). Don't abandon it on one low draw. |
| F3 | 3 | −0.168 (worse) | **UCB κ=2.576** + narrow bounds | Local explore | x3 sensitive (ls=0.07): search x3∈[0.19,0.49], x2∈[0.53,0.69] around best. Query: `0.493-0.692-0.401`. |
| F4 | 4 | −4.03 → 0.257 (big jump) | **UCB κ=3.0** | Explore (high κ) | Multimodal; keep wide coverage but start tracking the new positive basin. |
| F5 | 4 | 1089 → **2497** (huge) | **UCB κ=1.0** (signal-triggered exploit) | **Exploit** | Signal crossed threshold (2000) → tighten around the best point. Primary win to consolidate. |
| F6 | 5 | −0.714 → −0.478 | **EI** | Explore-lean | Steady gain; EI keeps a balanced push toward 0 in 5D. |
| F7 | 6 | 1.365 → 1.451 | **EI** | Explore-lean | High-dim; balanced EI, sustained exploration is still valuable. |
| F8 | 8 | 9.598 → 9.796 | **UCB κ=2.576** + boundary penalty | Explore | Penalise edge-hugging points (was 5 dims on boundary → now 1). Query: `0.07-0.07-0.02-...`. |

## 3. Where the focus should go this week

1. **F5 — consolidate the win (top priority).** This is our clearest signal. Week 2 should exploit:
   sample close to the best point to climb the single peak further. **Watch the bounds** — some
   coordinates sit near the edge (≈0.98), so the optimum may lie at the boundary; keep candidates
   inside `[0.02, 0.98]` but allow them to press against the edge.
2. **F4 — lock onto the new basin.** We escaped a negative region into a positive one. Keep high-κ
   coverage (multimodal risk) but bias new samples toward the basin around the Week 1 success.
3. **F1 — coverage, not corners.** Switched from raw UNCERTAINTY to coverage + boundary penalty;
   targets the largest interior gap (`0.421, 0.464`), not a misleading edge point.
4. **F3 — small steps on sensitive x3.** Narrow bounds around the best point after Week 1's large
   jump backfired.
5. **F8 — boundary penalty.** UCB still explores, but edge points are penalised.

## 4. A deliberate strategic question (the "thoughtful iteration" part)

Our phase schedule is **calendar-based** (weeks 1–4 = explore). With ~13 weeks total, that raises a
trade-off worth stating explicitly:

- **Low-dim functions that already found good signal (F2, F5):** these could justify **earlier
  exploitation** than the calendar dictates. F5 already self-adapts via its signal threshold; for
  F2 we *could* lower κ / tighten search sooner. **Decision for Week 2: hold EI for F2** — because
  the single dip is most likely noise, and we want one more reading near the good region before
  committing.
- **High-dim functions (F7, F8) and multimodal (F4):** here, **early exploitation is a trap**.
  Premature commitment risks locking onto a local optimum in a large space. We deliberately preserve
  their exploration budget.

This asymmetry — exploit fast in low dimensions with signal, stay patient in high dimensions — is
the core refinement of our Week 2 approach.

## 5. Summary

- **No framework change.** Week 1 validated the per-function AF design.
- **F5 → exploit** (signal-triggered), **F1 → coverage exploration** (interior gaps), **F3/F8 →
  refined bounds/penalties**, everything else **stays the course** within the exploration phase.
- The key reasoning: let the **data and dimensionality**, not just the calendar, decide how fast each
  function moves from exploration to exploitation.

> **Week 2 queries (submitted):**
> ```
> F1: 0.421062-0.463562   F2: 0.734317-0.926564   F3: 0.492581-0.691593-0.401268
> F4: 0.460385-0.434644-0.203056-0.431758   F5: 0.074189-0.696480-0.980000-0.980000
> F6: 0.517086-0.282151-0.771390-0.980000-0.207535
> F7: 0.020000-0.491672-0.247422-0.214597-0.377195-0.806097
> F8: 0.070000-0.070000-0.020000-0.038786-0.403935-0.070000-0.070000-0.893085
> ```
