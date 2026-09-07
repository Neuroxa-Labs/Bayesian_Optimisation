# Final-round reflection — RL lens

*Discussion-board post for the final query round. First person. Under 700 words. After Week 12 (4/8 improved).*

---

**Exploration vs exploitation (and how that balance evolved)**

Early in the project I behaved like a high-exploration bandit: wide UCB/EI, space-fill moves, and occasional jumps into empty corners of the unit hypercube. That was rational when every arm (region) was uncertain and I had almost no reward history. As the dataset grew past ~20 points per function, the balance flipped. Proven high-reward neighbourhoods — F4/F5/F7/F8 basins, F5’s x₁ ridge, F1’s (0.64, 0.68) signal lobe — became the arms I pull almost every week. Exploration did not disappear; it shrank to places where the surrogate is still untrusted (historical F1) or where a sensitive coordinate is still climbing (F5). Week 12 confirmed the late-game policy: four new bests from local exploit, a partial F6 recovery after a failed neighbour step, and another F2 miss on a razor ridge. For the final-round queries I therefore take almost pure exploitation inside compressed trust regions, with only tight recovery pulls on F2/F3/F6.

**Feedback, reward expectations, and Q-style updates**

Each portal return is a scalar reward for the action (query) I chose. In RL terms that feedback updates my estimate of which actions are valuable — analogous to adjusting Q-values or reward expectations after a transition. A strong positive surprise (F5’s ridge climb; Week 10’s F6 jump; Weeks 11–12 ticks on F4/F7/F8) raises the value of that local “arm” and makes me sample nearby again. A negative surprise (F6’s −0.372; F2’s repeated ~0.54 readings near the 0.777 peak) lowers the value of that offset and triggers a policy correction: shrink the step or return toward the incumbent centroid. The Gaussian Process posterior is my stand-in for a Q-landscape: mean ≈ expected return, variance ≈ uncertainty bonus. Acquisition (EI/UCB) then plays the role of the bandit/RL rule that trades those two quantities off under a one-query-per-week budget.

**AlphaGo Zero, self-play, and model-based vs model-free**

My loop resembles autonomous iterative improvement more than classical supervised learning: each round uses only self-generated (x, y) trajectories to refine the next policy, without an external teacher labelling the true optimum. It is closer to **model-based** planning than to pure model-free trial-and-error. I maintain an explicit surrogate of the objective (the GP), simulate candidate actions through acquisition scores, and then commit to a single expensive evaluation — more like planning with a learned model than like updating a Q-table only after raw interaction. Unlike AlphaGo Zero I do not run self-play between two agents; the “opponent” is the unknown black box. But the spirit — improve the policy from one’s own experience, and use a model to look ahead before spending a scarce sample — is the same.

**Real-world value of this RL framing**

In drug design, chemical process tuning, or hyperparameter search, each experiment can cost days or thousands of pounds. An RL-style explore–exploit schedule, backed by a surrogate and uncertainty-aware acquisition, allocates those trials where expected improvement is highest and cuts wasteful grid search. Trust regions and ARD-style dimension focus further speed convergence by freezing irrelevant knobs. The practical lesson from this capstone is sample-efficient sequential decision-making: start curious, then commit hard to verified high-reward arms, and treat every feedback signal as a policy update — not as noise to ignore.
