# CN2 beam width: results

Generated 2026-11-12 16:41 · pyrulearn 0.6.0 · Python 3.12.12 · arm64

## Setup

- Learner: `CN2(beam_width=w)` for w in [1, 5, 10, 20], all other settings library defaults.
- Datasets: vote, breast-cancer, tic-tac-toe, monks-problems-2, heart-c, credit-approval, diabetes, iris, lymph, glass, car.
- 10-fold stratified CV, shuffled with random_state=2; identical folds for every width.
- Fit timeout 600s per fit; 1 fit(s) at a time.
- Values are mean ± sd across folds (sd = spread over folds, not a standard error).

## Per dataset

| dataset | w | accuracy | rules | conditions | fit time (s) | failed folds |
|---|--:|--:|--:|--:|--:|--:|
| breast-cancer | 1 | 74.1 ± 4.8% | 8.4 ± 2.2 | 11.2 ± 4.9 | 0.01 ± 0.00 | 0 |
| breast-cancer | 5 | 71.7 ± 5.9% | 40.3 ± 11.5 | 108.1 ± 33.7 | 0.10 ± 0.03 | 0 |
| breast-cancer | 10 | 69.9 ± 3.3% | 48.6 ± 6.2 | 126.5 ± 20.8 | 0.20 ± 0.04 | 0 |
| breast-cancer | 20 | 72.0 ± 3.1% | 51.0 ± 6.3 | 143.8 ± 17.8 | 0.34 ± 0.05 | 0 |
| car | 1 | 94.0 ± 1.6% | 102.9 ± 2.9 | 542.5 ± 17.8 | 0.16 ± 0.01 | 0 |
| car | 5 | 94.4 ± 1.6% | 80.5 ± 2.6 | 432.1 ± 14.6 | 0.22 ± 0.01 | 0 |
| car | 10 | 95.4 ± 1.2% | 72.4 ± 2.9 | 397.0 ± 15.9 | 0.30 ± 0.02 | 0 |
| car | 20 | 95.3 ± 1.3% | 69.0 ± 2.4 | 384.4 ± 13.9 | 0.47 ± 0.01 | 0 |
| credit-approval | 1 | 84.5 ± 4.6% | 66.9 ± 6.9 | 180.3 ± 22.5 | 0.10 ± 0.01 | 0 |
| credit-approval | 5 | 83.3 ± 5.3% | 98.7 ± 10.0 | 291.4 ± 31.3 | 0.28 ± 0.06 | 0 |
| credit-approval | 10 | 83.5 ± 4.6% | 101.4 ± 4.5 | 307.6 ± 18.5 | 0.45 ± 0.09 | 0 |
| credit-approval | 20 | 83.5 ± 4.0% | 100.1 ± 6.0 | 311.2 ± 20.0 | 0.74 ± 0.19 | 0 |
| diabetes | 1 | 73.8 ± 2.9% | 82.7 ± 16.5 | 243.8 ± 55.9 | 0.13 ± 0.04 | 0 |
| diabetes | 5 | 75.1 ± 3.7% | 106.7 ± 11.9 | 353.9 ± 50.0 | 0.42 ± 0.07 | 0 |
| diabetes | 10 | 75.9 ± 3.4% | 116.1 ± 10.1 | 394.7 ± 44.1 | 0.72 ± 0.10 | 0 |
| diabetes | 20 | 74.5 ± 4.7% | 121.2 ± 12.5 | 424.7 ± 62.9 | 1.45 ± 0.39 | 0 |
| glass | 1 | 71.6 ± 6.5% | 44.8 ± 2.3 | 150.4 ± 7.5 | 0.09 ± 0.01 | 0 |
| glass | 5 | 70.2 ± 9.2% | 37.1 ± 1.8 | 128.4 ± 9.3 | 0.17 ± 0.02 | 0 |
| glass | 10 | 70.2 ± 10.3% | 35.3 ± 2.3 | 119.8 ± 5.8 | 0.28 ± 0.04 | 0 |
| glass | 20 | 71.5 ± 7.7% | 33.3 ± 1.3 | 114.7 ± 3.6 | 0.49 ± 0.08 | 0 |
| heart-c | 1 | 77.3 ± 7.7% | 48.7 ± 10.2 | 131.0 ± 35.9 | 0.06 ± 0.02 | 0 |
| heart-c | 5 | 81.3 ± 7.5% | 53.5 ± 1.9 | 154.7 ± 8.6 | 0.12 ± 0.01 | 0 |
| heart-c | 10 | 79.3 ± 7.2% | 52.0 ± 4.4 | 154.4 ± 18.4 | 0.17 ± 0.02 | 0 |
| heart-c | 20 | 77.0 ± 9.0% | 48.1 ± 3.3 | 148.6 ± 11.6 | 0.26 ± 0.04 | 0 |
| iris | 1 | 91.3 ± 8.3% | 12.4 ± 1.3 | 29.1 ± 3.0 | 0.01 ± 0.00 | 0 |
| iris | 5 | 92.7 ± 6.6% | 9.1 ± 0.7 | 21.2 ± 2.4 | 0.01 ± 0.00 | 0 |
| iris | 10 | 93.3 ± 5.4% | 8.8 ± 0.4 | 20.0 ± 1.9 | 0.02 ± 0.01 | 0 |
| iris | 20 | 94.0 ± 5.8% | 8.0 ± 0.5 | 18.0 ± 2.0 | 0.03 ± 0.01 | 0 |
| lymph | 1 | 79.0 ± 10.4% | 22.5 ± 2.5 | 48.9 ± 7.1 | 0.02 ± 0.00 | 0 |
| lymph | 5 | 81.9 ± 10.9% | 19.0 ± 0.9 | 50.8 ± 2.8 | 0.03 ± 0.01 | 0 |
| lymph | 10 | 80.6 ± 10.0% | 16.8 ± 1.4 | 48.5 ± 3.4 | 0.04 ± 0.01 | 0 |
| lymph | 20 | 86.7 ± 8.3% | 15.4 ± 1.1 | 46.6 ± 3.4 | 0.06 ± 0.01 | 0 |
| monks-problems-2 | 1 | 68.6 ± 8.8% | 88.3 ± 33.0 | 437.7 ± 177.8 | 0.14 ± 0.05 | 0 |
| monks-problems-2 | 5 | 90.3 ± 4.4% | 83.3 ± 8.7 | 420.8 ± 46.7 | 0.18 ± 0.03 | 0 |
| monks-problems-2 | 10 | 94.3 ± 3.9% | 72.6 ± 5.1 | 359.3 ± 27.6 | 0.22 ± 0.02 | 0 |
| monks-problems-2 | 20 | 97.0 ± 2.7% | 60.7 ± 4.1 | 291.9 ± 22.1 | 0.28 ± 0.03 | 0 |
| tic-tac-toe | 1 | 98.0 ± 1.5% | 40.6 ± 4.5 | 142.9 ± 16.9 | 0.05 ± 0.01 | 0 |
| tic-tac-toe | 5 | 98.2 ± 1.3% | 30.0 ± 2.7 | 103.9 ± 9.8 | 0.06 ± 0.01 | 0 |
| tic-tac-toe | 10 | 98.4 ± 1.2% | 26.8 ± 1.7 | 92.6 ± 5.8 | 0.07 ± 0.01 | 0 |
| tic-tac-toe | 20 | 98.4 ± 1.2% | 26.1 ± 1.3 | 90.5 ± 4.8 | 0.12 ± 0.01 | 0 |
| vote | 1 | 95.2 ± 2.0% | 27.5 ± 2.1 | 88.0 ± 7.1 | 0.03 ± 0.00 | 0 |
| vote | 5 | 95.2 ± 3.2% | 27.6 ± 2.0 | 88.3 ± 7.5 | 0.04 ± 0.00 | 0 |
| vote | 10 | 94.0 ± 2.7% | 25.8 ± 2.6 | 83.8 ± 9.5 | 0.07 ± 0.01 | 0 |
| vote | 20 | 93.6 ± 2.4% | 25.1 ± 2.1 | 82.1 ± 8.5 | 0.11 ± 0.02 | 0 |

## Failures

None: every fit finished within the timeout without an error.

## Across datasets

Mean rank per width (1 = best; ties averaged; computed on per-dataset means):

| width | accuracy rank | fewest conditions rank | fastest rank | accuracy wins |
|--:|--:|--:|--:|--:|
| 1 | 2.82 | 2.73 | 1.00 | 4.0 |
| 5 | 2.73 | 3.00 | 2.00 | 1.0 |
| 10 | 2.27 | 2.36 | 3.00 | 2.5 |
| 20 | 2.18 | 1.91 | 4.00 | 3.5 |

- Friedman test on accuracy: chi² = 2.06, p = 0.561 (11 datasets, 4 widths).
- Friedman test on n_conditions: chi² = 4.42, p = 0.220 (11 datasets, 4 widths).
- With few datasets the Friedman test has little power: p > 0.05 means *no evidence* of a difference, not evidence of none.
