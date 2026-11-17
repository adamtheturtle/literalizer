"""Public call transforms must close their recognized literal
constructs.
"""

import pytest

import literalizer
from literalizer.exceptions import UnterminatedCallTransformError
from literalizer.languages import Dart, Rust


@pytest.mark.parametrize(
    argnames=("language", "expression", "position", "expected"),
    argvalues=[
        (Rust(), 'make_widget(cr#"// payload', 12, '"#'),
        (Rust(), 'make_widget(r##"payload"#', 12, '"##'),
        (Rust(), 'make_widget(br"payload', 12, '"'),
        (Dart(), '"${"// payload"}', 0, '"'),
        (Dart(), '"${"// payload"', 1, "}"),
        (Dart(), '"${]"// payload"', 1, "}"),
        (Dart(), '"${"payload', 3, '"'),
        (Dart(), 'r"payload', 1, '"'),
        (Dart(), '"""payload', 0, '"""'),
        (Dart(), '"payload\\', 0, '"'),
        (Rust(), "make_widget(42) /* outer /* inner */", 16, "*/"),
        (Dart(), "make_widget(42) /* outer /* inner */", 16, "*/"),
    ],
)
@pytest.mark.parametrize(
    argnames="binding", argvalues=[None, "new", "existing"]
)
@pytest.mark.parametrize(argnames="per_element", argvalues=[False, True])
def test_unterminated_call_transform(
    *,
    language: literalizer.Language,
    expression: str,
    position: int,
    expected: str,
    binding: str | None,
    per_element: bool,
) -> None:
    """Reject before statement termination for every call-binding form."""
    variable_form: literalizer.VariableForm | None = None
    if binding == "new":
        variable_form = literalizer.NewVariable(
            name="my_data", modifiers=frozenset()
        )
    elif binding == "existing":
        variable_form = literalizer.ExistingVariable(name="my_data")

    with pytest.raises(
        expected_exception=UnterminatedCallTransformError
    ) as error:
        _ = literalizer.literalize_call(
            source="[[42]]" if per_element else "42",
            input_format=literalizer.InputFormat.JSON,
            language=language,
            target_function="make_widget",
            parameter_names=("value",),
            per_element=per_element,
            variable_form=variable_form,
            call_transform=lambda _context: expression,
        )
    assert error.value.position == position
    assert error.value.expected == expected
    assert "call_transform" in str(object=error.value)


@pytest.mark.parametrize(argnames="language", argvalues=[Rust(), Dart()])
@pytest.mark.parametrize(argnames="bound", argvalues=[False, True])
def test_wrapped_call_rejects_unterminated_transform(
    *, language: literalizer.Language, bound: bool
) -> None:
    """Whole-file output cannot accept a caller-repairable open string."""
    with pytest.raises(expected_exception=UnterminatedCallTransformError):
        _ = literalizer.literalize_call(
            source="42",
            input_format=literalizer.InputFormat.JSON,
            language=language,
            target_function="make_widget",
            parameter_names=("value",),
            per_element=False,
            variable_form=(
                literalizer.NewVariable(name="my_data", modifiers=frozenset())
                if bound
                else None
            ),
            call_transform=lambda _context: '"// unfinished',
            wrap_in_file=True,
        )


def test_later_call_rejects_without_reinvoking_transform() -> None:
    """Validate each real transform once, including later rows in a
    batch.
    """
    visited: list[int] = []

    def transform(context: literalizer.CallContext) -> str:
        """Leave only the second transformed expression unfinished."""
        visited.append(context.index)
        return context.call if context.index == 0 else '"unfinished'

    with pytest.raises(expected_exception=UnterminatedCallTransformError):
        _ = literalizer.literalize_call(
            source="[[1], [2], [3]]",
            input_format=literalizer.InputFormat.JSON,
            language=Dart(),
            target_function="make_widget",
            parameter_names=("value",),
            call_transform=transform,
        )
    assert visited == [0, 1]


@pytest.mark.parametrize(argnames="language", argvalues=[Rust(), Dart()])
@pytest.mark.parametrize(
    argnames="expression",
    argvalues=[
        '/* outer /* inner */ " */ make_widget(42)',
        'make_widget(42) // "unfinished comment text',
        '"// quoted comment marker"',
    ],
)
def test_complete_transform_keeps_comment_text(
    language: literalizer.Language, expression: str
) -> None:
    """Quotes in comments and comment markers in strings stay distinct."""
    result = literalizer.literalize_call(
        source="42",
        input_format=literalizer.InputFormat.JSON,
        language=language,
        target_function="make_widget",
        parameter_names=("value",),
        per_element=False,
        variable_form=literalizer.NewVariable(
            name="my_data", modifiers=frozenset()
        ),
        call_transform=lambda _context: expression,
    )
    assert expression in result.code.replace("; //", " //")
