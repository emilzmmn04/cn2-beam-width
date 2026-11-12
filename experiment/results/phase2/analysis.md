# CN2 beam width: analysis of phase 2

Data: `summary.md` / `results.csv` in this folder. 11 datasets (7 binary,
4 multiclass), 10-fold stratified CV, one fold split (seed 0), widths 1, 5,
10, 20, all other CN2 settings default. No fit failed or timed out.

## Context per dataset

"pp per person" = how many percentage points one test example is worth in
one fold; differences smaller than that on average are about one example.

| dataset | rows | majority class | pp per person | w=20 vs w=1, folds better / same / worse | mean Δ accuracy |
|---|--:|--:|--:|:-:|--:|
| monks-problems-2 | 601 | 65.7% | 1.7 | 10 / 0 / 0 | **+24.8 pp** |
| lymph | 148 | 54.7% | 6.8 | 7 / 3 / 0 | +8.8 pp |
| breast-cancer | 286 | 70.3% | 3.5 | 7 / 1 / 2 | +4.6 pp |
| heart-c | 303 | 54.5% | 3.3 | 5 / 0 / 5 | +1.3 pp |
| car | 1728 | 70.0% | 0.6 | 8 / 0 / 2 | +1.0 pp |
| glass | 214 | 35.5% | 4.7 | 3 / 6 / 1 | +1.0 pp |
| diabetes | 768 | 65.1% | 1.3 | 5 / 1 / 4 | +0.8 pp |
| tic-tac-toe | 958 | 65.3% | 1.0 | 2 / 7 / 1 | +0.1 pp |
| vote | 435 | 61.4% | 2.3 | 2 / 6 / 2 | −0.2 pp |
| credit-approval | 690 | 55.5% | 1.4 | 4 / 1 / 5 | −0.3 pp |
| iris | 150 | 33.3% | 6.7 | 0 / 9 / 1 | −0.7 pp |

## Findings

**1. Accuracy: wider was usually not worse, sometimes much better, and the
effect is very uneven.** Mean accuracy rank improves with width (3.27, 2.41,
2.27, 2.05 for w = 1, 5, 10, 20), but the Friedman test over the 11 datasets
gives p = 0.10. By the usual 0.05 threshold this is *not* evidence of a
general difference. The average gain of w=20 over w=1 is +3.7 pp, but that
mean is pulled up by one dataset; the median gain is +0.95 pp (glass; just below 1 pp). On 3 of 11
datasets w=20 was slightly worse on average (all within one test example
per fold).

**2. One clear, large effect: monks-problems-2 (+24.8 pp, better on all 10
folds).** Its target concept is "exactly two of the six attributes have
their first value". No single condition says much about that, so the first
greedy step has nothing good to follow, and greedy search ends up memorizing
small fragments (fold 0: 86 rules of 3–4 examples each, 70.5% accuracy). The
w=20 rules have the shape of the true concept, for example
`attr1≠1 ∧ attr2≠1 ∧ attr3=2 ∧ attr4=2 ∧ attr5=1 ∧ attr6=1` (exactly two
attributes =1), and reach 93.4%. This is the "greedy local optimum" case in
its clearest form.

**3. Breast-cancer: greedy CN2 is no better than always guessing the
majority class.** w=1 reaches 69.6%, and the majority class alone is 70.3%.
On fold 0 its rules include `inv-nodes ≠ 0-2 → no-recurrence (32/35)` and
the same body for the other class, i.e. rules that cover more of the wrong
class than the right one. w=20 learns 47 mostly pure rules and reaches 74.2%
on average. *Hypothesis (not tested):* along one greedy path the pure
refinements quickly become too small to pass the significance test, so the
best significant rule on that path is a weak short one; a wider beam sees
more paths and finds pure rules that are still significant.

**4. Model size moves in opposite directions depending on the dataset.** On
7 datasets (car, iris, tic-tac-toe, monks-2, glass, lymph, vote) wider beams
gave *smaller* models (down to about 0.65× the conditions). On 4
(breast-cancer about 13×, credit-approval, diabetes, heart-c about 1.3–1.8×)
they gave *larger* ones. All four "larger" datasets are binary with
accuracies below 90%, but so is no simple rule: glass (72%) and lymph (84%)
are also below 90% and got *smaller* models. What separates the two groups
is not yet clear: three of the four "larger" ones (credit-approval,
diabetes, heart-c) have discretized numeric attributes, but glass is all
numeric and went the other way. Friedman on
conditions: p = 0.53, i.e. no consistent direction across datasets, which is
expected when the direction depends on the dataset.

**5. Fit time is the only consistent effect.** w=20 was the slowest on every
dataset (mean rank 4.00), typically 2–10× w=1, not 20×: `BeamSearch`'s
optimistic pruning stops early when no beam member can still win. The
outlier is breast-cancer (about 37×), where the model itself became about 5×
larger, so the covering loop ran many more searches. Absolute times stay
below 1.5 s per fit everywhere.

**6. Not monotone.** On lymph and heart-c, w=5 beats w=10. With 15 and 30
test examples per fold (6.8 and 3.3 pp per example), and sds of 5–15 pp,
these zig-zags are within the noise. Nothing here supports "a specific
middle width is best".

## Against the proposed decision rule

The rule, since fixed in `../../DECISION_RULE.md`: primary measure accuracy;
Friedman p < 0.05, and the winner's median gain over w=1 ≥ 1 pp, on each of
seeds 0–2. Seed 0: ranks favour wider beams, but p = 0.10 misses the bar.
The median gain of the winner (w=20) is +0.95 pp (glass), just below 1 pp;
the mean (+3.7) is above it but is pulled up by a few datasets. Seed 0 does
not pass. (An earlier draft of this file said the median was +0.8 pp; that
was a misreading, corrected here.)

## Limitations

- One fold split (seed 0). Fold-to-fold sds are large on the small datasets
  (lymph, iris, glass, heart-c); a second and third seed would show how
  stable the per-dataset means are.
- 11 datasets give the Friedman test little power; p = 0.10 is "unclear",
  not "no effect".
- Dataset choice is not random: monks-2 and tic-tac-toe were added because
  they were expected to be hard for greedy search. Average effects are
  therefore not an estimate for "typical" data.
- Fit time includes sending the data to the worker process; ratios are more
  meaningful than seconds. Fits ran one at a time on one machine (arm64).
- Numeric attributes are discretized per fold (`TreeDiscretizer`); results on
  diabetes/credit-approval/heart-c/glass are for that encoding, not raw
  numeric data.
- Mechanism claims (findings 2–3) come from inspecting fold 0 only.

## Follow-up research questions supported by these observations

1. **When does greedy search fail?** monks-2 (+25 pp) and vote (±0) differ in
   whether any single condition is informative about the class. Does a
   simple dataset statistic, e.g. the best single-condition Laplace or
   information gain relative to the best two-condition rule, predict how
   much a wider beam helps? Testable on the artificial `deep` datasets in the
   catalog, where the concept's structure is known.
2. **Is the significance test what makes greedy CN2 fail on noisy data?**
   Repeat breast-cancer, credit-approval, diabetes and heart-c with
   `significance_threshold=None` and with the test as `stopping` instead of
   `filtering`. If the w=1 vs w=20 gap shrinks without the test, finding 3's
   hypothesis is supported.
3. **Does searching closer to the optimum keep helping, or start to
   overfit?** Add `CN2(search=BranchAndBoundSearch())` (the exact optimal rule
   per covering step) as "w=∞" and track *training* Laplace of the learned
   rules next to held-out accuracy. A growing gap between the two would be
   the oversearching effect (Quinlan & Cameron-Jones, 1995).
