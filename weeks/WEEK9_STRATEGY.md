# Week 9 Strategy — after Week 8 (3/8 improved: F4, F5, F8)

## Week 8 results (reference)

| Fn | Prior best → W8 y | Improved? |
|----|-------------------|-------------|
| F1 | ~0 → ~0 | No |
| F2 | 0.777 → 0.627 | No — left of cliff but missed peak |
| F3 | −0.011 → −0.026 | No |
| **F4** | 0.470 → **0.572** | **Yes** |
| **F5** | 3744 → **3760** | **Yes** — x₁=0.40 ridge |
| F6 | −0.240 → −0.283 | No |
| F7 | 1.857 → 1.856 | Flat |
| **F8** | 9.865 → **9.868** | **Yes** |

## Week 9 policy (LLM Module 19 framing)

- **Low temperature / structured prompt** where W8 proved signal (F4, F5, F8): tight exploit.
- **Retract bad decode** on F2/F6/F3: return toward incumbent with tiny new offset (no exact replay).
- **F1:** still refuse GP exploit — new explore “prompt”.

## Portal queries (Week 9)

```
Function 1:  0.550000-0.320000
Function 2:  0.716000-0.018000
Function 3:  0.495000-0.695000-0.400000
Function 4:  0.400000-0.418000-0.360000-0.408000
Function 5:  0.410000-0.980000-0.980000-0.980000
Function 6:  0.442000-0.248000-0.592000-0.728000-0.132000
Function 7:  0.068000-0.430000-0.305000-0.160000-0.348000-0.674000
Function 8:  0.138000-0.066000-0.216000-0.044000-0.408000-0.508000-0.222000-0.905000
```

## Status

Ready to submit (9th portal round / Module 20).  
Reflection: [`WEEK20_DISCUSSION.md`](WEEK20_DISCUSSION.md) (scaling & emergence).  
Module 19 LLM reflection (already posted): [`WEEK9_DISCUSSION.md`](WEEK9_DISCUSSION.md).
