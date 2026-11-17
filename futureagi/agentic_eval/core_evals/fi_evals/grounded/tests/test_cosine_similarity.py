import math

import pytest

from agentic_eval.core_evals.fi_evals.grounded.similarity import CosineSimilarity


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        ("", "", 0.0),
        ("one", "", 0.0),
        ("one", "two", 0.0),
        ("Cat cat DOG", "cat dog dog", 0.8),
        ("red red blue", "red", 2 / math.sqrt(5)),
        ("CAFÉ, café!", "café", 1.0),
    ],
)
def test_cosine_similarity_preserves_token_frequencies(left, right, expected):
    comparator = CosineSimilarity()
    assert comparator.compare(left, right) == pytest.approx(expected)
    assert comparator.compare(right, left) == pytest.approx(expected)


def test_cosine_similarity_large_vocabulary():
    left = " ".join(f"word{i}" for i in range(2000))
    right = " ".join(f"word{i}" for i in range(1000, 3000))
    assert CosineSimilarity().compare(left, right) == pytest.approx(0.5)
