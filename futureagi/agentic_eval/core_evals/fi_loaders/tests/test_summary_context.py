import pytest

from agentic_eval.core_evals.fi_loaders.summary_loader import SummaryLoader
from agentic_eval.core_evals.fi_utils.fi_interfaces import FiInference
from agentic_eval.core_evals.llm_services.fi_api_service import FiApiService


@pytest.mark.parametrize(
    "context,key,document",
    [
        ({"source": "article", "other": "metadata"}, "source", "article"),
        ({"source": ""}, "source", ""),
        ({"": "article"}, "", "article"),
        ({"source": "article"}, None, {"source": "article"}),
        (None, "source", None),
    ],
)
def test_summary_loader_uses_selected_context_field(
    monkeypatch, context, key, document
):
    record = FiInference(
        id="1",
        prompt_slug=None,
        language_model_id=None,
        user_query=None,
        context=context,
        prompt_response="summary",
        expected_response=None,
    )
    monkeypatch.setattr(FiApiService, "fetch_inferences", lambda **kwargs: [record])
    result = SummaryLoader().load_fi_inferences(context_key=key)
    assert result == [{"document": document, "response": "summary"}]
    assert record.context == context
