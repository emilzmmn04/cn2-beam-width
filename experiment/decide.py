"""
Apply DECISION_RULE.md to the beam-width runs, mechanically.

    python decide.py phase2:0 seed1:1 seed2:2      # tag:seed pairs

Per seed: Friedman p on accuracy over the 4 widths, the winner (best mean
accuracy rank), and the winner's median per-dataset gain over w=1. Then the
verdict across seeds. Supplementary numbers (not used to decide) follow.
Writes results/decision.md.
"""

from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

from pyrulearn.experiments.stats import friedman_test, mean_rank

HERE = os.path.dirname(os.path.abspath(__file__))
WIDTH_LEARNERS = ["CN2 (w=1)", "CN2 (w=5)", "CN2 (w=10)", "CN2 (w=20)"]
ALPHA, MIN_GAIN_PP = 0.05, 1.0


def per_seed(results: pd.DataFrame) -> dict:
    results = results[results.learner.isin(WIDTH_LEARNERS)]
    means = results.pivot_table(index="dataset", columns="learner", values="accuracy", aggfunc="mean")
    f = friedman_test(results, "accuracy")
    ranks = mean_rank(results, "accuracy")
    winner = ranks.index[0]
    gain = 100 * (means[winner] - means["CN2 (w=1)"])
    passes_p = f.pvalue < ALPHA
    passes_gain = winner != "CN2 (w=1)" and gain.median() >= MIN_GAIN_PP
    return {"p": f.pvalue, "n_datasets": f.n_datasets, "ranks": ranks, "winner": winner,
            "median_gain": gain.median(), "mean_gain": gain.mean(), "gain": gain,
            "passes_p": passes_p, "passes_gain": passes_gain, "passes": passes_p and passes_gain}


def main(pairs):
    runs = {}
    for pair in pairs:
        tag, seed = pair.split(":")
        runs[int(seed)] = (tag, pd.read_csv(os.path.join(HERE, "results", tag, "results.csv")))

    lines = ["# Decision (rule: DECISION_RULE.md)", "",
             f"Rule per seed: Friedman p < {ALPHA} **and** winner wider than 1 with median gain over w=1 "
             f">= {MIN_GAIN_PP} pp. Established only if every seed passes.", "",
             "| seed | datasets | Friedman p | part 1 | winner | median gain | part 2 | seed passes |",
             "|--:|--:|--:|:-:|---|--:|:-:|:-:|"]
    verdicts, out = [], {}
    for seed in sorted(runs):
        tag, res = runs[seed]
        r = out[seed] = per_seed(res)
        verdicts.append(r["passes"])
        lines.append(f"| {seed} | {r['n_datasets']} | {r['p']:.3f} | {'yes' if r['passes_p'] else 'no'} | "
                     f"{r['winner']} | {r['median_gain']:+.2f} pp | {'yes' if r['passes_gain'] else 'no'} | "
                     f"**{'yes' if r['passes'] else 'no'}** |")
    if all(verdicts):
        verdict = "ESTABLISHED: wider beams are better (all seeds pass)."
    elif any(verdicts):
        verdict = "NOT ESTABLISHED: inconsistent across seeds (some pass, some don't)."
    else:
        verdict = "NOT ESTABLISHED: no seed passes the rule."
    lines += ["", f"**Verdict: {verdict}**", ""]

    lines += ["## Supplementary (not used to decide)", "",
              "Mean accuracy rank per width (1 = best), per seed:", "",
              "| seed | " + " | ".join(w.replace("CN2 ", "") for w in WIDTH_LEARNERS) + " | mean gain of winner |",
              "|--:|" + "--:|" * (len(WIDTH_LEARNERS) + 1)]
    for seed, r in out.items():
        lines.append(f"| {seed} | " + " | ".join(f"{r['ranks'][w]:.2f}" for w in WIDTH_LEARNERS)
                     + f" | {r['mean_gain']:+.2f} pp |")

    allres = pd.concat([res.assign(seed=s) for s, (_, res) in runs.items()], ignore_index=True)
    allres = allres[allres.learner.isin(WIDTH_LEARNERS)]
    acc = allres.pivot_table(index=["dataset", "seed"], columns="learner", values="accuracy", aggfunc="mean")
    per_ds = acc.groupby(level=0).agg(["mean", "std"])
    lines += ["", "Per dataset: mean accuracy over seeds (± sd of the per-seed means = how much the split matters):",
              "", "| dataset | " + " | ".join(w.replace("CN2 ", "") for w in WIDTH_LEARNERS) + " |",
              "|---|" + "--:|" * len(WIDTH_LEARNERS)]
    for ds, row in per_ds.iterrows():
        lines.append(f"| {ds} | " + " | ".join(
            f"{100 * row[(w, 'mean')]:.1f} ± {100 * row[(w, 'std')]:.1f}" for w in WIDTH_LEARNERS) + " |")
    pooled = allres.groupby(["dataset", "learner"], as_index=False).accuracy.mean()
    fp = friedman_test(pooled, "accuracy")
    lines += ["", f"Friedman on accuracy averaged over the seeds: p = {fp.pvalue:.3f} "
              f"({fp.n_datasets} datasets). Averaging seeds makes per-dataset means more stable, "
              "but the datasets (not the seeds) are the sample, so this is still an 11-dataset test."]

    path = os.path.join(HERE, "results", "decision.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main(sys.argv[1:] or ["phase2:0", "seed1:1", "seed2:2"])
