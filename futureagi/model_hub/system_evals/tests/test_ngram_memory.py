import tracemalloc
from pathlib import Path

import pytest
import yaml


@pytest.mark.parametrize("name", ["distinct_n", "repetition_rate"])
@pytest.mark.parametrize("n", [1, 3])
def test_ngram_memory_and_scores(name, n):
    path = Path(__file__).parents[1] / "function" / f"{name}.yaml"
    namespace = {}
    exec(yaml.safe_load(path.read_text())["config"]["code"], namespace)
    evaluate = namespace["evaluate"]
    text = "a " * 20000
    tracemalloc.start()
    result = evaluate(None, text, None, None, n=n)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert result["score"] == pytest.approx(1 / (20000 - n + 1))
    assert peak < 900000, peak
    assert evaluate(None, "a b a b", None, None, n=2)["score"] == pytest.approx(2 / 3)
    assert evaluate(None, "a b c", None, None, n=2)["score"] == 1.0
