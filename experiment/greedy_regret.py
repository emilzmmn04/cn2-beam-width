"""
The "greedy regret" score: how much does greedy search lose in its first
`depth` steps, compared with the exact best rule of at most `depth`
conditions?

For one training set and one target class:

    regret = Laplace(best rule with <= depth conditions, exact)
           - Laplace(rule greedy search reaches within depth conditions)

both found by pyrulearn's own searches (`BranchAndBoundSearch(max_conditions=
depth)` and `BeamSearch(beam_width=1, max_conditions=depth)`), with CN2's
heuristic `Laplace(n_classes=c)`, from the empty rule, on all training rows,
no significance test. The dataset's score is the mean over classes and over
the 10 training folds of seed 0 (training data only: a user could compute it
before choosing a beam width).

    python greedy_regret.py --datasets vote,monks-problems-2 --depth 2
"""

from __future__ import annotations

import argparse
import os
import sys

import numpy as np
import pandas as pd

from pyrulearn.data.io import build_dataspec, encode
from pyrulearn.experiments.catalog import Catalog
from pyrulearn.experiments.runner import _stratified_folds
from pyrulearn.heuristics import Laplace
from pyrulearn.learners.seco import BeamSearch, BranchAndBoundSearch, EmptyRuleAllFeatures
from pyrulearn.heuristics import RuleStats

HERE = os.path.dirname(os.path.abspath(__file__))


def rule_score(data, target, heuristic, rule) -> float:
    if rule is None:
        return np.nan
    return float(heuristic.score(RuleStats.from_rule(rule, data, target)))


def regret_one(data, depth: int) -> float:
    classes = np.unique(np.asarray(data.y))
    h = Laplace(n_classes=max(2, len(classes)))
    out = []
    for c in classes:
        init = EmptyRuleAllFeatures().initial_candidates(data, c, None)
        exact = BranchAndBoundSearch(max_conditions=depth).search(data, c, h, init)
        greedy = BeamSearch(beam_width=1, max_conditions=depth).search(data, c, h, init)
        out.append(rule_score(data, c, h, exact) - rule_score(data, c, h, greedy))
    return float(np.nanmean(out))


def dataset_regret(name: str, depth: int, folds: int = 10, seed: int = 0) -> float:
    entry = Catalog.default().select(names=[name])[0]
    df, target = entry.load()
    vals = []
    for train_idx, _ in _stratified_folds(df[target].to_numpy(), folds, seed):
        tr = df.iloc[train_idx].reset_index(drop=True)
        spec = build_dataspec(tr, target=target, skip_unusable=True).build()
        vals.append(regret_one(encode(spec, tr, tr[target].to_numpy()), depth))
    return float(np.mean(vals))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--datasets", required=True)
    p.add_argument("--depth", type=int, default=2)
    p.add_argument("--out", help="CSV to write (dataset, depth, regret)")
    args = p.parse_args()
    rows = []
    for name in args.datasets.split(","):
        r = dataset_regret(name.strip(), args.depth)
        rows.append({"dataset": name.strip(), "depth": args.depth, "regret": r})
        print(f"{name:35s} depth {args.depth}: regret {r:.5f}", flush=True)
    if args.out:
        pd.DataFrame(rows).to_csv(args.out, index=False)


if __name__ == "__main__":
    main()
