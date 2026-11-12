# CN2 beam width: results

Generated 2026-11-12 16:39 · pyrulearn 0.6.0 · Python 3.12.12 · arm64

## Setup

- Learner: `CN2(beam_width=w)` for w in [1, 5, 10, 20], all other settings library defaults.
- Datasets: vote, breast-cancer, tic-tac-toe, monks-problems-2, heart-c, credit-approval, diabetes, iris, lymph, glass, car.
- 10-fold stratified CV, shuffled with random_state=1; identical folds for every width.
- Fit timeout 600s per fit; 1 fit(s) at a time.
- Values are mean ± sd across folds (sd = spread over folds, not a standard error).

## Per dataset

| dataset | w | accuracy | rules | conditions | fit time (s) | failed folds |
|---|--:|--:|--:|--:|--:|--:|
| breast-cancer | 1 | 73.5 ± 6.0% | 9.0 ± 3.0 | 13.3 ± 7.7 | 0.01 ± 0.00 | 0 |
| breast-cancer | 5 | 72.4 ± 6.2% | 41.9 ± 8.9 | 111.3 ± 30.2 | 0.10 ± 0.02 | 0 |
| breast-cancer | 10 | 73.8 ± 7.0% | 49.9 ± 6.5 | 134.7 ± 20.6 | 0.18 ± 0.03 | 0 |
| breast-cancer | 20 | 73.1 ± 6.7% | 55.2 ± 4.0 | 164.2 ± 17.0 | 0.37 ± 0.04 | 0 |
| car | 1 | 94.5 ± 2.2% | 103.8 ± 4.8 | 543.6 ± 28.0 | 0.16 ± 0.01 | 0 |
| car | 5 | 95.2 ± 1.5% | 80.7 ± 3.4 | 433.9 ± 17.1 | 0.21 ± 0.01 | 0 |
| car | 10 | 94.9 ± 1.8% | 74.1 ± 2.4 | 407.5 ± 15.6 | 0.29 ± 0.01 | 0 |
| car | 20 | 95.3 ± 2.3% | 69.6 ± 2.5 | 389.5 ± 15.5 | 0.46 ± 0.02 | 0 |
| credit-approval | 1 | 86.1 ± 4.9% | 66.7 ± 9.2 | 179.1 ± 31.2 | 0.11 ± 0.02 | 0 |
| credit-approval | 5 | 84.6 ± 4.1% | 96.6 ± 8.0 | 283.1 ± 29.7 | 0.29 ± 0.03 | 0 |
| credit-approval | 10 | 83.2 ± 3.1% | 100.7 ± 3.9 | 302.4 ± 17.3 | 0.50 ± 0.11 | 0 |
| credit-approval | 20 | 83.0 ± 3.7% | 101.1 ± 6.9 | 315.3 ± 26.6 | 0.81 ± 0.15 | 0 |
| diabetes | 1 | 75.3 ± 4.9% | 89.0 ± 14.0 | 268.0 ± 54.5 | 0.14 ± 0.03 | 0 |
| diabetes | 5 | 75.8 ± 3.9% | 115.8 ± 8.3 | 394.3 ± 34.5 | 0.43 ± 0.04 | 0 |
| diabetes | 10 | 76.2 ± 5.0% | 124.3 ± 9.1 | 431.3 ± 45.1 | 0.81 ± 0.15 | 0 |
| diabetes | 20 | 75.7 ± 4.3% | 131.1 ± 11.8 | 481.7 ± 64.4 | 1.40 ± 0.32 | 0 |
| glass | 1 | 69.7 ± 8.7% | 43.7 ± 3.9 | 153.3 ± 21.8 | 0.10 ± 0.01 | 0 |
| glass | 5 | 71.5 ± 9.9% | 38.0 ± 2.5 | 126.7 ± 8.8 | 0.18 ± 0.02 | 0 |
| glass | 10 | 70.1 ± 8.2% | 36.0 ± 1.3 | 123.8 ± 9.1 | 0.29 ± 0.03 | 0 |
| glass | 20 | 71.1 ± 7.7% | 33.8 ± 1.8 | 116.1 ± 6.6 | 0.53 ± 0.07 | 0 |
| heart-c | 1 | 77.3 ± 10.1% | 47.6 ± 9.0 | 124.5 ± 30.6 | 0.06 ± 0.02 | 0 |
| heart-c | 5 | 79.9 ± 6.3% | 53.8 ± 2.8 | 155.5 ± 10.3 | 0.12 ± 0.02 | 0 |
| heart-c | 10 | 78.9 ± 6.7% | 51.2 ± 4.9 | 155.4 ± 17.0 | 0.18 ± 0.06 | 0 |
| heart-c | 20 | 79.6 ± 6.7% | 49.7 ± 4.4 | 152.7 ± 13.5 | 0.29 ± 0.06 | 0 |
| iris | 1 | 93.3 ± 7.0% | 12.2 ± 1.2 | 28.8 ± 3.7 | 0.01 ± 0.00 | 0 |
| iris | 5 | 92.7 ± 6.6% | 9.1 ± 1.0 | 20.9 ± 2.2 | 0.02 ± 0.01 | 0 |
| iris | 10 | 92.7 ± 6.6% | 8.4 ± 1.1 | 19.1 ± 2.8 | 0.02 ± 0.01 | 0 |
| iris | 20 | 93.3 ± 5.4% | 8.0 ± 0.8 | 17.8 ± 1.5 | 0.04 ± 0.03 | 0 |
| lymph | 1 | 78.5 ± 8.0% | 23.2 ± 2.9 | 52.3 ± 8.6 | 0.02 ± 0.01 | 0 |
| lymph | 5 | 80.5 ± 7.2% | 18.8 ± 1.4 | 51.9 ± 2.3 | 0.03 ± 0.00 | 0 |
| lymph | 10 | 81.8 ± 8.3% | 16.9 ± 1.1 | 47.6 ± 3.0 | 0.04 ± 0.01 | 0 |
| lymph | 20 | 81.9 ± 10.9% | 15.9 ± 0.9 | 46.9 ± 2.4 | 0.07 ± 0.01 | 0 |
| monks-problems-2 | 1 | 73.0 ± 9.0% | 99.9 ± 35.8 | 496.8 ± 191.3 | 0.16 ± 0.06 | 0 |
| monks-problems-2 | 5 | 89.5 ± 3.4% | 84.7 ± 5.7 | 428.3 ± 31.7 | 0.19 ± 0.02 | 0 |
| monks-problems-2 | 10 | 92.2 ± 3.2% | 72.9 ± 4.2 | 361.7 ± 23.7 | 0.23 ± 0.02 | 0 |
| monks-problems-2 | 20 | 96.3 ± 2.5% | 60.9 ± 3.2 | 292.4 ± 18.2 | 0.30 ± 0.02 | 0 |
| tic-tac-toe | 1 | 97.4 ± 1.7% | 41.7 ± 4.9 | 147.0 ± 18.2 | 0.05 ± 0.01 | 0 |
| tic-tac-toe | 5 | 98.0 ± 1.0% | 30.2 ± 1.9 | 104.5 ± 7.1 | 0.06 ± 0.00 | 0 |
| tic-tac-toe | 10 | 98.2 ± 1.0% | 27.0 ± 1.9 | 93.3 ± 6.7 | 0.07 ± 0.01 | 0 |
| tic-tac-toe | 20 | 98.3 ± 1.0% | 26.3 ± 1.7 | 91.1 ± 6.1 | 0.11 ± 0.01 | 0 |
| vote | 1 | 94.7 ± 2.9% | 26.7 ± 2.3 | 86.3 ± 8.4 | 0.02 ± 0.00 | 0 |
| vote | 5 | 95.0 ± 3.0% | 27.2 ± 2.0 | 87.1 ± 7.0 | 0.04 ± 0.00 | 0 |
| vote | 10 | 94.5 ± 2.5% | 25.6 ± 1.2 | 83.2 ± 4.6 | 0.06 ± 0.01 | 0 |
| vote | 20 | 94.7 ± 2.7% | 25.0 ± 1.3 | 81.6 ± 4.8 | 0.11 ± 0.01 | 0 |

## Failures

None: every fit finished within the timeout without an error.

## Across datasets

Mean rank per width (1 = best; ties averaged; computed on per-dataset means):

| width | accuracy rank | fewest conditions rank | fastest rank | accuracy wins |
|--:|--:|--:|--:|--:|
| 1 | 3.14 | 2.82 | 1.00 | 1.5 |
| 5 | 2.32 | 2.91 | 2.00 | 3.0 |
| 10 | 2.50 | 2.36 | 3.00 | 2.0 |
| 20 | 2.05 | 1.91 | 4.00 | 4.5 |

- Friedman test on accuracy: chi² = 4.33, p = 0.228 (11 datasets, 4 widths).
- Friedman test on n_conditions: chi² = 4.20, p = 0.241 (11 datasets, 4 widths).
- With few datasets the Friedman test has little power: p > 0.05 means *no evidence* of a difference, not evidence of none.
