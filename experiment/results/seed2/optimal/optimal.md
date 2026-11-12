# Exact-search reference (seed 2)

`CN2(search=BranchAndBoundSearch())`: the best significant rule by Laplace in every covering
step. Same folds as the beam widths. **Not part of the decision rule** (see DECISION_RULE.md).

| dataset | learner | accuracy | rules | conditions | fit time (s) | failed folds |
|---|---|--:|--:|--:|--:|--:|
| vote | 1 | 95.2 ± 2.0% | 27.5 ± 2.1 | 88.0 ± 7.1 | 0.03 ± 0.00 | 0 |
| vote | 5 | 95.2 ± 3.2% | 27.6 ± 2.0 | 88.3 ± 7.5 | 0.04 ± 0.00 | 0 |
| vote | 10 | 94.0 ± 2.7% | 25.8 ± 2.6 | 83.8 ± 9.5 | 0.07 ± 0.01 | 0 |
| vote | 20 | 93.6 ± 2.4% | 25.1 ± 2.1 | 82.1 ± 8.5 | 0.11 ± 0.02 | 0 |
| vote | opt | 93.8 ± 2.9% | 24.5 ± 2.0 | 92.4 ± 9.5 | 4.51 ± 1.42 | 0 |
| monks-problems-2 | 1 | 68.6 ± 8.8% | 88.3 ± 33.0 | 437.7 ± 177.8 | 0.14 ± 0.05 | 0 |
| monks-problems-2 | 5 | 90.3 ± 4.4% | 83.3 ± 8.7 | 420.8 ± 46.7 | 0.18 ± 0.03 | 0 |
| monks-problems-2 | 10 | 94.3 ± 3.9% | 72.6 ± 5.1 | 359.3 ± 27.6 | 0.22 ± 0.02 | 0 |
| monks-problems-2 | 20 | 97.0 ± 2.7% | 60.7 ± 4.1 | 291.9 ± 22.1 | 0.28 ± 0.03 | 0 |
| monks-problems-2 | opt | 99.2 ± 1.2% | 41.3 ± 0.5 | 213.2 ± 5.4 | 9.10 ± 0.39 | 0 |
| iris | 1 | 91.3 ± 8.3% | 12.4 ± 1.3 | 29.1 ± 3.0 | 0.01 ± 0.00 | 0 |
| iris | 5 | 92.7 ± 6.6% | 9.1 ± 0.7 | 21.2 ± 2.4 | 0.01 ± 0.00 | 0 |
| iris | 10 | 93.3 ± 5.4% | 8.8 ± 0.4 | 20.0 ± 1.9 | 0.02 ± 0.01 | 0 |
| iris | 20 | 94.0 ± 5.8% | 8.0 ± 0.5 | 18.0 ± 2.0 | 0.03 ± 0.01 | 0 |
| iris | opt | 92.7 ± 4.9% | 7.9 ± 0.3 | 28.0 ± 4.9 | 6.27 ± 10.01 | 0 |

Folds where optimal is better / same / worse than ...

| dataset | vs w=1 | vs w=20 |
|---|:-:|:-:|
| vote | 2 / 2 / 6 | 2 / 6 / 2 |
| monks-problems-2 | 10 / 0 / 0 | 5 / 5 / 0 |
| iris | 2 / 7 / 1 | 0 / 8 / 2 |
