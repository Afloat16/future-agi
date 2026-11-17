"""Missing characters must not match literal NUL characters."""

import builtins
from pathlib import Path

import pytest
import yaml

cases = pytest.mark.parametrize("left,right,score", [
    ("a", "a\0", 0.5), ("a\0", "a", 0.5), ("", "\0", 0.0),
    ("\0", "", 0.0), ("a\0", "a\0", 1.0), ("abc", "ab", 2 / 3),
    ("A", "a", 1.0), ("", "", 1.0),
])


@cases
def test_yaml_hamming_length(left, right, score):
    path = Path(__file__).parents[1] / "function/hamming_similarity.yaml"
    namespace = {}
    builtins.exec(yaml.safe_load(path.read_text())["config"]["code"], namespace)
    assert namespace["evaluate"](None, left, right, None)["score"] == pytest.approx(score)


@cases
def test_library_hamming_length(left, right, score):
    from agentic_eval.core_evals.fi_evals.function.functions import calculate_hamming_similarity

    assert calculate_hamming_similarity(left, right)["result"] == pytest.approx(score)
