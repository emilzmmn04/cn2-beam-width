"""
CN2 beam-width experiment
=========================

How does CN2's beam width affect held-out accuracy, model size and fit time?

Everything except `beam_width` is CN2's library default (Laplace heuristic,
likelihood-ratio significance test at 3.841 as filtering, unordered
one-vs-rest rule sets combined by `MicroVoteCombiner`, random_state=0). The
cross-validation is pyrulearn's own `run_cv`: stratified, shuffled k-fold
with a fixed seed, numeric attributes discretized on each training fold only.
Within a dataset, every beam width is fitted on exactly the same folds.

Usage (from this folder, with the venv one level up active):

    python run_experiment.py                      # phase 1: vote, 10 folds
    python run_experiment.py --datasets vote,breast-cancer,iris --tag phase2
    python run_experiment.py --inspect vote --fold 0   # print the rule sets

Outputs go to results/<tag>/: results.csv (one row per dataset x fold x
width), summary.csv + summary.md (mean, sd, failures), and plots/*.png.
Fits are cached in _cache/, so a rerun or an added dataset only fits what
is new; delete _cache/ to recompute everything (e.g. for fresh timings).
"""

from __future__ import annotations

import argparse
import os
import platform
import sys
from datetime import datetime

import numpy as np
import pandas as pd

import pyrulearn
from pyrulearn.experiments.catalog import Catalog
from pyrulearn.experiments.runner import run_cv, timed_out
from pyrulearn.experiments.stats import friedman_test, mean_rank, win_counts

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # so `labeled` is importable here and in run_cv's workers
from labeled import LabeledCN2  # noqa: E402

WIDTHS = (1, 5, 10, 20)
METRICS = ("accuracy", "fit_time", "n_rules", "n_conditions")
METRIC_LABELS = {
    "accuracy": "held-out accuracy",
    "fit_time": "fit time (s)",
    "n_rules": "rules",
    "n_conditions": "conditions (total)",
}
# categorical slots 1-4 of the dataviz reference palette, validated for CVD
# separation; markers differ per width too, so colour is never the only cue
COLORS = {1: "#2a78d6", 5: "#eb6834", 10: "#1baf7a", 20: "#eda100"}
MARKERS = {1: "o", 5: "s", 10: "^", 20: "D"}
INK, INK_2, GRID = "#0b0b0b", "#52514e", "#e6e5e1"


def build_learners(widths):
    return [LabeledCN2(beam_width=w) for w in widths]


def width_of(label: str) -> int:
    return int(label.split("w=")[1].rstrip(")"))


# ---------------------------------------------------------------- summarise

def summarise(results: pd.DataFrame) -> pd.DataFrame:
    """mean and sd across folds per (dataset, width), plus failure count.
    sd is across the k folds -- it shows how much the estimate moves with
    the split, not a standard error, and folds share training data."""
    df = results.copy()
    df["beam_width"] = df["learner"].map(width_of)
    df["failed"] = df["error"].notna()
    g = df.groupby(["dataset", "beam_width"])
    out = g[list(METRICS)].agg(["mean", "std"])
    out.columns = [f"{m}_{s}" for m, s in out.columns]
    out["n_folds_ok"] = g["failed"].apply(lambda s: int((~s).sum()))
    out["n_folds_failed"] = g["failed"].sum().astype(int)
    return out.reset_index()


def _pm(mean, sd, fmt):
    if mean != mean:
        return "n/a"
    return f"{fmt.format(mean)} ± {fmt.format(sd)}" if sd == sd else fmt.format(mean)


def summary_markdown(summary: pd.DataFrame, results: pd.DataFrame, args, datasets) -> str:
    lines = [
        "# CN2 beam width: results",
        "",
        f"Generated {datetime.now():%Y-%m-%d %H:%M} · pyrulearn {getattr(pyrulearn, '__version__', '?')} · "
        f"Python {platform.python_version()} · {platform.machine()}",
        "",
        "## Setup",
        "",
        f"- Learner: `CN2(beam_width=w)` for w in {list(args.widths)}, all other settings library defaults.",
        f"- Datasets: {', '.join(d.name for d in datasets)}.",
        f"- {args.folds}-fold stratified CV, shuffled with random_state={args.seed}; identical folds for every width.",
        f"- Fit timeout {args.timeout:g}s per fit; {args.n_jobs} fit(s) at a time.",
        "- Values are mean ± sd across folds (sd = spread over folds, not a standard error).",
        "",
        "## Per dataset",
        "",
        "| dataset | w | accuracy | rules | conditions | fit time (s) | failed folds |",
        "|---|--:|--:|--:|--:|--:|--:|",
    ]
    for _, r in summary.iterrows():
        lines.append(
            f"| {r.dataset} | {r.beam_width} | "
            f"{_pm(100 * r.accuracy_mean, 100 * r.accuracy_std, '{:.1f}')}% | "
            f"{_pm(r.n_rules_mean, r.n_rules_std, '{:.1f}')} | "
            f"{_pm(r.n_conditions_mean, r.n_conditions_std, '{:.1f}')} | "
            f"{_pm(r.fit_time_mean, r.fit_time_std, '{:.2f}')} | {r.n_folds_failed} |")

    failures = results[results["error"].notna()]
    lines += ["", "## Failures", ""]
    if failures.empty:
        lines.append("None: every fit finished within the timeout without an error.")
    else:
        for (ds, lr), grp in failures.groupby(["dataset", "learner"]):
            lines.append(f"- {ds} / {lr}: {len(grp)} fold(s), error `{grp['error'].iloc[0]}`")
        for ds, lr in sorted(timed_out(results)):
            lines.append(f"- whole CV counted as timed out: {ds} / {lr}")

    n_ds = results["dataset"].nunique()
    if n_ds >= 2:
        lines += ["", "## Across datasets", "",
                  "Mean rank per width (1 = best; ties averaged; computed on per-dataset means):", "",
                  "| width | accuracy rank | fewest conditions rank | fastest rank | accuracy wins |",
                  "|--:|--:|--:|--:|--:|"]
        acc_r = mean_rank(results, "accuracy")
        cond_r = mean_rank(results, "n_conditions", higher_is_better=False)
        time_r = mean_rank(results, "fit_time", higher_is_better=False)
        wins = win_counts(results, "accuracy")
        for lr in sorted(acc_r.index, key=width_of):
            lines.append(f"| {width_of(lr)} | {acc_r[lr]:.2f} | {cond_r[lr]:.2f} | {time_r[lr]:.2f} | {wins[lr]:.1f} |")
        lines.append("")
        for m in ("accuracy", "n_conditions"):
            try:
                f = friedman_test(results, m)
                lines.append(f"- Friedman test on {m}: chi² = {f.statistic:.2f}, p = {f.pvalue:.3f} "
                             f"({f.n_datasets} datasets, {f.n_learners} widths).")
            except ValueError as e:
                lines.append(f"- Friedman test on {m}: not computed ({e}).")
        lines.append("- With few datasets the Friedman test has little power: p > 0.05 means *no evidence* "
                     "of a difference, not evidence of none.")
    else:
        lines += ["", "Only one dataset: no across-dataset statistics (ranks/Friedman need several)."]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- plots

def _style(ax):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(INK_2)
    ax.tick_params(colors=INK_2, labelsize=8)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def _log_ticks(ax, which: str, suffix: str = ""):
    """Readable ticks on a log axis: 1-2-5 steps inside the current range,
    plain numbers ("0.05", "2×") instead of matplotlib's 5×10⁻² style."""
    from matplotlib.ticker import NullFormatter, NullLocator

    lo, hi = ax.get_xlim() if which == "x" else ax.get_ylim()
    cands = [m * 10.0 ** e for e in range(-4, 5) for m in (1, 2, 5)]
    if hi / lo < 4:  # narrow range: denser steps
        cands = [m * 10.0 ** e for e in range(-4, 5) for m in (1, 1.1, 1.25, 1.5, 2, 3, 5, 8, 9)]
    ticks = [t for t in cands if lo <= t <= hi]
    axis = ax.xaxis if which == "x" else ax.yaxis
    axis.set_minor_locator(NullLocator())
    axis.set_minor_formatter(NullFormatter())
    (ax.set_xticks if which == "x" else ax.set_yticks)(ticks, [f"{t:g}{suffix}" for t in ticks])
    (ax.set_xlim if which == "x" else ax.set_ylim)(lo, hi)


def plot_metric_grid(summary: pd.DataFrame, metric: str, path: str):
    """Small multiples: one panel per dataset, x = beam width, mean ± sd.
    Each panel has its own y-scale: the question is the trend within a
    dataset, and datasets differ a lot in level."""
    import matplotlib.pyplot as plt

    datasets = list(dict.fromkeys(summary["dataset"]))
    n = len(datasets)
    cols = min(n, 4)
    rows = int(np.ceil(n / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(max(3.2 * cols + 0.6, 4.4), 2.6 * rows + 0.6), squeeze=False)
    scale = 100 if metric == "accuracy" else 1
    for ax, ds in zip(axes.flat, datasets):
        s = summary[summary["dataset"] == ds].sort_values("beam_width")
        xs = np.arange(len(s))
        ax.plot(xs, scale * s[f"{metric}_mean"], color=INK_2, linewidth=1, zorder=1)
        for x, (_, r) in zip(xs, s.iterrows()):
            w = r.beam_width
            ax.errorbar(x, scale * r[f"{metric}_mean"], yerr=scale * r[f"{metric}_std"],
                        fmt=MARKERS[w], color=COLORS[w], markersize=7, linewidth=2, capsize=3,
                        markeredgecolor="white", markeredgewidth=1, zorder=2)
        ax.set_xticks(xs, [str(w) for w in s["beam_width"]])
        ax.set_title(ds, fontsize=9, color=INK, loc="left")
        if metric == "fit_time":
            ax.set_yscale("log")
            _log_ticks(ax, "y")
        _style(ax)
    for ax in list(axes.flat)[n:]:
        ax.set_visible(False)
    unit = " (%)" if metric == "accuracy" else ""
    for ax in axes[:, 0]:
        ax.set_ylabel(METRIC_LABELS[metric] + unit, fontsize=9, color=INK_2)
    for ax in axes[-1, :]:
        ax.set_xlabel("beam width", fontsize=9, color=INK_2)
    fig.suptitle(f"CN2: {METRIC_LABELS[metric]} by beam width\n"
                 "mean ± sd over folds; x not to scale",
                 fontsize=10, color=INK, x=0.02, ha="left")
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(path, dpi=130)
    plt.close(fig)


def plot_change_vs_greedy(results: pd.DataFrame, path: str):
    """Paired view: per dataset and fold, each width minus w=1 on the same
    fold, averaged over folds. Accuracy in percentage points; size and time
    as ratios on a log axis. One row per dataset, colour+marker = width."""
    import matplotlib.pyplot as plt

    df = results.copy()
    df["beam_width"] = df["learner"].map(width_of)
    base = df[df["beam_width"] == 1].set_index(["dataset", "fold"])
    others = sorted(w for w in df["beam_width"].unique() if w != 1)
    if not others or base.empty:
        return
    datasets = list(dict.fromkeys(df["dataset"]))
    panels = [("accuracy", "Δ accuracy vs w=1 (pp)", "diff"),
              ("n_conditions", "conditions ÷ w=1", "ratio"),
              ("fit_time", "fit time ÷ w=1", "ratio")]
    fig, axes = plt.subplots(1, 3, figsize=(11, 0.45 * len(datasets) + 1.8), sharey=True)
    offsets = np.linspace(-0.22, 0.22, len(others))
    for ax, (metric, label, kind) in zip(axes, panels):
        for off, w in zip(offsets, others):
            cur = df[df["beam_width"] == w].set_index(["dataset", "fold"])
            joined = cur[[metric]].join(base[[metric]].add_suffix("_base")).dropna()
            if kind == "diff":
                per_fold = 100 * (joined[metric] - joined[f"{metric}_base"])
                agg = per_fold.groupby(level=0).agg(["mean", "std"])
            else:
                per_fold = np.log(joined[metric] / joined[f"{metric}_base"])
                agg = per_fold.groupby(level=0).agg(["mean", "std"])
            for i, ds in enumerate(datasets):
                if ds not in agg.index:
                    continue
                m, s = agg.loc[ds, "mean"], agg.loc[ds, "std"]
                if kind == "ratio":  # geometric mean ratio, ± 1 sd in log space
                    x, lo, hi = np.exp(m), np.exp(m) - np.exp(m - s), np.exp(m + s) - np.exp(m)
                    xerr = [[lo], [hi]]
                else:
                    x, xerr = m, s
                ax.errorbar(x, i + off, xerr=xerr, fmt=MARKERS[w], color=COLORS[w], markersize=6,
                            linewidth=1.5, capsize=2, markeredgecolor="white", markeredgewidth=0.8,
                            label=f"w={w}" if (i == 0 and metric == "accuracy") else None)
        ax.axvline(0 if kind == "diff" else 1, color=INK_2, linewidth=1)
        if kind == "ratio":
            ax.set_xscale("log")
            _log_ticks(ax, "x", suffix="×")
        ax.set_xlabel(label, fontsize=9, color=INK_2)
        _style(ax)
        ax.grid(axis="x", color=GRID, linewidth=0.8)
        ax.grid(axis="y", visible=False)
    axes[0].set_yticks(range(len(datasets)), datasets, fontsize=8)
    axes[0].invert_yaxis()
    axes[0].legend(fontsize=8, frameon=False, loc="lower left", bbox_to_anchor=(0, 1.0), ncol=len(others))
    fig.suptitle("CN2: change relative to greedy search (w=1), paired by fold; bars = ±1 sd over folds",
                 fontsize=10, color=INK, x=0.01, ha="left")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


# ---------------------------------------------------------------- inspect

def inspect(dataset: str, fold: int, folds: int, seed: int, widths):
    """Fit every width on one training fold, exactly as run_cv builds it,
    and print the rule sets -- to see *how* the models differ."""
    from pyrulearn.data.io import build_dataspec, encode
    from pyrulearn.experiments.runner import _stratified_folds  # same splitter run_cv uses

    entry = Catalog.default().select(names=[dataset])[0]
    df, target = entry.load()
    train_idx, test_idx = _stratified_folds(df[target].to_numpy(), folds, seed)[fold]
    train_df = df.iloc[train_idx].reset_index(drop=True)
    test_df = df.iloc[test_idx].reset_index(drop=True)
    spec = build_dataspec(train_df, target=target, skip_unusable=True).build()
    train = encode(spec, train_df, train_df[target].to_numpy())
    test = encode(spec, test_df, test_df[target].to_numpy())
    print(f"{dataset}, fold {fold} of {folds}: {len(train_idx)} train / {len(test_idx)} test rows\n")
    for w in widths:
        model = LabeledCN2(beam_width=w).fit(train)
        st = model.evaluate(test)
        print(f"=== beam width {w}: {st.n_rules} rules, {st.n_conditions} conditions, "
              f"test accuracy {st.confusion.accuracy:.3f}")
        print(model)
        print()


# ---------------------------------------------------------------- main

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--datasets", default="vote", help="comma-separated catalog names (default: vote)")
    p.add_argument("--widths", default=",".join(map(str, WIDTHS)))
    p.add_argument("--folds", type=int, default=10)
    p.add_argument("--seed", type=int, default=0, help="random_state of the fold split")
    p.add_argument("--timeout", type=float, default=600.0, help="seconds per fit before it counts as failed")
    p.add_argument("--n-jobs", type=int, default=1, help="parallel fits (>1 makes fit times noisier)")
    p.add_argument("--tag", default="phase1", help="results/<tag>/ output folder")
    p.add_argument("--inspect", metavar="DATASET", help="print the rule sets of one fold instead")
    p.add_argument("--fold", type=int, default=0)
    args = p.parse_args()
    args.widths = tuple(int(w) for w in args.widths.split(","))

    if args.inspect:
        inspect(args.inspect, args.fold, args.folds, args.seed, args.widths)
        return

    names = [n.strip() for n in args.datasets.split(",") if n.strip()]
    datasets = Catalog.default().select(names=names)
    out = os.path.join(HERE, "results", args.tag)
    os.makedirs(os.path.join(out, "plots"), exist_ok=True)

    results = run_cv(build_learners(args.widths), datasets, n_folds=args.folds,
                     fit_timeout=args.timeout, random_state=args.seed,
                     cache_dir=os.path.join(HERE, "_cache"), n_jobs=args.n_jobs)
    results.to_csv(os.path.join(out, "results.csv"), index=False)

    summary = summarise(results)
    summary.to_csv(os.path.join(out, "summary.csv"), index=False)
    with open(os.path.join(out, "summary.md"), "w", encoding="utf-8") as f:
        f.write(summary_markdown(summary, results, args, datasets))

    for m in METRICS:
        plot_metric_grid(summary, m, os.path.join(out, "plots", f"{m}.png"))
    plot_change_vs_greedy(results, os.path.join(out, "plots", "change_vs_greedy.png"))
    print(f"\nwrote {out}/")


if __name__ == "__main__":
    main()
