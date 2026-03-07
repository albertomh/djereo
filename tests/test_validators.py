# Test the custom validators defined for certain questions in `copier.yaml`.

import re
from collections.abc import Callable

import pytest


@pytest.mark.unit
@pytest.mark.parametrize(
    ("question", "answer", "error_msg"),
    [
        ("author_name", "Francisco de Quevedo", None),
        ("author_name", "", "author_name cannot be empty"),
        ("initial_version", "0.0.0", None),
        ("initial_version", "", "Must have value"),
    ],
)
def test_validator_is_empty(
    question: str,
    answer: str,
    error_msg: str | None,
    copier_copy: Callable,
    copier_input_data: dict,
):
    """Align with the new way: using copier_copy fixture and session-scoped input data."""
    payload = {**copier_input_data, question: answer}

    if error_msg is None:
        copier_copy(payload)
    else:
        # Copier raises ValueError when a validator returns a non-empty string
        with pytest.raises(ValueError, match=rf".*{re.escape(error_msg)}$"):
            copier_copy(payload)


@pytest.mark.unit
@pytest.mark.parametrize(
    ("project_name", "should_raise"),
    [
        ("ok_project", False),
        ("MyProjectName", True),
        ("dash-it", True),
        ("2whynumber", True),
    ],
)
def test_validator_project_name(
    project_name: str,
    should_raise: bool,
    copier_copy: Callable,
    copier_input_data: dict,
):
    payload = {**copier_input_data, "project_name": project_name}

    expected_error_msg = (
        "project_name must start with a letter, be lowercase and may contain underscores"
    )

    if should_raise:
        with pytest.raises(ValueError, match=re.escape(expected_error_msg)):
            copier_copy(payload)
    else:
        copier_copy(payload)


@pytest.mark.unit
@pytest.mark.parametrize(
    ("author_email", "should_raise"),
    [
        ("user@example.com", False),
        ("broken@email", True),
        ("justastring", True),
        ("nope@@tld", True),
    ],
)
def test_validator_author_email(
    author_email: str,
    should_raise: bool,
    copier_copy: Callable,
    copier_input_data: dict,
):
    payload = {**copier_input_data, "author_email": author_email}

    expected_error_msg = "author_email must be an email address"

    if should_raise:
        with pytest.raises(ValueError, match=re.escape(expected_error_msg)):
            copier_copy(payload)
    else:
        copier_copy(payload)
