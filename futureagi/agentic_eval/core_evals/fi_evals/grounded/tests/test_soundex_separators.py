import pytest

from agentic_eval.core_evals.fi_evals.grounded.similarity import PhoneticSimilarity


@pytest.mark.parametrize(
    ("word", "code"),
    [
        ("Tymczak", "T522"),
        ("Jackson", "J250"),
        ("Ashcraft", "A261"),
        ("Pfister", "P236"),
        ("Honeyman", "H555"),
        ("Bob", "B100"),
        ("Gutierrez", "G362"),
    ],
)
def test_soundex_respects_consonant_separators(word, code):
    assert PhoneticSimilarity()._get_soundex_code(word) == code


def test_vowel_separated_consonants_do_not_create_false_matches():
    assert PhoneticSimilarity().compare("Bob", "B") == 0.0
