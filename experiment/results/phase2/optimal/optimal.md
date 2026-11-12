# Exact-search reference (seed 0)

`CN2(search=BranchAndBoundSearch())`: the best significant rule by Laplace in every covering
step. Same folds as the beam widths. **Not part of the decision rule** (see DECISION_RULE.md).

| dataset | learner | accuracy | rules | conditions | fit time (s) | failed folds |
|---|---|--:|--:|--:|--:|--:|
| vote | 1 | 94.7 ± 3.2% | 26.4 ± 2.1 | 83.9 ± 7.4 | 0.02 ± 0.00 | 0 |
| vote | 5 | 94.5 ± 3.6% | 26.3 ± 1.3 | 84.9 ± 4.9 | 0.04 ± 0.00 | 0 |
| vote | 10 | 94.0 ± 3.3% | 25.1 ± 1.6 | 81.2 ± 6.1 | 0.06 ± 0.01 | 0 |
| vote | 20 | 94.5 ± 3.1% | 24.4 ± 2.0 | 79.8 ± 6.6 | 0.11 ± 0.02 | 0 |
| vote | opt | 93.8 ± 2.2% | 24.1 ± 2.1 | 91.5 ± 9.3 | 3.70 ± 1.37 | 0 |
| monks-problems-2 | 1 | 70.0 ± 10.2% | 91.6 ± 32.0 | 457.9 ± 173.2 | 0.14 ± 0.04 | 0 |
| monks-problems-2 | 5 | 90.0 ± 3.4% | 84.6 ± 5.8 | 427.2 ± 32.1 | 0.19 ± 0.02 | 0 |
| monks-problems-2 | 10 | 92.2 ± 3.4% | 72.1 ± 5.7 | 356.2 ± 31.8 | 0.22 ± 0.02 | 0 |
| monks-problems-2 | 20 | 94.8 ± 4.0% | 62.7 ± 4.1 | 301.9 ± 23.1 | 0.30 ± 0.02 | 0 |
| monks-problems-2 | opt | 98.5 ± 1.2% | 41.6 ± 0.5 | 214.0 ± 5.5 | 9.30 ± 0.52 | 0 |
| iris | 1 | 93.3 ± 6.3% | 12.3 ± 0.8 | 28.5 ± 2.7 | 0.01 ± 0.00 | 0 |
| iris | 5 | 92.7 ± 5.8% | 8.7 ± 1.1 | 20.0 ± 2.4 | 0.01 ± 0.01 | 0 |
| iris | 10 | 92.7 ± 5.8% | 8.5 ± 1.0 | 19.4 ± 2.3 | 0.02 ± 0.01 | 0 |
| iris | 20 | 92.7 ± 5.8% | 8.0 ± 0.7 | 18.0 ± 1.2 | 0.03 ± 0.02 | 0 |
| iris | opt | 92.7 ± 5.8% | 7.9 ± 0.6 | 29.1 ± 4.0 | 8.23 ± 16.96 | 0 |

Folds where optimal is better / same / worse than ...

| dataset | vs w=1 | vs w=20 |
|---|:-:|:-:|
| vote | 1 / 5 / 4 | 1 / 5 / 4 |
| monks-problems-2 | 10 / 0 / 0 | 6 / 4 / 0 |
| iris | 1 / 6 / 3 | 1 / 6 / 3 |
