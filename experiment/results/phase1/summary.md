# CN2 beam width: results

Generated 2026-11-12 15:53 · pyrulearn 0.6.0 · Python 3.12.12 · arm64

## Setup

- Learner: `CN2(beam_width=w)` for w in [1, 5, 10, 20], all other settings library defaults.
- Datasets: vote.
- 10-fold stratified CV, shuffled with random_state=0; identical folds for every width.
- Fit timeout 600s per fit; 1 fit(s) at a time.
- Values are mean ± sd across folds (sd = spread over folds, not a standard error).

## Per dataset

| dataset | w | accuracy | rules | conditions | fit time (s) | failed folds |
|---|--:|--:|--:|--:|--:|--:|
| vote | 1 | 94.7 ± 3.2% | 26.4 ± 2.1 | 83.9 ± 7.4 | 0.02 ± 0.00 | 0 |
| vote | 5 | 94.5 ± 3.6% | 26.3 ± 1.3 | 84.9 ± 4.9 | 0.04 ± 0.00 | 0 |
| vote | 10 | 94.0 ± 3.3% | 25.1 ± 1.6 | 81.2 ± 6.1 | 0.06 ± 0.01 | 0 |
| vote | 20 | 94.5 ± 3.1% | 24.4 ± 2.0 | 79.8 ± 6.6 | 0.11 ± 0.02 | 0 |

## Failures

None: every fit finished within the timeout without an error.

Only one dataset: no across-dataset statistics (ranks/Friedman need several).
