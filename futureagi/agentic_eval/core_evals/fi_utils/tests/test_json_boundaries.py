import json

import pytest

from agentic_eval.core_evals.fi_utils.json import JsonExtractor, JsonHelper


@pytest.mark.parametrize("value", ["}", "{", "]", "[", 'quote: \\" }', "\\\\["])
def test_extractor_ignores_delimiters_inside_strings(value):
    expected = {"nested": [{"value": value}], "after": True}
    text = "Result: " + json.dumps(expected) + ' followed by {"later": true}'
    assert JsonExtractor.extract_first_json_entity(text) == expected


@pytest.mark.parametrize("value", ["}", "{", "]", "["])
def test_helper_loads_prose_wrapped_string_arrays(value):
    expected = [value, "ordinary"]
    assert JsonHelper.extract_json_from_text("Result: " + json.dumps(expected)) == expected


def test_extractor_skips_invalid_candidates_and_handles_absent_json():
    assert JsonExtractor.extract_first_json_entity('bad {x} then [1, 2]') == [1, 2]
    assert JsonExtractor.extract_first_json_entity("No JSON here") is None
