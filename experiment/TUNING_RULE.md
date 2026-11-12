# Option D: decision rule (fixed 2026-11-12, before the nested-CV run)

Learner: `TunedCN2` (`tuned.py`): inside each outer training fold, 5-fold
stratified inner CV (inner seed 0) over widths 1, 5, 10, 20; best mean
inner accuracy wins, ties go to the smaller width; refit on the whole outer
training fold. Outer evaluation: the same 11 datasets, 10 folds, seeds
0, 1, 2 as before (identical outer folds), fit timeout 600 s.

**Question 1 (primary): does letting the data choose beat the default?**
Comparison: `TunedCN2` vs `CN2(beam_width=5)`, the library default.
"Tuning is better" counts as **established** only if on **each** seed:
Wilcoxon signed-rank test over the 11 per-dataset mean accuracies gives
p < 0.05 (two-sided; zero differences dropped, scipy's default) **and**
the median per-dataset gain is ≥ 1 pp. Same thresholds as DECISION_RULE.md.

**Question 2 (practical): does the data choose about as well as hindsight?**
"Oracle" = for each dataset, the fixed width with the best mean outer test
accuracy over the 3 seeds. This peeks at test data, so it is an upper bound
no real method can use. "Tuning is close to the oracle" counts as
**established** if, averaged over the 3 seeds, `TunedCN2` is within 1 pp of
the oracle on at least 9 of the 11 datasets.

Reported but not deciding: tuned vs w=1 and vs w=20 (same test), which
widths were chosen and how often, fit time, rules, conditions.

Nothing here is changed after the nested-CV results are seen.
