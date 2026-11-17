import json

import pytest
import requests

from agentic_eval.core_evals.fi_utils.fi_dataset import Dataset, DatasetRow
from agentic_eval.core_evals.keys.fi_api_key import FiApiKey


@pytest.mark.parametrize("as_row", [True, False])
def test_dataset_rows_are_json_serializable(monkeypatch, as_row):
    row = {"query": "你好", "response": "", "context": []}
    rows = [DatasetRow(**row) if as_row else row]
    sent = []

    def send(session, request, **kwargs):
        sent.append(json.loads(request.body))
        response = requests.Response()
        response.status_code = 201
        response._content = (
            b'{"data":{"dataset":{"id":"1","name":"test","source":"dev_sdk",'
            b'"description":null,"language_model_id":null,"prompt_template":null}}}'
        )
        return response

    monkeypatch.setattr(FiApiKey, "_fi_api_key", "test-key")
    monkeypatch.setattr(requests.Session, "send", send)
    assert Dataset.create("test", rows=rows).id == "1"
    assert sent[0]["dataset_rows"] == [row]
    assert rows[0] == (DatasetRow(**row) if as_row else row)
