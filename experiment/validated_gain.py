"""
Attempt 2 of predicting the beam-width gain (definition frozen in
results/predict/DEV_LOG.md before this was run): the "validated first-rule
gain".

For each of the 10 training folds of seed 0, each of 3 inner stratified
grow (2/3) / validation (1/3) splits of that fold, and each class c:
learn CN2's first rule for c on the grow part with BeamSearch(1) and with
BeamSearch(20) (CN2's own settings: Laplace(n_classes), likelihood-ratio
filtering at 3.841, no depth limit), score both on the validation part with
the same Laplace, and take w20 minus w1. A missing rule counts as the empty
rule. Dataset score = mean over everything. Training data only.

    python validated_gain.py --datasets vote,monks-problems-2 --out results/predict/x.csv
"""

from __future__ import annotations

import argparse

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit

from pyrulearn.data.io import build_dataspec, encode
from pyrulearn.experiments.catalog import Catalog
from pyrulearn.experiments.runner import _stratified_folds
from pyrulearn.heuristics import Laplace, LikelihoodRatio, RuleStats
from pyrulearn.learners.seco import BeamSearch, EmptyRuleAllFeatures
from pyrulearn.pruning import ThresholdPrePruning
from pyrulearn.rule import Rule

INNER_SEEDS = (0, 1, 2)
SIGNIFICANCE = 3.841  # CN2's default threshold


def _inner_split(y, seed):
    """Stratified 2/3 grow, 1/3 validation; plain random if a class is too
    small to stratify (same fallback idea as run_cv)."""
    idx = np.arange(len(y))
    try:
        sss = StratifiedShuffleSplit(n_splits=1, test_size=1 / 3, random_state=seed)
        grow, val = next(sss.split(idx, y))
    except ValueError:
        rng = np.random.default_rng(seed)
        perm = rng.permutation(idx)
        cut = int(round(len(y) * 2 / 3))
        grow, val = perm[:cut], perm[cut:]
    g = np.zeros(len(y), bool)
    v = np.zeros(len(y), bool)
    g[grow] = True
    v[val] = True
    return g, v


def score_fold(data) -> float:
    y = np.asarray(data.y)
    classes = np.unique(y)
    h = Laplace(n_classes=max(2, len(classes)))
    filt = ThresholdPrePruning(LikelihoodRatio(), SIGNIFICANCE, operator="<")
    vals = []
    for seed in INNER_SEEDS:
        grow, val = _inner_split(y, seed)
        for c in classes:
            init = EmptyRuleAllFeatures().initial_candidates(data, c, grow)
            scores = {}
            for w in (1, 20):
                rule = BeamSearch(beam_width=w).search(data, c, h, init, example_mask=grow, filtering=filt)
                if rule is None:
                    rule = Rule([], target=c, dataspec=data.spec)
                scores[w] = float(h.score(RuleStats.from_rule(rule, data, c, example_mask=val)))
            vals.append(scores[20] - scores[1])
    return float(np.mean(vals))


def dataset_score(name: str, folds: int = 10, seed: int = 0) -> float:
    entry = Catalog.default().select(names=[name])[0]
    df, target = entry.load()
    vals = []
    for train_idx, _ in _stratified_folds(df[target].to_numpy(), folds, seed):
        tr = df.iloc[train_idx].reset_index(drop=True)
        spec = build_dataspec(tr, target=target, skip_unusable=True).build()
        vals.append(score_fold(encode(spec, tr, tr[target].to_numpy())))
    return float(np.mean(vals))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--datasets", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    rows = []
    for name in [n.strip() for n in args.datasets.split(",")]:
        s = dataset_score(name)
        rows.append({"dataset": name, "score": s})
        print(f"{name:40s} validated first-rule gain {s:+.5f}", flush=True)
        pd.DataFrame(rows).to_csv(args.out, index=False)


if __name__ == "__main__":
    main()
