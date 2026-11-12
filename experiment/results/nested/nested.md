# Option D: nested cross-validation (rule: TUNING_RULE.md)

Failed fits: 0

## Question 1: tuned vs fixed widths (per seed, Wilcoxon over 11 datasets)

| seed | vs | median gain | mean gain | tuned better / same / worse | Wilcoxon p | Q1 passes |
|--:|---|--:|--:|:-:|--:|:-:|
| 0 | (w=5) (primary) | -0.39 pp | -0.93 pp | 2 / 2 / 7 | 0.250 | no |
| 0 | (w=1) | +0.10 pp | +2.28 pp | 6 / 0 / 5 | 0.966 | – |
| 0 | (w=20) | -0.48 pp | -1.46 pp | 1 / 3 / 7 | 0.055 | – |
| 1 | (w=5) (primary) | +0.91 pp | +1.04 pp | 9 / 0 / 2 | 0.102 | no |
| 1 | (w=1) | +1.04 pp | +3.03 pp | 8 / 0 / 3 | 0.024 | – |
| 1 | (w=20) | +0.62 pp | +0.39 pp | 7 / 0 / 4 | 0.278 | – |
| 2 | (w=5) (primary) | +0.00 pp | +0.29 pp | 5 / 1 / 5 | 1.000 | no |
| 2 | (w=1) | +0.71 pp | +2.72 pp | 8 / 0 / 3 | 0.320 | – |
| 2 | (w=20) | +0.00 pp | -0.55 pp | 4 / 2 / 5 | 0.496 | – |

**Q1 verdict: NOT ESTABLISHED** (seeds passing: 0 of 3).

## Question 2: tuned vs hindsight-best fixed width (oracle, mean of 3 seeds)

| dataset | oracle width | oracle acc | tuned acc | tuned − oracle | w=5 − oracle |
|---|---|--:|--:|--:|--:|
| lymph | (w=20) | 83.9% | 80.5% | -3.41 pp | -1.84 pp |
| heart-c | (w=5) | 81.1% | 78.0% | -3.17 pp | +0.00 pp |
| breast-cancer | (w=20) | 73.1% | 71.0% | -2.10 pp | -1.75 pp |
| glass | (w=20) | 71.8% | 70.8% | -1.10 pp | -0.92 pp |
| vote | (w=1) | 94.9% | 93.9% | -0.92 pp | -0.00 pp |
| diabetes | (w=10) | 75.4% | 75.0% | -0.39 pp | -0.57 pp |
| monks-problems-2 | (w=20) | 96.1% | 95.8% | -0.22 pp | -6.10 pp |
| car | (w=10) | 95.3% | 95.1% | -0.15 pp | -0.44 pp |
| tic-tac-toe | (w=20) | 98.4% | 98.3% | -0.03 pp | -0.17 pp |
| iris | (w=20) | 93.3% | 93.3% | +0.00 pp | -0.67 pp |
| credit-approval | (w=1) | 85.0% | 85.2% | +0.24 pp | -0.24 pp |

Within 1 pp of the oracle: tuned on **7 of 11** datasets (w=5 alone: 8 of 11; w=20 alone: 9 of 11).

**Q2 verdict: NOT ESTABLISHED** (needs ≥ 9 of 11).

## Which width did the inner CV choose? (count over 30 outer folds)

| dataset | w=1 | w=5 | w=10 | w=20 |
|---|--:|--:|--:|--:|
| breast-cancer | 10 | 7 | 9 | 4 |
| car | 0 | 4 | 7 | 19 |
| credit-approval | 21 | 6 | 2 | 1 |
| diabetes | 2 | 7 | 8 | 13 |
| glass | 11 | 5 | 6 | 8 |
| heart-c | 3 | 10 | 12 | 5 |
| iris | 9 | 7 | 4 | 10 |
| lymph | 2 | 3 | 15 | 10 |
| monks-problems-2 | 0 | 0 | 1 | 29 |
| tic-tac-toe | 0 | 0 | 12 | 18 |
| vote | 14 | 7 | 4 | 5 |

Fit time of tuned vs w=5: median 24.1×, range 21.1–28.6× (inner CV fits 4 widths × 5 folds + 1 refit).

