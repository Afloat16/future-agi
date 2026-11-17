import pytest

from agentic_eval.core_evals.fi_utils.token_count_helper import (
    get_completion_tokens_openai_chat_completion,
    get_prompt_tokens_openai_chat_completion,
    get_token_usage_openai_completion,
)

TEXT_COUNTS = [("<|endoftext|>", 7), ("a <|fim_prefix|> b", 8), ("hello world", 2)]


@pytest.mark.parametrize("text,count", TEXT_COUNTS)
@pytest.mark.parametrize(
    "counter",
    [
        get_completion_tokens_openai_chat_completion,
        get_token_usage_openai_completion,
    ],
)
def test_completion_counts_literal_special_token_text(counter, text, count):
    assert counter(text, "gpt-4") == count


@pytest.mark.parametrize("text,count", TEXT_COUNTS)
def test_prompt_counts_literal_special_token_text(text, count):
    messages = [{"role": "user", "content": text}]
    assert get_prompt_tokens_openai_chat_completion(messages, "gpt-4") == count + 7
