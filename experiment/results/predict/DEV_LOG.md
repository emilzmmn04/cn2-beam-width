# Predicting the beam-width gain: development log

Every score tried on the 11 development datasets is listed here, including
failures, so the number of attempts is visible (each extra attempt on the same
11 datasets makes a lucky fit more likely). No held-out dataset has been run.

Target: gain = accuracy(w=20) − accuracy(w=1), mean of seeds 0–2 (pp).

## Attempt 1 (2026-11-12): greedy regret, depth 2 and 3 (`greedy_regret.py`)

Score: Laplace(exact best rule with ≤ d conditions) − Laplace(greedy rule
within d conditions), per class, mean over classes and the 10 training folds
of seed 0.

| depth | Spearman ρ vs gain | p |
|--:|--:|--:|
| 2 | +0.23 | 0.50 |
| 3 | +0.28 | 0.40 |

**Failed on development data.** Not taken to the test datasets.

Why, from the table (`dev_regret_d2.csv`, `dev_regret_d3.csv`):

- monks-problems-2 (gain +25.5 pp) scores in the middle. Its concept needs
  six conditions; at depth 2–3 greedy and exact search barely differ, so
  depth ≤ 3 cannot see the trap.
- breast-cancer, glass and iris score highest but gain < 1 pp. On small or
  noisy data, exact search finds tiny pure pockets (e.g. 5 covered, 0 wrong)
  with a higher Laplace than greedy's broader rule. Those pockets are
  training-set accidents: a "regret" on training data that does not exist
  on test data. The score measures *search* difficulty, the gain measures
  *generalization*, and noise separates the two.

## Attempt 2 (defined 2026-11-12, before computing it): validated first-rule gain

Last development attempt (agreed cap: one more try after attempt 1).

Score (`validated_gain.py`): for each of the 10 training folds of seed 0, and
each of 3 inner stratified splits of that training fold into grow (2/3) and
validation (1/3) (inner random_state 0, 1, 2), and each class c:

1. On the grow part, learn CN2's *first* rule for c twice, with CN2's own
   single-rule settings (Laplace(n_classes), likelihood-ratio filtering at
   3.841, no depth limit): once with `BeamSearch(1)`, once with
   `BeamSearch(20)`.
2. Score both rules on the validation part with the same Laplace.
3. value = Laplace_val(w=20 rule) − Laplace_val(w=1 rule); a missing rule
   (nothing significant) counts as the empty rule.

Dataset score = mean over classes, inner splits and folds. Uses training data
only.

Caveat, stated in advance: unlike attempt 1 this uses the beam itself (on
one rule, inside the training data), so it is closer to the quantity being
predicted. A success would show that "the first rule's held-out quality"
predicts the whole model's gain, not that a simple data property does.

Development criterion: Spearman ρ ≥ 0.5 between score and gain on the 11
development datasets. If not met: stop, report, no test run.

## Frozen test protocol (only run if attempt 2 passes development)

Test datasets (never run before in this project), 34:

- `deep`-tagged, small/medium, not in development: artificial-nnf-{5, 16,
  19, 24, 36, 44, 53, 57, 60, 65, 68, 69, 70, 81, 82, 85, 89, 107, 112,
  118}, kr-vs-kp, monks-problems-1, monks-problems-3, mushroom
  (car-binary excluded: derived from car, which is in development);
- 10 drawn at random (numpy default_rng(2026), without replacement) from
  the 68 small/medium catalog datasets that are neither in development nor
  `deep`-tagged: MiceProtein, analcatdata_dmft,
  blood-transfusion-service-center, first-order-theorem-proving,
  hayes-roth, hypothyroid, mofn-3-7-10, pc1, segment, zoo.

Gain per test dataset: CN2 w=20 minus w=1, 10-fold CV, seeds 0, 1, 2, mean
(same as development). Fit timeout 300 s; a dataset where either width
times out on any seed is excluded from the correlation and listed.

**Success on test:** Spearman ρ ≥ 0.5 **and** two-sided p < 0.05 between the
attempt-2 score and the gain, over all non-excluded test datasets. Otherwise
the prediction is not supported. Nothing about the score or the protocol is
changed after test results are seen.

## Attempt 2: result

| score | Spearman ρ vs gain (11 dev datasets) | p | criterion ρ ≥ 0.5 |
|---|--:|--:|:-:|
| validated first-rule gain | +0.36 | 0.29 | **not met** |

**Failed on development data. Per the protocol: stop, no test run.** The 34
test datasets remain unused (`dev_validated_gain.csv` has the scores).

What changed against attempt 1, and what didn't:

- Fixed: monks-problems-2 now has the highest score (0.124) and vote the
  lowest (0.006), the two ends that attempt 1 got wrong or flat.
- Still wrong: lymph (gain +6.6 pp, the second largest) scores second
  lowest; iris (gain +0.7) scores second highest; credit-approval (gain
  −1.4) is mid-range.
- Observation (descriptive, not tested): the score is positive on **all 11**
  datasets, i.e. on held-out training rows the w=20 first rule beat the w=1
  first rule on average everywhere, while the whole model's gain was near 0
  on most datasets. A better *first* rule does not reliably make a better
  *rule set*; whatever decides the final gain happens later, in the covering
  loop (which examples remain, which rules follow, how they vote).

## Conclusion of the prediction study

Two pre-specified scores, both computed from training data only, failed to
predict on the development datasets where the gain of a wider beam is
known. With the agreed cap of two attempts reached, the question "can the
beam-width gain be predicted from a cheap training-data score?" is answered
*no, not with these scores*; the test set was not used, so it is still
available for a future, pre-registered score.
