import pytest
import requests

from agentic_eval.core_evals.llm_services import fi_api_service as service


@pytest.mark.parametrize(
    "method,args",
    [
        ("fetch_inferences", (None, 1)),
        ("log_eval_results", ([],)),
        ("create_eval_request", ({},)),
    ],
)
def test_transport_errors_keep_their_public_contract(monkeypatch, method, args):
    def unavailable(self, request, **kwargs):
        raise requests.ConnectionError("test service unavailable")

    monkeypatch.setattr(requests.Session, "send", unavailable)
    monkeypatch.setattr(service.FiApiKey, "_fi_api_key", "test-key")
    call = getattr(service.FiApiService, method)
    if method == "fetch_inferences":
        assert call(*args) == []
    else:
        with pytest.raises(requests.ConnectionError, match="test service unavailable"):
            call(*args)
