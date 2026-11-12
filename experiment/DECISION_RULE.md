# Decision rule (fixed 2026-11-12, before seeds 1 and 2 were run)

Question: does a wider beam make CN2 better, in general?

**Primary measure:** held-out accuracy. Fit time and model size are reported
but do not decide the question.

"Wider beams are better" counts as **established** only if, for **each** of
the three fold splits (seeds 0, 1, 2) on the same 11 datasets:

1. **Real, not luck:** Friedman test on accuracy over the 4 widths
   (1, 5, 10, 20) gives p < 0.05;
2. **Big enough to matter:** the width with the best mean accuracy rank
   (the "winner") is wider than 1, and its *median* per-dataset gain over
   w=1 is at least 1.0 percentage point;
3. **Holds up:** 1 and 2 hold for all three seeds.

If some seeds pass and others don't: **inconsistent, not established**.

Not part of the rule (reported, never used to decide): the mean gain,
win counts, per-dataset results, the pooled-over-seeds Friedman test, and
the exact-search reference (`optimal_reference.py`), which only covers
vote, iris and monks-problems-2 because exact search is too slow elsewhere.

## Honesty note

The rule was written after seeing the seed-0 results (phase 2), which
already fail parts 1 and 2 (p = 0.10, median gain +0.8 pp). So for seed 0
it is not a blind test; seeds 1 and 2 are. The rule was not tuned to make
seed 0 pass or fail: the thresholds are the conventional p < 0.05 and a
1 pp gain proposed before discussing any threshold alternatives.
