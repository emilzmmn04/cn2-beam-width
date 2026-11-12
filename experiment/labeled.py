"""CN2 with a label, so each beam width gets its own name in the results.

`run_cv` names result rows by `learner.display_name`, which for a native
learner is just its class name -- every beam width would show up as "CN2"
and the runner's per-(dataset, learner) timeout bookkeeping would lump
them together. This is the same pattern as `demos/dense_vs_modular.py`'s
`_labeled`. It lives in its own module so the worker processes `run_cv`
starts can unpickle it by reference.

Only the name changes: `CN2(beam_width=w)` is built exactly as the library
builds it (Laplace heuristic, likelihood-ratio significance test at 3.841
as filtering, one-vs-rest `ConceptSet` with `MicroVoteCombiner`).
"""

from __future__ import annotations

from pyrulearn.learners.seco import CN2


class LabeledCN2(CN2):
    def __init__(self, beam_width: int, **kwargs):
        super().__init__(beam_width=beam_width, **kwargs)
        # public attribute -> part of the runner's cache key, next to the
        # nested BeamSearch(beam_width=...) that already distinguishes them
        self.label = f"CN2 (w={beam_width})"

    @property
    def display_name(self) -> str:
        return self.label


class LabeledCN2Optimal(CN2):
    """CN2 with exact search instead of a beam: `BranchAndBoundSearch()`
    finds, in every covering step, the rule with the highest Laplace score
    among *all* conjunctions that pass the same significance test (OPUS,
    Webb 1995) -- "beam width infinity". Everything else is CN2's default.
    Exponential in the worst case: only affordable on some datasets."""

    def __init__(self, **kwargs):
        from pyrulearn.learners.seco import BranchAndBoundSearch

        super().__init__(search=BranchAndBoundSearch(), **kwargs)
        self.label = "CN2 (optimal)"

    @property
    def display_name(self) -> str:
        return self.label
