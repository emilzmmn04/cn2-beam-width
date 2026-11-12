# CN2 beam width: results

Generated 2026-11-12 16:18 · pyrulearn 0.6.0 · Python 3.12.12 · arm64

## Setup

- Learner: `CN2(beam_width=w)` for w in [1, 5, 10, 20], all other settings library defaults.
- Datasets: vote, breast-cancer, tic-tac-toe, monks-problems-2, heart-c, credit-approval, diabetes, iris, lymph, glass, car.
- 10-fold stratified CV, shuffled with random_state=0; identical folds for every width.
- Fit timeout 600s per fit; 1 fit(s) at a time.
- Values are mean ± sd across folds (sd = spread over folds, not a standard error).

## Per dataset

| dataset | w | accuracy | rules | conditions | fit time (s) | failed folds |
|---|--:|--:|--:|--:|--:|--:|
| breast-cancer | 1 | 69.6 ± 7.4% | 8.4 ± 2.2 | 11.7 ± 5.9 | 0.01 ± 0.00 | 0 |
| breast-cancer | 5 | 69.9 ± 6.6% | 35.0 ± 10.1 | 91.0 ± 29.1 | 0.08 ± 0.03 | 0 |
| breast-cancer | 10 | 73.1 ± 6.8% | 48.5 ± 6.8 | 131.4 ± 24.4 | 0.17 ± 0.03 | 0 |
| breast-cancer | 20 | 74.2 ± 6.2% | 52.8 ± 4.0 | 153.7 ± 17.1 | 0.33 ± 0.05 | 0 |
| car | 1 | 94.3 ± 1.6% | 104.9 ± 2.5 | 548.2 ± 12.3 | 0.16 ± 0.01 | 0 |
| car | 5 | 94.9 ± 1.4% | 82.1 ± 3.0 | 440.2 ± 15.7 | 0.22 ± 0.01 | 0 |
| car | 10 | 95.6 ± 1.1% | 73.8 ± 1.5 | 405.7 ± 8.8 | 0.29 ± 0.01 | 0 |
| car | 20 | 95.3 ± 1.2% | 70.8 ± 2.1 | 392.9 ± 11.0 | 0.47 ± 0.02 | 0 |
| credit-approval | 1 | 84.3 ± 4.4% | 64.2 ± 7.3 | 171.2 ± 20.3 | 0.10 ± 0.02 | 0 |
| credit-approval | 5 | 86.2 ± 5.6% | 92.1 ± 15.2 | 270.0 ± 50.5 | 0.30 ± 0.06 | 0 |
| credit-approval | 10 | 84.8 ± 4.7% | 101.0 ± 5.3 | 304.8 ± 18.0 | 0.48 ± 0.05 | 0 |
| credit-approval | 20 | 84.1 ± 3.9% | 99.2 ± 3.5 | 308.6 ± 15.1 | 0.83 ± 0.10 | 0 |
| diabetes | 1 | 73.4 ± 5.4% | 86.8 ± 11.3 | 262.3 ± 51.9 | 0.13 ± 0.02 | 0 |
| diabetes | 5 | 73.6 ± 4.5% | 106.6 ± 17.2 | 352.0 ± 79.6 | 0.42 ± 0.11 | 0 |
| diabetes | 10 | 74.1 ± 4.1% | 121.6 ± 14.5 | 429.5 ± 73.9 | 0.73 ± 0.14 | 0 |
| diabetes | 20 | 74.2 ± 4.5% | 128.6 ± 10.9 | 471.2 ± 51.8 | 1.37 ± 0.16 | 0 |
| glass | 1 | 72.0 ± 6.5% | 45.0 ± 3.2 | 158.9 ± 17.5 | 0.10 ± 0.02 | 0 |
| glass | 5 | 71.1 ± 8.5% | 38.0 ± 3.3 | 131.0 ± 14.9 | 0.20 ± 0.04 | 0 |
| glass | 10 | 73.0 ± 10.5% | 35.8 ± 2.4 | 120.7 ± 11.9 | 0.32 ± 0.08 | 0 |
| glass | 20 | 72.9 ± 4.9% | 32.7 ± 2.8 | 112.2 ± 8.7 | 0.57 ± 0.14 | 0 |
| heart-c | 1 | 77.6 ± 6.2% | 46.7 ± 5.6 | 121.3 ± 21.2 | 0.06 ± 0.01 | 0 |
| heart-c | 5 | 82.2 ± 5.0% | 51.7 ± 4.3 | 148.4 ± 16.6 | 0.12 ± 0.01 | 0 |
| heart-c | 10 | 77.9 ± 8.8% | 50.7 ± 4.8 | 148.9 ± 16.0 | 0.17 ± 0.02 | 0 |
| heart-c | 20 | 78.9 ± 8.7% | 48.4 ± 3.1 | 150.2 ± 10.5 | 0.27 ± 0.02 | 0 |
| iris | 1 | 93.3 ± 6.3% | 12.3 ± 0.8 | 28.5 ± 2.7 | 0.01 ± 0.00 | 0 |
| iris | 5 | 92.7 ± 5.8% | 8.7 ± 1.1 | 20.0 ± 2.4 | 0.01 ± 0.01 | 0 |
| iris | 10 | 92.7 ± 5.8% | 8.5 ± 1.0 | 19.4 ± 2.3 | 0.02 ± 0.01 | 0 |
| iris | 20 | 92.7 ± 5.8% | 8.0 ± 0.7 | 18.0 ± 1.2 | 0.03 ± 0.02 | 0 |
| lymph | 1 | 74.5 ± 14.9% | 23.9 ± 2.5 | 55.8 ± 8.3 | 0.02 ± 0.00 | 0 |
| lymph | 5 | 84.0 ± 8.9% | 18.5 ± 1.1 | 50.2 ± 3.6 | 0.03 ± 0.00 | 0 |
| lymph | 10 | 78.5 ± 8.7% | 16.9 ± 1.2 | 47.7 ± 4.1 | 0.04 ± 0.01 | 0 |
| lymph | 20 | 83.3 ± 13.8% | 16.0 ± 1.3 | 47.4 ± 5.0 | 0.07 ± 0.02 | 0 |
| monks-problems-2 | 1 | 70.0 ± 10.2% | 91.6 ± 32.0 | 457.9 ± 173.2 | 0.14 ± 0.04 | 0 |
| monks-problems-2 | 5 | 90.0 ± 3.4% | 84.6 ± 5.8 | 427.2 ± 32.1 | 0.19 ± 0.02 | 0 |
| monks-problems-2 | 10 | 92.2 ± 3.4% | 72.1 ± 5.7 | 356.2 ± 31.8 | 0.22 ± 0.02 | 0 |
| monks-problems-2 | 20 | 94.8 ± 4.0% | 62.7 ± 4.1 | 301.9 ± 23.1 | 0.30 ± 0.02 | 0 |
| tic-tac-toe | 1 | 98.2 ± 1.2% | 41.3 ± 4.8 | 145.3 ± 17.0 | 0.05 ± 0.01 | 0 |
| tic-tac-toe | 5 | 98.3 ± 1.3% | 28.6 ± 1.6 | 98.8 ± 6.2 | 0.05 ± 0.00 | 0 |
| tic-tac-toe | 10 | 98.3 ± 1.4% | 26.8 ± 1.9 | 92.4 ± 6.9 | 0.07 ± 0.01 | 0 |
| tic-tac-toe | 20 | 98.3 ± 1.4% | 26.3 ± 2.0 | 91.0 ± 7.3 | 0.11 ± 0.01 | 0 |
| vote | 1 | 94.7 ± 3.2% | 26.4 ± 2.1 | 83.9 ± 7.4 | 0.02 ± 0.00 | 0 |
| vote | 5 | 94.5 ± 3.6% | 26.3 ± 1.3 | 84.9 ± 4.9 | 0.04 ± 0.00 | 0 |
| vote | 10 | 94.0 ± 3.3% | 25.1 ± 1.6 | 81.2 ± 6.1 | 0.06 ± 0.01 | 0 |
| vote | 20 | 94.5 ± 3.1% | 24.4 ± 2.0 | 79.8 ± 6.6 | 0.11 ± 0.02 | 0 |

## Failures

None: every fit finished within the timeout without an error.

## Across datasets

Mean rank per width (1 = best; ties averaged; computed on per-dataset means):

| width | accuracy rank | fewest conditions rank | fastest rank | accuracy wins |
|--:|--:|--:|--:|--:|
| 1 | 3.27 | 2.82 | 1.00 | 2.0 |
| 5 | 2.41 | 2.73 | 2.00 | 3.3 |
| 10 | 2.27 | 2.36 | 3.00 | 2.3 |
| 20 | 2.05 | 2.09 | 4.00 | 3.3 |

- Friedman test on accuracy: chi² = 6.21, p = 0.102 (11 datasets, 4 widths).
- Friedman test on n_conditions: chi² = 2.24, p = 0.525 (11 datasets, 4 widths).
- With few datasets the Friedman test has little power: p > 0.05 means *no evidence* of a difference, not evidence of none.
