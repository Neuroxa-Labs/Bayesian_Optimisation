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
| F1 | 2 | still ~0 (no signal) | **UNCERTAINTY** | Pure explore | No signal yet → keep mapping the largest empty gaps until any non-zero reading appears. |
| F2 | 2 | 0.490 (noise dip) | **EI** | Explore-lean | Noisy target; refine *around* the known-good region (best ≈ 0.611). Don't abandon it on one low draw. |
| F3 | 3 | −0.168 (worse) | **UCB κ=2.576** | Explore | Expected exploration cost; keep mapping. Still early (3D). |
| F4 | 4 | −4.03 → 0.257 (big jump) | **UCB κ=3.0** | Explore (high κ) | Multimodal; keep wide coverage but start tracking the new positive basin. |
| F5 | 4 | 1089 → **2497** (huge) | **UCB κ=1.0** (signal-triggered exploit) | **Exploit** | Signal crossed threshold (2000) → tighten around the best point. Primary win to consolidate. |
| F6 | 5 | −0.714 → −0.478 | **EI** | Explore-lean | Steady gain; EI keeps a balanced push toward 0 in 5D. |
| F7 | 6 | 1.365 → 1.451 | **EI** | Explore-lean | High-dim; balanced EI, sustained exploration is still valuable. |
| F8 | 8 | 9.598 → 9.796 | **UCB κ=2.576** | Explore | Largest space (8D); keep broad exploration, small steady gains expected. |

## 3. Where the focus should go this week

1. **F5 — consolidate the win (top priority).** This is our clearest signal. Week 2 should exploit:
   sample close to the best point to climb the single peak further. **Watch the bounds** — some
   coordinates sit near the edge (≈0.98), so the optimum may lie at the boundary; keep candidates
   inside `[0.02, 0.98]` but allow them to press against the edge.
2. **F4 — lock onto the new basin.** We escaped a negative region into a positive one. Keep high-κ
   coverage (multimodal risk) but bias new samples toward the basin around the Week 1 success.
3. **F1 — patience.** Continue pure exploration; a zero is elimination, not failure. The next query
   targets the biggest uncovered region. No change.

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
- **F5 → exploit** (signal-triggered), **F1 → keep pure exploration** (no signal), everything else
  **stays the course** within the exploration phase.
- The key reasoning: let the **data and dimensionality**, not just the calendar, decide how fast each
  function moves from exploration to exploitation.

> **Next action:** generate Week 2 query points by running the pipeline with the updated 11-point
> dataset, then submit and record the new outputs for the Week 3 iteration.
