# Technical Justification — Prior Work & Tooling

*Discussion-board write-up: grounding the BBO strategy in literature and libraries (<700 words).*

---

My main technical choice is a Gaussian Process with EI or UCB. With one query per function per week and only a few dozen points, I need a model that works on small data and gives uncertainty. That is what classical Bayesian optimisation is built for: fit a GP, then use an acquisition score to pick the next point. A neural net could fit the past values, but with this sample size it can overfit and does not naturally give the kind of uncertainty EI/UCB need.

The ideas behind this come from standard BO / GP work. Rasmussen and Williams are the usual reference for GPs and kernels — that is why I look at length scales and use a Matérn kernel. Jones et al. motivate Expected Improvement when I want to beat the current best. Srinivas et al. motivate UCB when I still need exploration, especially on multimodal or higher-dimensional functions. I am not implementing a paper line by line; I am using these as the reason to stay with GP + acquisition instead of switching models every week.

For code, I rely on NumPy, scikit-learn, SciPy, and Matplotlib. scikit-learn’s GaussianProcessRegressor is enough for this project and easy to debug. I considered PyTorch or TensorFlow surrogates, and also more specialised BO libraries, but they felt heavy for ~15–50 points per function. An SVM is related as a kernel method, but it does not give calibrated predictive variance for EI/UCB, so I keep it as a conceptual parallel only.

I document the reasoning in the GitHub repo: README for the overall pipeline and per-function choices, weekly strategy/reflection notes for what changed after each portal result, and short write-ups on library and design trade-offs. The goal is that someone opening the repo can see why I use a GP, not only which x I submitted.

Looking ahead, I may read more practical BO material (for example Frazier’s tutorial) and look at BoTorch-style acquisition options if I need richer search later. For F1, if the peak stays invisible, sparse-peak or stronger exploration methods are worth checking. I would also compare against simple baselines like random or Sobol points, just to sanity-check that the GP proposals are actually helping.
