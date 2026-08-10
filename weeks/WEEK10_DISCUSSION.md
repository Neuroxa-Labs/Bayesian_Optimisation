# Week 10 Discussion — Reasoning, Transparency, Assumptions (10th round)

*Copy-paste for the discussion board. First person. Under 700 words.*

---

**Reasoning behind my tenth-round queries**

I choose each point from the Week 9 outcomes plus the longer history, still with a Matérn GP and EI/UCB inside per-function constraints.

On **F4, F5, F7 and F8** Week 9 set new bests (0.64, 3769, 1.858, 9.869). That pattern says the local basins are real, so I stay slightly exploitative: a tight trust-region step from each new incumbent — F5 continues the ridge to x₁=0.42 with x₂–x₄ locked high; F4 nudges the new warehouse basin; F7/F8 take small interior steps rather than global jumps.

On **F2, F3 and F6** Week 9 did not beat the historical bests. F2’s return to ~0.716 still scored 0.52 versus 0.777 at ~0.718/0.02, so I move even closer to that record with a fresh offset. F3 stays in the safe x₃≈0.40 band but steps back toward the −0.011 coordinates. F6 got closer than Week 8 (−0.25 vs −0.28) yet remains below −0.24, so I micro-adjust around that older cake-recipe best instead of another wider step.

**F1** still has essentially no usable signal at my historical best near `[0.731, 0.733]`. Space-fill hopping also failed. Interpreting F1 as a **localised radiation peak** (only proximity to a source yields signal), and drawing on a peer basin where measurable responses appeared near **`~0.64 / ~0.68`**, I place this week’s query in that neighbourhood rather than polishing the null lobe or the domain centre.

**Transparency / reproducibility**

Another researcher could largely reproduce my strategy from the repo notes: cumulative (x, y) per function, the GP config (Matérn ν, length-scale bounds, WhiteKernel on F2, log-y on F5), acquisition choice (EI vs UCB and rough κ/ξ), explicit locks (F3 x₃, F5 high face), boundary penalties, and the trust-gate rule for F1. Weekly strategy files list the exact portal strings and one-line rationales. What is less fully automatic is the final human override of trust-region radius after reading diagnostics — that step is documented in the week notes, but not a single frozen hyperparameter file for every round.

**Key assumption and how it limits me**

I assume each promising function has **one dominant smooth basin** (or one ridge on F5) that local BO can climb. That can fail if a sharp second peak sits far from my sampled clusters — especially on F4/F7/F8, where I now spend budget near the incumbent. On F1 I now make the parallel bet that any useful mass, if it exists, is near my best-so-far lobe rather than uniformly elsewhere; that can also trap me. The assumption speeds progress when true (Week 8–9 jumps) but can miss a distant global max.

**Gaps and sampling bias in the data**

My dataset is clustered: F5 almost only on the high x₂–x₄ face; F3 mostly with x₃ near 0.4; F6/F7/F8 around recent bests; F2 along the low-x₂ line. Large volumes of each hypercube are untouched. I also bias against exact 0/1 corners because early GPs hallucinated boundaries — that removes some artefacts but can miss a true edge optimum. F1 was exploratory for many weeks; this round I intentionally bias toward the historical best lobe after space-fill failed — a deliberate remaining-budget bias, not proof that the peak is there.

**One significant limitation**

The hard limit is **one evaluation per function per week**. Even a well-tuned GP cannot run a proper inner optimisation loop on the real black box; I get one shot to test a hypothesis. Combined with a stationary kernel, that makes discontinuous or very narrow peaks easy to miss and makes F1’s null results expensive in opportunity cost. I manage it by exploiting where Week 9 proved signal and exploring only where the trust gate fails — accepting that I optimise under incomplete information, not under a full grid.
