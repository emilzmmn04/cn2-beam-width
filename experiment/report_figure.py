"""Summary figure for REPORT.md: per dataset, accuracy gain of w=20 over w=1,
one dot per seed (paired by fold, averaged over the 10 folds) and the mean
over seeds. Run after run_experiment.py for tags phase2, seed1, seed2.

    python report_figure.py        # -> results/report_gain_w20.png
"""

from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from run_experiment import COLORS, INK, INK_2, GRID, _style  # noqa: E402

TAGS = {"phase2": 0, "seed1": 1, "seed2": 2}
SEED_MARKERS = {0: "o", 1: "s", 2: "^"}


def main():
    rows = []
    for tag, seed in TAGS.items():
        r = pd.read_csv(os.path.join(HERE, "results", tag, "results.csv"))
        p = r.pivot_table(index="dataset", columns="learner", values="accuracy")
        gain = 100 * (p["CN2 (w=20)"] - p["CN2 (w=1)"])
        rows += [{"dataset": d, "seed": seed, "gain": g} for d, g in gain.items()]
    df = pd.DataFrame(rows)
    order = df.groupby("dataset").gain.mean().sort_values().index.tolist()
    y = {d: i for i, d in enumerate(order)}

    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    for seed, g in df.groupby("seed"):
        ax.scatter(g.gain, [y[d] for d in g.dataset], marker=SEED_MARKERS[seed], s=26,
                   color=INK_2, alpha=0.55, label=f"seed {seed}", zorder=2)
    mean = df.groupby("dataset").gain.mean()
    ax.scatter(mean[order], range(len(order)), marker="D", s=60, color=COLORS[20],
               edgecolor="white", linewidth=1, label="mean of 3 seeds", zorder=3)
    from matplotlib.transforms import blended_transform_factory
    tr = blended_transform_factory(ax.transAxes, ax.transData)
    ax.text(1.02, len(order) - 0.4, "mean", transform=tr, fontsize=7, color=INK_2, va="bottom")
    for d in order:
        ax.text(1.02, y[d], f"{mean[d]:+.1f}", transform=tr, fontsize=8, color=INK, va="center")
    ax.axvline(0, color=INK_2, linewidth=1)
    ax.axvline(1, color=INK_2, linewidth=0.8, linestyle=":")
    ax.text(1, len(order) - 0.4, " 1 pp bar", fontsize=7, color=INK_2, va="bottom")
    ax.set_yticks(range(len(order)), order, fontsize=8)
    ax.set_xlabel("accuracy of w=20 minus w=1 (percentage points)", fontsize=9, color=INK_2)
    _style(ax)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.grid(axis="y", visible=False)
    ax.legend(fontsize=8, frameon=False, loc="lower right")
    fig.suptitle("CN2: gain from beam width 20 over greedy search, per dataset\n"
                 f"median dataset {mean.median():+.1f} pp; one dataset (monks-2) dominates the mean",
                 fontsize=10, color=INK, x=0.02, ha="left")
    fig.tight_layout(rect=(0, 0, 0.95, 0.94))
    out = os.path.join(HERE, "results", "report_gain_w20.png")
    fig.savefig(out, dpi=130)
    print(out, "\nmedian of seed means:", round(mean.median(), 2))


if __name__ == "__main__":
    main()
