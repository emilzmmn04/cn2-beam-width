"""CN2 whose beam width is chosen by inner cross-validation on the training
data it is given (nested CV when run inside run_cv's outer folds).

`fit(train)`: split `train` into `inner_folds` stratified folds
(`inner_seed`); for each width in `widths`, fit `CN2(beam_width=w)` on each
inner training part and measure accuracy on the inner held-out part; pick
the width with the best mean inner accuracy (ties -> the smallest width);
refit `CN2(beam_width=best)` on all of `train`. The outer test fold is never
seen. The chosen width and the inner accuracies are attached to the model as
`tuned_width` / `tuned_inner_accuracy` for reporting.

Note: `train` arrives already discretized by run_cv on the whole outer
training fold, so inner validation rows took part in choosing the
discretization thresholds. That uses training data only (no test leakage),
but it makes the inner estimate slightly optimistic for every width alike.
"""

from __future__ import annotations

import numpy as np

from pyrulearn.learners.seco import CN2


def _inner_folds(y, k, seed):
    from sklearn.model_selection import KFold, StratifiedKFold

    idx = np.zeros(len(y))
    try:
        return list(StratifiedKFold(n_splits=k, shuffle=True, random_state=seed).split(idx, y))
    except ValueError:
        return list(KFold(n_splits=k, shuffle=True, random_state=seed).split(idx))


class TunedCN2(CN2):
    def __init__(self, widths=(1, 5, 10, 20), inner_folds: int = 5, inner_seed: int = 0):
        super().__init__()
        self.widths = tuple(widths)
        self.inner_folds = inner_folds
        self.inner_seed = inner_seed
        self.label = "CN2 (tuned)"

    @property
    def display_name(self) -> str:
        return self.label

    def fit(self, data, model=None, **model_kwargs):
        y = np.asarray(data.y)
        n = len(y)
        acc = {w: [] for w in self.widths}
        for tr, va in _inner_folds(y, self.inner_folds, self.inner_seed):
            mtr = np.zeros(n, bool)
            mtr[tr] = True
            mva = np.zeros(n, bool)
            mva[va] = True
            dtr, dva = data.select_rows(mtr), data.select_rows(mva)
            for w in self.widths:
                stats = CN2(beam_width=w).fit(dtr).evaluate(dva)
                acc[w].append(stats.confusion.accuracy)
        means = {w: float(np.mean(a)) for w, a in acc.items()}
        best = max(means.values())
        chosen = min(w for w, m in means.items() if m >= best - 1e-12)
        fitted = CN2(beam_width=chosen).fit(data, model, **model_kwargs)
        fitted.tuned_width = chosen
        fitted.tuned_inner_accuracy = means
        return fitted


def measure(model, test_rep) -> dict:
    """run_cv measure_fn: record which width was chosen."""
    return {"tuned_width": getattr(model, "tuned_width", np.nan)}
