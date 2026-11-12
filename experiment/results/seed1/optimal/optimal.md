# Exact-search reference (seed 1)

`CN2(search=BranchAndBoundSearch())`: the best significant rule by Laplace in every covering
step. Same folds as the beam widths. **Not part of the decision rule** (see DECISION_RULE.md).

| dataset | learner | accuracy | rules | conditions | fit time (s) | failed folds |
|---|---|--:|--:|--:|--:|--:|
| vote | 1 | 94.7 ± 2.9% | 26.7 ± 2.3 | 86.3 ± 8.4 | 0.02 ± 0.00 | 0 |
| vote | 5 | 95.0 ± 3.0% | 27.2 ± 2.0 | 87.1 ± 7.0 | 0.04 ± 0.00 | 0 |
| vote | 10 | 94.5 ± 2.5% | 25.6 ± 1.2 | 83.2 ± 4.6 | 0.06 ± 0.01 | 0 |
| vote | 20 | 94.7 ± 2.7% | 25.0 ± 1.3 | 81.6 ± 4.8 | 0.11 ± 0.01 | 0 |
| vote | opt | 94.2 ± 2.7% | 24.0 ± 1.8 | 90.6 ± 6.8 | 3.91 ± 1.78 | 0 |
| monks-problems-2 | 1 | 73.0 ± 9.0% | 99.9 ± 35.8 | 496.8 ± 191.3 | 0.16 ± 0.06 | 0 |
| monks-problems-2 | 5 | 89.5 ± 3.4% | 84.7 ± 5.7 | 428.3 ± 31.7 | 0.19 ± 0.02 | 0 |
| monks-problems-2 | 10 | 92.2 ± 3.2% | 72.9 ± 4.2 | 361.7 ± 23.7 | 0.23 ± 0.02 | 0 |
| monks-problems-2 | 20 | 96.3 ± 2.5% | 60.9 ± 3.2 | 292.4 ± 18.2 | 0.30 ± 0.02 | 0 |
| monks-problems-2 | opt | 98.8 ± 1.4% | 41.5 ± 0.5 | 213.4 ± 4.9 | 9.17 ± 0.47 | 0 |
| iris | 1 | 93.3 ± 7.0% | 12.2 ± 1.2 | 28.8 ± 3.7 | 0.01 ± 0.00 | 0 |
| iris | 5 | 92.7 ± 6.6% | 9.1 ± 1.0 | 20.9 ± 2.2 | 0.02 ± 0.01 | 0 |
| iris | 10 | 92.7 ± 6.6% | 8.4 ± 1.1 | 19.1 ± 2.8 | 0.02 ± 0.01 | 0 |
| iris | 20 | 93.3 ± 5.4% | 8.0 ± 0.8 | 17.8 ± 1.5 | 0.04 ± 0.03 | 0 |
| iris | opt | 94.7 ± 5.3% | 7.8 ± 0.6 | 28.8 ± 2.1 | 15.44 ± 34.09 | 0 |

Folds where optimal is better / same / worse than ...

| dataset | vs w=1 | vs w=20 |
|---|:-:|:-:|
| vote | 3 / 2 / 5 | 3 / 2 / 5 |
| monks-problems-2 | 10 / 0 / 0 | 8 / 2 / 0 |
| iris | 4 / 4 / 2 | 2 / 8 / 0 |
