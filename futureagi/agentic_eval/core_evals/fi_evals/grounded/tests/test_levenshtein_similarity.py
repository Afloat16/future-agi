import pytest

from agentic_eval.core_evals.fi_evals.grounded.similarity import (
    NormalisedLevenshteinSimilarity,
)


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        ("kitten", "sitting", 4 / 7),
        ("flaw", "lawn", 0.5),
        ("identical", "identical", 1.0),
        ("", "abc", 0.0),
        ("café", "cafe", 0.75),
        ("a" * 1000, "a", 0.001),
    ],
)
def test_levenshtein_similarity_rolling_rows(left, right, expected):
    comparator = NormalisedLevenshteinSimilarity()
    assert comparator.compare(left, right) == pytest.approx(expected)
    assert comparator.compare(right, left) == pytest.approx(expected)
