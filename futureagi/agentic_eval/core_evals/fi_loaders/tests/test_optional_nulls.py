import pytest

from agentic_eval.core_evals.fi_loaders import Loader, ResponseLoader


@pytest.mark.parametrize("factory", [Loader, ResponseLoader])
@pytest.mark.parametrize("key", ["query", "context", "expected_response"])
def test_null_optional_matches_missing(factory, key):
    expected = factory().load_dict([{"response": "answer"}])
    assert factory().load_dict([{"response": "answer", key: None}]) == expected
    with pytest.raises(TypeError):
        factory().load_dict([{"response": "answer", key: 123}])


@pytest.mark.parametrize("factory", [Loader, ResponseLoader])
def test_loader_output_can_be_loaded_again(factory):
    rows = factory().load_dict([{"response": "answer"}])
    assert factory().load_dict(rows) == rows


@pytest.mark.parametrize("factory", [Loader, ResponseLoader])
def test_custom_optional_columns_allow_null(factory):
    loader = factory(col_query="q", col_context="ctx", col_expected_response="gold")
    result = loader.load_dict([{"response": "answer", "q": None, "ctx": None, "gold": None}])
    assert result == factory().load_dict([{"response": "answer"}])
