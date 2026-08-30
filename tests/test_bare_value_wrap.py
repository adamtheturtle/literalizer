"""A whole file holding a value that binds no name.

``wrap_in_file=True`` with ``variable_form=None`` is a surface no
golden-file case reaches: every case owner declares a variable form, so
the value is always bound to a name.  These check the shapes that need
the file to read the value as an expression rather than as a statement
(issue #4774).
"""

import pytest

from literalizer import InputFormat, LanguageCls, NewVariable, literalize
from literalizer.languages import JavaScript, TypeScript


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=[JavaScript, TypeScript],
    ids=lambda language_cls: language_cls.__name__,
)
def test_bare_object_is_parenthesized(language_cls: LanguageCls) -> None:
    """An object at statement scope would open a block, not a literal."""
    result = literalize(
        source='{"a": 1}',
        input_format=InputFormat.JSON,
        language=language_cls(),
        wrap_in_file=True,
        variable_form=None,
    )

    assert result.code.startswith("({")
    assert "})" in result.code


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=[JavaScript, TypeScript],
    ids=lambda language_cls: language_cls.__name__,
)
@pytest.mark.parametrize(
    argnames=("source", "opening"),
    argvalues=[("[1, 2]", "["), ("42", "42"), ('"text"', '"text"')],
)
def test_other_bare_roots_are_left_alone(
    language_cls: LanguageCls,
    source: str,
    opening: str,
) -> None:
    """Every other root already reads as an expression."""
    result = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=language_cls(),
        wrap_in_file=True,
        variable_form=None,
    )

    assert result.code.startswith(opening)


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=[JavaScript, TypeScript],
    ids=lambda language_cls: language_cls.__name__,
)
def test_bound_object_is_not_parenthesized(language_cls: LanguageCls) -> None:
    """A name to bind to makes the statement reading impossible."""
    result = literalize(
        source='{"a": 1}',
        input_format=InputFormat.JSON,
        language=language_cls(),
        wrap_in_file=True,
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
    )

    assert "({" not in result.code
