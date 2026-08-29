# Week 11 Discussion — Clustering lens (11th round)

*Copy-paste for the discussion board. First person. Under 700 words.*

---

**How past query patterns shaped this round**

After ten rounds the map is no longer a blank box. Week 10 reinforced a clear pattern: when I stay inside a high-performing neighbourhood, best-y moves (F4 0.64→0.67, F5 3769→3779, F6 −0.24→**−0.14**, F7/F8 small ticks). When I leave a known good cluster without evidence — earlier F2/F6 overshoots, F1 space-fill hops — I waste the weekly budget. So Week 11 queries are almost all **within-cluster steps**: small offsets from the current incumbent or from the newly validated F1 signal lobe, not global acquisition jumps into empty space.

**Clusters / recurring regions I treat as promising**

I think of each “cluster” as a tight cloud of past inputs that share high (or, for F1, non-null) outputs — like a clustering algorithm’s dense group around a centroid.

- **F4 / F6 / F7 / F8:** local basins around the Week 10 bests; I nudge inside that ball rather than jumping to a second guessed mode.
- **F5:** a ridge cluster on the high x₂–x₄ face with x₁ walking 0.38→0.42→**0.43** this week.
- **F2:** a thin ridge cluster near (≈0.72, ≈0.02); I step toward the historical centroid (0.718, 0.02) that still holds 0.777.
- **F3:** a constrained cluster with x₃≈0.40; I return toward the −0.011 point.
- **F1:** two competing stories — a long null cluster near (0.73, 0.73) versus a **signal cluster** near (0.64, 0.68) that Week 10 finally hit (y≈−0.008). I now exploit the signal cluster, not the null one.

**What proved less effective — and how I adjust**

Global EI/UCB into unexplored corners, exact incumbent replays, and uniform micro-steps away from a sharp peak (F2’s 0.72 cliff, early F6/F7) were weak. Max-distance exploration on F1 also failed for weeks. Adjustments: trust-region radius as the main “bandwidth,” WhiteKernel / noise awareness on F2, log-y on F5, hard locks (F3 x₃, F5 high face), and a trust gate that refuses GP exploit when every label is ~0 — until a real cluster appears.

**Parallel to clustering algorithms**

Clustering separates dense structure from noise by distance and similarity. My refinements do the same in optimisation form: points with similar x and strong y define a basin; outliers and near-zero F1 samples are treated as noise or empty space. Shrinking the trust region is like tightening a cluster boundary around a centroid. ARD length scales act like feature weights — dimensions that do not separate good from bad get less movement, analogous to ignoring noisy features before clustering. Week 10’s F1 result is the clustering moral in one line: the null (0.73) group looked “central” because I sampled it often, but the meaningful group was elsewhere; once a non-null label appeared, I reassigned the active cluster.

**If the queries were plotted — trends and next iteration**

A plot of all (x, y) would show tight clouds around F4–F8 incumbents, a ridge line on F5, a needle on F2’s low-x₂ edge, and for F1 a new coloured point in the 0.64/0.68 lobe against a sea of near-zeros near 0.73. That picture already drives Week 11: stay inside the high-y clouds, walk the F5 ridge one step, pull F2 toward its best centroid, and micro-exploit F1’s signal cluster. Next iteration, if F1’s cluster deepens (larger |y| or a positive tick under maximisation), I keep compressing that neighbourhood; if it goes flat again, I treat it as a weak cluster and reopen controlled exploration — the same decision a clustering pipeline makes when a putative group loses cohesion.
