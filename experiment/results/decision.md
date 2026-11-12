# Decision (rule: DECISION_RULE.md)

Rule per seed: Friedman p < 0.05 **and** winner wider than 1 with median gain over w=1 >= 1.0 pp. Established only if every seed passes.

| seed | datasets | Friedman p | part 1 | winner | median gain | part 2 | seed passes |
|--:|--:|--:|:-:|---|--:|:-:|:-:|
| 0 | 11 | 0.102 | no | CN2 (w=20) | +0.95 pp | no | **no** |
| 1 | 11 | 0.301 | no | CN2 (w=20) | +0.75 pp | no | **no** |
| 2 | 11 | 0.561 | no | CN2 (w=20) | +0.42 pp | no | **no** |

**Verdict: NOT ESTABLISHED: no seed passes the rule.**

## Supplementary (not used to decide)

Mean accuracy rank per width (1 = best), per seed:

| seed | (w=1) | (w=5) | (w=10) | (w=20) | mean gain of winner |
|--:|--:|--:|--:|--:|--:|
| 0 | 3.27 | 2.41 | 2.27 | 2.05 | +3.73 pp |
| 1 | 3.09 | 2.32 | 2.50 | 2.09 | +2.64 pp |
| 2 | 2.82 | 2.73 | 2.27 | 2.18 | +3.27 pp |

Per dataset: mean accuracy over seeds (± sd of the per-seed means = how much the split matters):

| dataset | (w=1) | (w=5) | (w=10) | (w=20) |
|---|--:|--:|--:|--:|
| breast-cancer | 72.4 ± 2.5 | 71.3 ± 1.3 | 72.3 ± 2.1 | 73.1 ± 1.1 |
| car | 94.3 ± 0.2 | 94.8 ± 0.4 | 95.3 ± 0.4 | 95.3 ± 0.0 |
| credit-approval | 85.0 ± 1.0 | 84.7 ± 1.5 | 83.8 ± 0.8 | 83.5 ± 0.5 |
| diabetes | 74.2 ± 1.0 | 74.8 ± 1.1 | 75.4 ± 1.1 | 74.8 ± 0.8 |
| glass | 71.1 ± 1.3 | 70.9 ± 0.7 | 71.1 ± 1.7 | 71.8 ± 1.0 |
| heart-c | 77.4 ± 0.2 | 81.1 ± 1.2 | 78.7 ± 0.7 | 78.5 ± 1.3 |
| iris | 92.7 ± 1.2 | 92.7 ± 0.0 | 92.9 ± 0.4 | 93.3 ± 0.7 |
| lymph | 77.3 ± 2.5 | 82.1 ± 1.8 | 80.3 ± 1.7 | 83.9 ± 2.5 |
| monks-problems-2 | 70.5 ± 2.3 | 90.0 ± 0.4 | 92.9 ± 1.3 | 96.1 ± 1.1 |
| tic-tac-toe | 97.9 ± 0.4 | 98.2 ± 0.2 | 98.3 ± 0.1 | 98.4 ± 0.1 |
| vote | 94.9 ± 0.3 | 94.9 ± 0.3 | 94.2 ± 0.3 | 94.3 ± 0.6 |

Friedman on accuracy averaged over the seeds: p = 0.152 (11 datasets). Averaging seeds makes per-dataset means more stable, but the datasets (not the seeds) are the sample, so this is still an 11-dataset test.
