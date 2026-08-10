# Module 20 Discussion — Scaling & Emergence (9th query round)

*Copy-paste for the discussion board. First person. Under 700 words.*

---

**Scaling laws and my query choices**

Scaling laws say more data or compute usually helps, but not in proportion forever. Each weekly query updates my Gaussian Process; early rounds moved the posterior a lot, while by the ninth round (~18 points on lower-D functions, more on F4–F8) I mostly see **diminishing returns on best-y**, even when the surrogate is sharper.

That changes how I choose queries. I no longer trust a global acquisition argmax in an empty corner. I ask whether the point adds decision-relevant information inside a trust region. F5 shows classic diminishing returns after the breakthrough: big early jumps, then 3744→3760 at x₁=0.40, and this week only a small step to 0.41. F8 gains are ~0.001 — real but small. F1 gains nothing from longer “context.” Higher-D boxes (F7/F8) are still sparse, so I keep light exploration there, not blind global UCB. Progress is mixed: best-y improves slowly or in spurts; my confidence about *where* to look can still improve. I do not score a week only by whether every output rose.

**Emergent behaviour and how I prepare**

Emergence means sudden behaviour once evidence crosses a threshold. Week 8 did that on F4 (~0.47→**0.57**) and when F5’s step past x₁=0.38 paid off — not a smooth micro-step story. F7’s earlier mid-project jump was similar; F1 shows the opposite: no emergence despite many queries.

I prepare with diagnostics, not weekly miracle bets: length scales, boundary drift, distance to the incumbent, and a **trust gate**. If there is no signal on F1, I refuse GP exploit. On F4 I use a local search radius around the new 0.57 basin so I can exploit it while staying open to a nearby ridge that exact replay would miss.

**Cost, robustness and performance**

The binding cost is **one query per function per week**. That pushes me toward known basins for performance (F4, F5, F8). Robustness warns me against near-duplicates and against a heavy neural net on n≈18 — it overfits and hallucinates corners. GP fit cost is cheap next to the black-box call, so I keep WhiteKernel on noisy F2, log-y on F5, and boundary penalties, with the GP as my main decider.

In practice I use low κ/ξ trust-region exploit when the basin is clear; tiny *new* offsets back toward the incumbent after a failed step (F2/F3/F6); and space-fill only where the trust gate fails (F1). F1’s opportunity cost is high relative to progress — I still cover it, but I do not pretend the week’s performance lives there.

**Predictable optimisation vs uneven emergence**

Predictable optimisation, for me, is the structured shift from exploration to exploitation: Matérn GP, EI/UCB, decaying exploration weight, and constraints (F3 x₃ lock, F5 high face, interior penalties). That stops me overreacting to one weird acquisition spike.

Uneven emergence means one function can jump (F4/F5) while another stays flat (F1). I keep small trust-region optionality and continued explore on no-signal cases, without leaving my GP-led loop. Noise checks and ARD “attention” to sensitive dimensions help me tell real jumps from artefacts. Overall I stick to systematic BO for consistency, but I revise the local plan when evidence produces a discontinuous gain — the same scaling/emergence lesson as in large LLMs, under a much stricter evaluation budget.
