# CN2 beam width: final analysis (seeds 0–2)

**Question.** Does a wider beam (1, 5, 10, 20) make CN2 better? Measured:
held-out accuracy (primary), rules, conditions, fit time.

**Setup.** pyrulearn `main` @ 873e4ed, `CN2(beam_width=w)` with all other
settings at their defaults. 11 OpenML datasets (7 binary, 4 multiclass),
10-fold stratified CV, three fold splits (seeds 0, 1, 2): 1,320 fits, none
failed. Exact search (`BranchAndBoundSearch`, "w=∞") as a separate reference
on vote, iris and monks-problems-2 only (360 more fits, none failed).
Numbers: `decision.md`, `<tag>/summary.md`, `<tag>/optimal/optimal.md`.

## Verdict under the decision rule

| seed | Friedman p (need < 0.05) | winner | median gain over w=1 (need ≥ 1 pp) | passes |
|--:|--:|---|--:|:-:|
| 0 | 0.102 | w=20 | +0.95 pp | no |
| 1 | 0.301 | w=20 | +0.75 pp | no |
| 2 | 0.561 | w=20 | +0.42 pp | no |

**Not established: no seed passes.** With these 11 datasets there is no
evidence that wider beams are better *in general*. This is not evidence that
they are equal: the Friedman test over 11 datasets has little power, and the
gains are concentrated on a few datasets (finding 2).

## Findings

1. **The direction is stable, the size is not.** w=20 had the best mean
   accuracy rank on all three seeds and w=1 the worst on all three
   (`decision.md`). But p moved from 0.10 to 0.56 and the median gain from
   +0.95 to +0.42 pp depending only on how the folds were cut, a reminder
   that one CV run is one sample.

2. **Large gains on few datasets, nothing on most.** w=20 minus w=1,
   averaged over the three seeds (`report_gain_w20.png`): monks-problems-2
   **+25.5 pp**, lymph +6.6, heart-c +1.1, car +1.0, glass +0.8,
   breast-cancer +0.7, iris +0.7, diabetes +0.6, tic-tac-toe +0.5,
   vote −0.6, credit-approval −1.4. The median dataset gains +0.7 pp.

3. **breast-cancer was a seed-0 artefact.** Seed 0 showed +4.6 pp for w=20;
   over three seeds it is +0.7 pp (w=1 72.4 ± 2.5, w=20 73.1 ± 1.1). The
   phase-2 explanation (greedy CN2 at the majority-class baseline) is
   therefore not supported as a general effect; it described one split.

4. **monks-problems-2 is the clear case of a greedy local optimum.** Its
   concept ("exactly two of six attributes equal their first value") gives
   no single condition any signal, so greedy search memorizes fragments
   (≈ 90 rules, sd ≈ 33 across folds). Accuracy rises at every width:
   70.5 → 90.0 → 92.9 → 96.1%, and exact search reaches **98.5–99.2%** with
   ≈ 41 rules, better than w=1 on all 30 folds and never worse than w=20.

5. **Exact search is not better everywhere: on vote it is slightly worse.**
   Over 30 folds, exact search vs w=1 on vote: better 6, same 9, worse 15;
   mean −0.9 pp. Its rule sets have fewer rules (≈ 24 vs 27) but more
   conditions (≈ 91 vs 86): the Laplace optimum is a narrower, purer rule.
   On iris it is mixed (7 / 17 / 6, +0.7 pp), again with fewer but longer
   rules (≈ 29 conditions vs ≈ 18 for w=20). This is *consistent with*
   oversearching (finding the best training score picks rules that fit the
   training data too narrowly) but two datasets and 30 non-independent folds
   are not proof.

6. **Model size depends on the dataset, not only on the width.** Wider beams
   shrank models on 7 datasets and grew them on 4 (seed 0; see
   `phase2/analysis.md`, finding 4). No simple attribute (binary/multiclass,
   numeric/categorical, accuracy level) separated the two groups.

7. **Cost.** w=20 was the slowest on every dataset in every seed, typically
   2–10× w=1 (not 20×: the beam search's optimistic pruning stops early).
   Exact search took 3.7–15 s per fit where it finished (≈ 30–400× w=20) and
   over 90 s on a single fold of the other 8 datasets.

## Limitations

- 11 datasets, chosen by hand, including two (monks-2, tic-tac-toe) picked
  because greedy search was expected to struggle. Not a random sample of
  "typical" data.
- The decision rule was written after seed 0 was seen; seeds 1 and 2 are the
  blind test (both fail it independently).
- Fold-level counts pooled over seeds (findings 4–5) count the same examples
  several times; they describe, they don't test.
- Exact search covers only the 3 datasets where it was affordable, all easy
  or artificial ones, so its results don't transfer to the other 8.
- `fit_time` includes sending data to the worker process; one machine
  (arm64), fits run one at a time.
- Environment: pandas pinned < 3 because of a scikit-learn ARFF parsing bug
  (README). Small classes in lymph (2 members) and glass (9) are below 10, so
  scikit-learn warned that stratification could not be exact there.
- Mechanism claims (monks-2 concept recovery) are from reading fold-0 rule
  sets, not from a measurement.

## Three follow-up research questions

1. **Can you predict, before training, whether a wider beam will help?**
   monks-2 (+25.5 pp) has no informative single condition; vote (−0.6 pp) has
   one condition that nearly decides the class. Measure, per dataset, the gap
   between the best one-condition rule and the best two-condition rule, and
   test whether it predicts the w=20 − w=1 gain. The catalog's 20 artificial
   `deep` datasets (known concepts) give a controlled testbed.

2. **Is there an oversearching point, and where?** Finding 5 hints that exact
   search loses accuracy on vote while gaining on monks-2. Record each rule
   set's *training* Laplace / training accuracy next to held-out accuracy for
   w = 1, 5, 10, 20, 50, ∞ and check whether the gap between training and
   test accuracy grows with search effort (Quinlan & Cameron-Jones, 1995).

3. **Does the significance test interact with the beam?** CN2 accepts only
   rules passing the likelihood-ratio test, and a wider beam reaches narrower
   rules that may or may not pass it. Repeat the 11 datasets with
   `significance_threshold=None` and with stricter thresholds (e.g. 6.63,
   p < 0.01) to see whether the beam-width effect (and the model-size
   increase on 4 datasets) changes.
