"""
Option D: nested cross-validation. Runs TunedCN2 (inner 5-fold CV chooses the
beam width from the training data) on the 11 datasets, seeds 0-2, with the
same outer folds as the fixed-width runs, then applies TUNING_RULE.md.

    python nested.py            # run + evaluate
    python nested.py --eval     # only evaluate cached runs

Writes results/nested/: seed<k>.csv, nested.md, chosen_widths.png, vs_oracle.png
"""

from __future__ import annotations

import argparse
import os
import sys

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon

from pyrulearn.experiments.catalog import Catalog
from pyrulearn.experiments.runner import run_cv

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from run_experiment import COLORS, GRID, INK, INK_2, _style  # noqa: E402
from tuned import TunedCN2, measure  # noqa: E402

DATASETS = ("vote,breast-cancer,tic-tac-toe,monks-problems-2,heart-c,credit-approval,diabetes,"
            "iris,lymph,glass,car").split(",")
FIXED_TAGS = {0: "phase2", 1: "seed1", 2: "seed2"}
TUNED = "CN2 (tuned)"
FIXED = ["CN2 (w=1)", "CN2 (w=5)", "CN2 (w=10)", "CN2 (w=20)"]
OUT = os.path.join(HERE, "results", "nested")


def run(timeout):
    os.makedirs(OUT, exist_ok=True)
    datasets = Catalog.default().select(names=DATASETS)
    for seed in FIXED_TAGS:
        res = run_cv([TunedCN2()], datasets, n_folds=10, fit_timeout=timeout, random_state=seed,
                     cache_dir=os.path.join(HERE, "_cache"), measure_fn=measure)
        res.to_csv(os.path.join(OUT, f"seed{seed}.csv"), index=False)


def load():
    frames = []
    for seed, tag in FIXED_TAGS.items():
        fixed = pd.read_csv(os.path.join(HERE, "results", tag, "results.csv"))
        tuned = pd.read_csv(os.path.join(OUT, f"seed{seed}.csv"))
        frames.append(pd.concat([fixed, tuned], ignore_index=True).assign(seed=seed))
    return pd.concat(frames, ignore_index=True)


def evaluate(df):
    acc = df.pivot_table(index=["seed", "dataset"], columns="learner", values="accuracy", aggfunc="mean")
    L = ["# Option D: nested cross-validation (rule: TUNING_RULE.md)", ""]
    fails = df[df.error.notna()]
    L += [f"Failed fits: {len(fails)}" + ("" if fails.empty else
          " -- " + "; ".join(f"{d}/{l}: {e}" for (d, l), e in fails.groupby(['dataset', 'learner']).error.first().items())), ""]

    # Question 1 (+ reported comparisons)
    L += ["## Question 1: tuned vs fixed widths (per seed, Wilcoxon over 11 datasets)", "",
          "| seed | vs | median gain | mean gain | tuned better / same / worse | Wilcoxon p | Q1 passes |",
          "|--:|---|--:|--:|:-:|--:|:-:|"]
    q1 = []
    for seed in FIXED_TAGS:
        a = acc.loc[seed]
        for base in ("CN2 (w=5)", "CN2 (w=1)", "CN2 (w=20)"):
            d = 100 * (a[TUNED] - a[base])
            nz = d[d.abs() > 1e-9]
            p = wilcoxon(nz).pvalue if len(nz) >= 1 else 1.0
            primary = base == "CN2 (w=5)"
            ok = primary and p < 0.05 and d.median() >= 1.0
            if primary:
                q1.append(ok)
            L.append(f"| {seed} | {base.replace('CN2 ', '')}{' (primary)' if primary else ''} | "
                     f"{d.median():+.2f} pp | {d.mean():+.2f} pp | "
                     f"{(d > 1e-9).sum()} / {(d.abs() <= 1e-9).sum()} / {(d < -1e-9).sum()} | {p:.3f} | "
                     f"{('**yes**' if ok else 'no') if primary else '–'} |")
    L += ["", f"**Q1 verdict: {'ESTABLISHED' if all(q1) else 'NOT ESTABLISHED'}** "
          f"(seeds passing: {sum(q1)} of {len(q1)}).", ""]

    # Question 2: oracle
    mean_over_seeds = acc.groupby(level="dataset").mean()
    oracle_width = mean_over_seeds[FIXED].idxmax(axis=1)
    oracle = mean_over_seeds[FIXED].max(axis=1)
    gap = 100 * (mean_over_seeds[TUNED] - oracle)
    within = int((gap >= -1.0).sum())
    L += ["## Question 2: tuned vs hindsight-best fixed width (oracle, mean of 3 seeds)", "",
          "| dataset | oracle width | oracle acc | tuned acc | tuned − oracle | w=5 − oracle |",
          "|---|---|--:|--:|--:|--:|"]
    for ds in gap.sort_values().index:
        L.append(f"| {ds} | {oracle_width[ds].replace('CN2 ', '')} | {100 * oracle[ds]:.1f}% | "
                 f"{100 * mean_over_seeds.loc[ds, TUNED]:.1f}% | {gap[ds]:+.2f} pp | "
                 f"{100 * (mean_over_seeds.loc[ds, 'CN2 (w=5)'] - oracle[ds]):+.2f} pp |")
    L += ["", f"Within 1 pp of the oracle: tuned on **{within} of 11** datasets "
          f"(w=5 alone: {int(((100 * (mean_over_seeds['CN2 (w=5)'] - oracle)) >= -1.0).sum())} of 11; "
          f"w=20 alone: {int(((100 * (mean_over_seeds['CN2 (w=20)'] - oracle)) >= -1.0).sum())} of 11).", "",
          f"**Q2 verdict: {'ESTABLISHED' if within >= 9 else 'NOT ESTABLISHED'}** (needs ≥ 9 of 11).", ""]

    # chosen widths and cost
    t = df[df.learner == TUNED]
    counts = t.groupby(["dataset", "tuned_width"]).size().unstack(fill_value=0)
    L += ["## Which width did the inner CV choose? (count over 30 outer folds)", "",
          "| dataset | " + " | ".join(f"w={int(w)}" for w in counts.columns) + " |",
          "|---|" + "--:|" * len(counts.columns)]
    for ds, row in counts.iterrows():
        L.append(f"| {ds} | " + " | ".join(str(v) for v in row) + " |")
    ft = df.pivot_table(index="dataset", columns="learner", values="fit_time", aggfunc="mean")
    ratio = (ft[TUNED] / ft["CN2 (w=5)"])
    L += ["", f"Fit time of tuned vs w=5: median {ratio.median():.1f}×, range {ratio.min():.1f}–{ratio.max():.1f}× "
          "(inner CV fits 4 widths × 5 folds + 1 refit).", ""]
    with open(os.path.join(OUT, "nested.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))
    plots(counts, gap, mean_over_seeds, oracle)


def plots(counts, gap, means, oracle):
    import matplotlib.pyplot as plt

    # 1. chosen widths: stacked horizontal bars, one row per dataset
    order = gap.sort_values().index.tolist()
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    left = np.zeros(len(order))
    for w in counts.columns:
        vals = counts.reindex(order)[w].to_numpy()
        ax.barh(range(len(order)), vals, left=left, color=COLORS[int(w)], edgecolor="white",
                linewidth=2, height=0.7, label=f"w={int(w)}")
        for i, v in enumerate(vals):
            if v >= 3:
                ax.text(left[i] + v / 2, i, str(int(v)), ha="center", va="center", fontsize=7, color=INK)
        left += vals
    ax.set_yticks(range(len(order)), order, fontsize=8)
    ax.set_xlabel("outer folds (3 seeds × 10)", fontsize=9, color=INK_2)
    _style(ax)
    ax.grid(axis="y", visible=False)
    ax.legend(fontsize=8, frameon=False, ncol=4, loc="lower left", bbox_to_anchor=(0, 1.0))
    fig.suptitle("Beam width chosen by inner cross-validation", fontsize=10, color=INK, x=0.02, ha="left")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(os.path.join(OUT, "chosen_widths.png"), dpi=130)
    plt.close(fig)

    # 2. gap to oracle: tuned vs fixed w=1 / w=5 / w=20, dot plot
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    series = [("CN2 (w=1)", COLORS[1], "o"), ("CN2 (w=5)", COLORS[5], "s"),
              ("CN2 (w=20)", COLORS[20], "D"), (TUNED, "#e87ba4", "*")]
    offs = np.linspace(-0.27, 0.27, len(series))
    for (lr, c, m), off in zip(series, offs):
        g = 100 * (means[lr] - oracle)
        ax.scatter(g.reindex(order), np.arange(len(order)) + off, color=c, marker=m,
                   s=70 if lr == TUNED else 30, edgecolor="white", linewidth=0.8,
                   label=lr.replace("CN2 (", "").rstrip(")"), zorder=3)
    ax.axvline(0, color=INK_2, linewidth=1)
    ax.axvline(-1, color=INK_2, linewidth=0.8, linestyle=":")
    ax.text(-1, len(order) - 0.45, "−1 pp ", fontsize=7, color=INK_2, ha="right")
    ax.set_xscale("symlog", linthresh=2)
    ax.set_xticks([-20, -10, -5, -2, -1, 0], ["−20", "−10", "−5", "−2", "−1", "0"])
    ax.set_yticks(range(len(order)), order, fontsize=8)
    ax.set_xlabel("accuracy minus hindsight-best fixed width (pp, mean of 3 seeds; symlog)", fontsize=9, color=INK_2)
    _style(ax)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.grid(axis="y", visible=False)
    ax.legend(fontsize=8, frameon=False, ncol=4, loc="lower left", bbox_to_anchor=(0, 1.0))
    fig.suptitle("How far each strategy is from the best fixed width chosen with hindsight",
                 fontsize=10, color=INK, x=0.02, ha="left")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(os.path.join(OUT, "vs_oracle.png"), dpi=130)
    plt.close(fig)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--eval", action="store_true", help="only evaluate existing runs")
    p.add_argument("--timeout", type=float, default=600.0)
    args = p.parse_args()
    if not args.eval:
        run(args.timeout)
    evaluate(load())


if __name__ == "__main__":
    main()
