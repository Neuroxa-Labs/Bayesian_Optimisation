# Week 6 Discussion — Reflection on Strategy (Module 17 / CNNs)

*Submitted after Week 6 queries (~15 observations per function).*

---

This week I submitted my sixth round of BBO queries with roughly 15 observations per function. I still use a Gaussian Process with EI/UCB, but Module 17’s CNN ideas helped me rethink how that process builds understanding over time — from coarse patterns to finer local structure.

**Progressive feature extraction.** CNNs start with edges and textures, then compose object-level features. My BBO strategy has followed a similar path. Early weeks were about coarse “features”: sign of y, rough scale, and which dimensions look flat (degenerate length scales). By Week 6 I was working with mid-level structure — F5’s yield ridge near x₁≈0.38, F3’s safe band for x₃≈0.401, and F4’s positive warehouse basin. This round I refined those features rather than restarting from scratch: keep x₃ locked on F3, stay interior on F6, and exploit F4 locally. That is progressive extraction in optimisation form: first learn what kind of landscape you have, then sharpen the details that matter.

**LeNet-style breakthroughs and incremental gains.** LeNet and later CNNs did not win by one clever trick alone; they stacked simple, reusable ideas until performance jumped. My capstone feels similar. No single week reinvented the pipeline. Fixes accumulated: narrower bounds on F3, log-y on F5, boundary penalties on F6/F7, and local basin search on F4. Week 6’s clearest payoffs — F4 jumping to about 0.47, F3 to −0.011, F6 to −0.240 — came from that stacked learning. Like vision models, progress here is less “sudden genius” and more “enough structure finally clicks.”

**Depth, cost, and overfitting vs explore/exploit.** Training deeper CNNs costs compute and can overfit. With one query per function per week, exploration is my “depth/capacity” and exploitation is my “efficiency.” Exploring widely is expensive if a good region is already known; exploiting too hard can miss another peak. Week 6 forced that trade-off explicitly. On F4 and F6 I exploited known good neighbourhoods and improved. On F2 I pushed too far from the W5 best (0.777 at high x₁, low x₂) and dropped to 0.40 — a reminder that aggressive steps can “overfit” to a wrong local story. On F1 I am still exploring because there is almost no signal; exploiting near zero readings would just polish noise.

**Convolutions, pooling, activations, and loss.** A few CNN building blocks changed how I read the GP:

- **Convolution:** local kernels → Matérn length scales. Short length scales mean the response is local and sharp; I take smaller steps (F1, parts of F7).
- **Pooling:** summarising regions → my manual locks and filters (freeze x₃ on F3; avoid box edges on F6). Pooling discards detail to keep what matters; locks do the same under a tight budget.
- **Activation:** soft non-linear response → how the GP posterior bends around data. Softmax-like ranking of candidates appears in acquisition scores.
- **Loss:** current best y is the baseline; EI/UCB ask whether a new point is worth the query cost relative to that baseline — like deciding if another training step is worth it.

**Edge AI and how I benchmark success.** Andrea Dunbar’s edge-AI discussion emphasised deploying under constraints: limited compute, limited data, clear success metrics. My BBO “deployment” constraint is even stricter — eight black boxes, one query each per week. So I no longer treat “did every function improve?” as the only score. Success is: (1) improve where the model has signal (F3/F4/F6 this week), (2) avoid expensive mistakes (F2 overshoot), and (3) keep a defensible plan for no-signal cases (F1). That is closer to edge thinking: maximise value under budget, not perfection everywhere.

Overall, CNNs reminded me that good systems learn in layers. Week 6 was a mid-depth layer: not first contact with the data, not final polish — targeted refinement of features I already trust.
