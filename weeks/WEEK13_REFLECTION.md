# Week 13 Reflection — Final portal round

*Results after Week 13 / final-round portal submission.*

## Headline

**4 of 8 improved** — **F4, F5, F7, F8**. F5 ridge continued to **≈3813** at \(x_1=0.45\). F3 reaffirmed the **−0.011** peak. F1 signal lobe improved to **−0.00457** (still below seed max). F2 and F6 missed their historical basins.

## Week 13 results

| Fn | Prior best → W13 y | Improved? | Notes |
|----|--------------------|-----------|--------|
| F1 | ~0 (seed) / lobe ~−0.005 | −0.00457 | Lobe continued (not official best) |
| F2 | **0.777** | 0.372 | No — hard-return missed the needle |
| F3 | **−0.011** | −0.011366 | Held / reaffirmed safe band |
| **F4** | 0.6786 | **0.6794** | **Yes** — micro-step |
| **F5** | 3801 | **3812.75** | **Yes** — ridge \(x_1=0.45\) |
| F6 | **−0.136** | −0.207 | No — short of W10 centroid |
| **F7** | 1.872 | **1.878** | **Yes** — micro-step |
| **F8** | 9.873 | **9.8737** | **Yes** — micro tick |

## Cumulative best after Week 13 (final)

| Fn | Best y | Incumbent note |
|----|--------|----------------|
| F1 | 7.711×10⁻¹⁶ (seed) | Late lobe ~−0.0046 is usable but below seed max |
| F2 | **0.776645** | Historical Week-5 ridge held; W13 miss |
| F3 | **−0.011366** | Safe \(x_3\) lock confirmed |
| F4 | **0.679389** | Week 13 |
| F5 | **3812.75** | Week 13 ridge |
| F6 | **−0.136** | Week 10 still best |
| F7 | **1.877841** | Week 13 |
| F8 | **9.873669** | Week 13 |

## Late improve streak

W8 3/8 · W9 4/8 · W10 5/8 · W11 4/8 · W12 4/8 · **W13 4/8** (F4, F5, F7, F8).

## Takeaways

- Trust-region / ridge exploit paid off on F4/F5/F7/F8 through the final round.
- F5 remains the clearest success story (seed ~1089 → **3813**).
- Sharp basins (F2, F6) stayed fragile even under hard-return.
- F1 never beat the near-null seed reading; the late lobe is evidence of a real signal neighbourhood, not a solved peak.

Strategy note: [`WEEK13_STRATEGY.md`](WEEK13_STRATEGY.md) · hub: [`../STRATEGY.md`](../STRATEGY.md).
