import json

import pytest

from agentic_eval.core_evals.fi_loaders import JsonLoader, Loader, ResponseLoader, SummaryLoader, TextLoader
from agentic_eval.core_evals.fi_utils.fi_interfaces import FiInference
from agentic_eval.core_evals.llm_services.fi_api_service import FiApiService


@pytest.mark.parametrize("factory", [JsonLoader, Loader, ResponseLoader, SummaryLoader, TextLoader])
@pytest.mark.parametrize("format", ["dict", "json"])
def test_reload_replaces_dataset(factory, format, tmp_path):
    loader = factory()
    row = {"response": "first", "text": "first", "document": "first", "actual_json": "{}"}
    first = loader.load_dict([row])
    saved = list(first)
    replacement = {**row, "response": "second", "text": "second", "actual_json": "[]"}
    path = tmp_path / "rows.json"
    path.write_text(json.dumps([replacement]))
    second = loader.load_json(str(path)) if format == "json" else loader.load_dict([replacement])
    assert second == factory().load_dict([replacement])
    assert first == saved and first is not second
    loader.process()
    assert loader.processed_dataset == second
    assert loader.load_dict([]) == []


@pytest.mark.parametrize("factory", [Loader, ResponseLoader, SummaryLoader, TextLoader])
def test_inference_reload_replaces_dataset(factory, monkeypatch):
    rows = [FiInference("id", None, None, "query", None, "first", None)]
    monkeypatch.setattr(FiApiService, "fetch_inferences", lambda **kwargs: rows)
    loader = factory()
    first = loader.load_fi_inferences()
    rows[0] = FiInference("next", None, None, "query", None, "second", None)
    second = loader.load_fi_inferences()
    assert second == factory().load_fi_inferences() and len(first) == 1
    assert first is not second
    rows.clear()
    assert loader.load_fi_inferences() == []
