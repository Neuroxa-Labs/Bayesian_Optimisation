# Week 5 Discussion — Reflection on Strategy (Module 16)

*Submitted after Week 5 queries (14 observations per function).*

---

## Introduction

This week I submitted my fifth round of queries for the BBO capstone. I kept a Gaussian Process as my surrogate rather than switching to a neural network, but Module 16 prompted me to reflect on how deep learning concepts — feature hierarchies, architectural trade-offs, and framework choices — parallel the iterative design of my optimisation strategy.

---

## 1. Hierarchical feature learning and my optimisation strategy

In deep learning, early layers capture simple patterns and deeper layers combine them into richer features. My BBO workflow has evolved in a comparable way. Early weeks were about coarse structure: whether outputs are positive or negative, what scale they sit on, and which dimensions seem inactive (degenerate length scales). By Week 5, the focus shifted to finer patterns — for example, which input directions define the F5 yield ridge, or how steep the gradient is near F7’s current best at 1.857.

Practically, my pipeline loads and updates data, applies function-specific transforms (log-y on F5, WhiteKernel noise on F2), fits a GP, and then uses an acquisition function to propose the next point. Each stage narrows the decision rather than jumping straight from raw data to a single guess. That is the closest analogue I have to hierarchical feature learning: broad structural learning first, local refinement later.

---

## 2. AlexNet, ImageNet, and incremental capstone progress

AlexNet did not appear from nowhere — it stacked ReLU, deeper convolutional layers, dropout, and more data into one breakthrough. My capstone progress looks similar in spirit, if smaller in scale. No single change produced a dramatic jump on its own: fixing F3 bounds in Week 2, adding log-y on F5, local basin search on F4, and boundary penalties on F6/F7 each contributed a piece of structure. Week 4 was the clearest payoff — four functions improved, with F5 reaching 3744 and F7 reaching 1.857 — after several weeks of data and rule refinement rather than a wholesale model swap.

That parallel matters for expectations. In both deep learning history and BBO, breakthrough-looking results often follow a long period of incremental adjustments where the system learns *where* to look before it learns *how* to exploit precisely.

---

## 3. Explore/exploit trade-offs (depth, complexity, and efficiency)

Designing neural networks involves balancing depth and complexity against training cost and overfitting risk. In my queries, the equivalent trade-off is exploration versus exploitation. With only one query per function per week, wide exploration covers more of the space but wastes budget if good regions are already known. Heavy exploitation is efficient but can miss a better peak elsewhere.

This week I applied that balance differently per function. F1 remains exploratory (coverage grid) because readings are still essentially zero. F5 and F7 are strongly exploitative near known highs. F3 uses a locked x₃ near 0.401 because earlier exploratory moves above 0.5 missed the best −0.020 region. F6 deliberately avoids box edges after boundary queries underperformed. The trade-off is not “explore or exploit everywhere,” but how much capacity to spend refining a promising region versus searching elsewhere.

---

## 4. Neural network building blocks and learning from accumulated data

Several deep-learning concepts helped me interpret what the surrogate is doing with the data collected so far:

- **Inputs:** normalised query vectors in [0,1]ᵈ — the raw coordinates fed into the model.
- **Activations / representation:** the Matérn kernel shapes how nearby points influence predictions — smooth versus sharp local response.
- **Loss:** I think of “current best y” as the baseline to beat; acquisition scores ask whether a candidate is likely to improve on that loss.
- **Gradients:** the acquisition surface (EI, UCB) plays a similar role — it points toward directions of expected improvement on the GP posterior.
- **Weight updates:** each portal response adds one observation and updates beliefs — one step of iterative learning, not retraining from scratch in a batch sense.

I considered a small NN or SVM as an alternative surrogate, especially for higher-dimensional functions, but with 14–44 points per task I stayed with the GP because it provides both mean and uncertainty for EI/UCB without extra machinery. NN ideas informed *strategy*; they did not replace the model this round.

---

## 5. Framework analogy: PyTorch-style flexibility vs structured design

Module 16 introduced PyTorch and TensorFlow as different ways to build and scale models. If I map my optimisation approach to a “framework” choice, it sits between rapid prototyping and structured design — perhaps closer to a modular production notebook than to ad-hoc PyTorch experimentation.

Core components (data loading, GP fitting, acquisition, diagnostics) are fixed, but I retain weekly flexibility: per-function ν and α, manual overrides when the GP hits boundaries (F7 x₁, F3 x₃), and log transforms where the data justify them. Before submission I review posterior behaviour, length scales, and whether a proposed point actually targets improvement over the current best — similar to checking training curves before deploying a model.

---

## 6. Real-world benchmarking (Giovanni Liotta guest interview)

The guest interview on deep learning in sport emphasised that industry success is measured by reliable performance gains under real constraints, not by model complexity alone. That reframed how I judge this capstone. A fancy surrogate metric matters less than whether each week’s query moves a function toward a better zone under a strict budget.

F5 and F7 are my clearest benchmarks — not one lucky spike, but repeated refinement of high-performing regions. F1 remains unresolved, which is itself informative: some landscapes need coverage and patience before any hierarchical “deep” exploit layer becomes meaningful.

---

## Conclusion

Overall, Module 16 did not push me to bolt an AlexNet onto eight black boxes. It pushed me to articulate *why* my iterative GP strategy is layered, function-specific, and judged by outcomes — the same mindset that makes deep learning work in practice, even when the surrogate stays classical.
