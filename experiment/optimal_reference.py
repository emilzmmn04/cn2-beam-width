"""
Exact-search reference ("beam width infinity") for the CN2 beam-width study.

`CN2(search=BranchAndBoundSearch())` finds the best-scoring significant rule
in every covering step -- no local-maximum trap in the single-rule search.
It is exponential in the worst case: on fold 0, one fit took 2.5 s (vote),
7.8 s (iris) and 11.5 s (monks-problems-2) and over 90 s on the other 8
phase-2 datasets, so it only runs on those three by default.

Kept separate from run_experiment.py on purpose: the decision-rule
statistics (Friedman over 4 widths, 11 datasets) must not change because
this learner only finishes on some datasets.

    python optimal_reference.py --tag phase2 --seed 0     # needs results/phase2/results.csv
    python optimal_reference.py --tag seed1  --seed 1

Writes results/<tag>/optimal/: results_optimal.csv, optimal.md, accuracy.png.
Same folds as the beam-width run of that tag (same run_cv, same seed).
"""

from __future__ import annotations

import argparse
import os
import sys

import numpy as np
import pandas as pd

from pyrulearn.experiments.catalog import Catalog
from pyrulearn.experiments.runner import run_cv

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from labeled import LabeledCN2Optimal  # noqa: E402
from run_experiment import COLORS, INK, INK_2, MARKERS, _pm, _style  # noqa: E402

OPT = "CN2 (optimal)"
ORDER = ["CN2 (w=1)", "CN2 (w=5)", "CN2 (w=10)", "CN2 (w=20)", OPT]
SHORT = {"CN2 (w=1)": "1", "CN2 (w=5)": "5", "CN2 (w=10)": "10", "CN2 (w=20)": "20", OPT: "opt"}
COLOR = {**{f"CN2 (w={w})": c for w, c in COLORS.items()}, OPT: "#e87ba4"}
MARKER = {**{f"CN2 (w={w})": m for w, m in MARKERS.items()}, OPT: "*"}


def paired(results, a, b, ds):
    p = results[results.dataset == ds].pivot(index="fold", columns="learner", values="accuracy")
    if a not in p or b not in p:
        return "n/a"
    d = (p[a] - p[b]).dropna()
    return f"{(d > 1e-9).sum()} / {(d.abs() <= 1e-9).sum()} / {(d < -1e-9).sum()}"


def write_md(both, path, args):
    lines = [f"# Exact-search reference (seed {args.seed})", "",
             "`CN2(search=BranchAndBoundSearch())`: the best significant rule by Laplace in every covering",
             "step. Same folds as the beam widths. **Not part of the decision rule** (see DECISION_RULE.md).", "",
             "| dataset | learner | accuracy | rules | conditions | fit time (s) | failed folds |",
             "|---|---|--:|--:|--:|--:|--:|"]
    for ds in dict.fromkeys(both.dataset):
        for lr in ORDER:
            g = both[(both.dataset == ds) & (both.learner == lr)]
            if g.empty:
                continue
            ok = g[g.error.isna()]
            lines.append(
                f"| {ds} | {SHORT[lr]} | {_pm(100 * ok.accuracy.mean(), 100 * ok.accuracy.std(), '{:.1f}')}% | "
                f"{_pm(ok.n_rules.mean(), ok.n_rules.std(), '{:.1f}')} | "
                f"{_pm(ok.n_conditions.mean(), ok.n_conditions.std(), '{:.1f}')} | "
                f"{_pm(ok.fit_time.mean(), ok.fit_time.std(), '{:.2f}')} | {int(g.error.notna().sum())} |")
    lines += ["", "Folds where optimal is better / same / worse than ...", "",
              "| dataset | vs w=1 | vs w=20 |", "|---|:-:|:-:|"]
    for ds in dict.fromkeys(both.dataset):
        lines.append(f"| {ds} | {paired(both, OPT, 'CN2 (w=1)', ds)} | {paired(both, OPT, 'CN2 (w=20)', ds)} |")
    errs = both[(both.learner == OPT) & both.error.notna()]
    if not errs.empty:
        lines += ["", "Failures: " + "; ".join(f"{d}: {e}" for d, e in
                                              errs.groupby("dataset").error.first().items())]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def plot(both, path):
    import matplotlib.pyplot as plt

    datasets = list(dict.fromkeys(both.dataset))
    fig, axes = plt.subplots(1, len(datasets), figsize=(3.4 * len(datasets) + 0.6, 3.2), squeeze=False)
    for ax, ds in zip(axes.flat, datasets):
        for x, lr in enumerate(ORDER):
            g = both[(both.dataset == ds) & (both.learner == lr) & both.error.isna()]
            if g.empty:
                continue
            ax.errorbar(x, 100 * g.accuracy.mean(), yerr=100 * g.accuracy.std(), fmt=MARKER[lr],
                        color=COLOR[lr], markersize=9 if lr == OPT else 7, linewidth=2, capsize=3,
                        markeredgecolor="white", markeredgewidth=1)
        ax.axvline(3.5, color=INK_2, linewidth=0.8, linestyle=":")
        ax.set_xticks(range(len(ORDER)), [SHORT[lr] for lr in ORDER])
        ax.set_title(ds, fontsize=9, color=INK, loc="left")
        ax.set_xlabel("beam width  |  exact", fontsize=9, color=INK_2)
        _style(ax)
    axes[0, 0].set_ylabel("held-out accuracy (%)", fontsize=9, color=INK_2)
    fig.suptitle("CN2: beam widths vs exact (optimal) search, mean ± sd over folds",
                 fontsize=10, color=INK, x=0.02, ha="left")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--datasets", default="vote,iris,monks-problems-2")
    p.add_argument("--tag", required=True, help="beam-width run to compare against: results/<tag>/")
    p.add_argument("--seed", type=int, required=True, help="must match that run's --seed")
    p.add_argument("--folds", type=int, default=10)
    p.add_argument("--timeout", type=float, default=300.0)
    args = p.parse_args()

    names = [n.strip() for n in args.datasets.split(",")]
    widths = pd.read_csv(os.path.join(HERE, "results", args.tag, "results.csv"))
    opt = run_cv([LabeledCN2Optimal()], Catalog.default().select(names=names), n_folds=args.folds,
                 fit_timeout=args.timeout, random_state=args.seed, cache_dir=os.path.join(HERE, "_cache"))
    out = os.path.join(HERE, "results", args.tag, "optimal")
    os.makedirs(out, exist_ok=True)
    opt.to_csv(os.path.join(out, "results_optimal.csv"), index=False)
    both = pd.concat([widths[widths.dataset.isin(names)], opt], ignore_index=True)
    write_md(both, os.path.join(out, "optimal.md"), args)
    plot(both, os.path.join(out, "accuracy.png"))
    print(f"\nwrote {out}/")


if __name__ == "__main__":
    main()
