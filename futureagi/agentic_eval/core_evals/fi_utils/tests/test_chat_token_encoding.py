import pytest
import tiktoken

from agentic_eval.core_evals.fi_utils.token_count_helper import (
    get_completion_tokens_openai_chat_completion,
    get_prompt_tokens_openai_chat_completion,
)


@pytest.mark.parametrize(
    "model",
    ["gpt-4o", "gpt-4o-2024-08-06", "gpt-4o-mini", "gpt-4", "gpt-3.5-turbo"],
)
def test_chat_token_counts_use_the_model_encoding(model):
    text = "你好，世界！こんにちは世界！"
    encoding = tiktoken.encoding_for_model(model)
    expected = len(encoding.encode(text))
    assert get_completion_tokens_openai_chat_completion(text, model) == expected
    prompt = [{"role": "user", "content": text}]
    assert get_prompt_tokens_openai_chat_completion(prompt, model) == expected + 7


def test_chat_token_counts_reject_unknown_models():
    with pytest.raises(ValueError, match="not supported"):
        get_completion_tokens_openai_chat_completion("hello", "unknown")
