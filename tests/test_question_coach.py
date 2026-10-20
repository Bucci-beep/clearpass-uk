import pytest

from clearpass.services.question_coach import CoachInput, build_question


def test_preserves_original_question_and_supplied_information():
    prompt = build_question(
        CoachInput(
            "Does my policy cover stock?", "Wales", "Baking", "£500 in a cupboard", "Home contents"
        )
    )
    for text in (
        "Does my policy cover stock?",
        "Wales",
        "Baking",
        "£500 in a cupboard",
        "Home contents",
    ):
        assert text in prompt
    assert "my own policy" in prompt


def test_unsupplied_data_is_not_invented():
    prompt = build_question(CoachInput("Is business stock covered?"))
    assert "Missing or uncertain" in prompt
    assert "which UK nation" in prompt
    assert "£" not in prompt
    assert "Scotland" not in prompt


def test_empty_question_rejected():
    with pytest.raises(ValueError):
        build_question(CoachInput("   "))


def test_unrecognised_policy_is_rejected():
    with pytest.raises(ValueError):
        build_question(CoachInput("Coverage?", insurance="Comprehensive"))


def test_original_input_is_not_modified():
    question = "Is my GARAGE stock covered?"
    assert f"Original question: {question}" in build_question(CoachInput(question))
