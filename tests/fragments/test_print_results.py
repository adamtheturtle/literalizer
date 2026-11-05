"""Printing retains native syntax and producer-owned dependencies."""

from collections.abc import Callable

import pytest

from literalizer import (
    CallContext,
    InputFormat,
    Language,
    NewVariable,
    literalize_call,
)
from literalizer._formatters.preamble_roles import preamble_imports
from literalizer.exceptions import UnsupportedCallShapeError
from literalizer.languages import (
    Cpp,
    CSharp,
    Go,
    Java,
    JavaScript,
    Kotlin,
    Python,
    Ruby,
    Rust,
    Scala,
    TypeScript,
    Yaml,
)


@pytest.mark.parametrize(
    argnames=("language", "expected"),
    argvalues=[
        (Python(), "print(calculate(value=1))"),
        (Java(), "System.out.println(calculate(1));"),
        (Cpp(), "std::cout << calculate(1) << '\\n';"),
        (CSharp(), "System.Console.WriteLine(calculate(1));"),
        (Go(), "fmt.Println(calculate(1))"),
        (JavaScript(), "console.log(calculate({ value: 1 }));"),
        (TypeScript(), "console.log(calculate({ value: 1 }));"),
        (Kotlin(), "println(calculate(value = 1))"),
        (Ruby(), "puts calculate(value: 1)"),
        (Scala(), "println(calculate(value = 1))"),
        (Rust(), 'println!("{:?}", calculate(1));'),
    ],
)
def test_native_printing(*, language: Language, expected: str) -> None:
    """Each backend supplies syntax without evaluating calls twice."""
    result = literalize_call(
        source="[[1]]",
        input_format=InputFormat.JSON,
        language=language,
        target_function="calculate",
        parameter_names=["value"],
        print_result=True,
    )
    assert result.code == expected
    assert result.code.count("calculate(") == 1


@pytest.mark.parametrize(argnames="language", argvalues=[Cpp(), Go()])
def test_print_imports(*, language: Language) -> None:
    """Printing dependencies survive as structured import metadata."""
    printed = literalize_call(
        source="[[1], [2]]",
        input_format=InputFormat.JSON,
        language=language,
        target_function="calculate",
        parameter_names=["value"],
        print_result=True,
    )
    bare = literalize_call(
        source="[[1], [2]]",
        input_format=InputFormat.JSON,
        language=language,
        target_function="calculate",
        parameter_names=["value"],
    )
    expected = (
        "#include <iostream>" if isinstance(language, Cpp) else 'import "fmt"'
    )
    assert printed.preamble.count(expected) == 1
    assert expected in preamble_imports(printed.preamble)
    assert expected not in bare.preamble


def test_no_calls_need_no_print_import() -> None:
    """An empty call sequence does not add an unused printing import."""
    result = literalize_call(
        source="[]",
        input_format=InputFormat.JSON,
        language=Go(),
        target_function="calculate",
        parameter_names=["value"],
        print_result=True,
    )
    assert 'import "fmt"' not in result.preamble
    assert result.code == ""


def _identity(context: CallContext) -> str:
    """Retain a caller-owned custom transform for the conflict case."""
    return context.call


@pytest.mark.parametrize(
    argnames=("transform", "binding", "zip_source"),
    argvalues=[
        (_identity, None, None),
        (None, NewVariable(name="result", modifiers=frozenset()), None),
        (None, None, "[1]"),
    ],
)
def test_incompatible_print_options(
    *,
    transform: Callable[[CallContext], str] | None,
    binding: NewVariable | None,
    zip_source: str | None,
) -> None:
    """Result handling conflicts are rejected rather than ignored."""
    with pytest.raises(
        expected_exception=UnsupportedCallShapeError,
        match="print_result cannot be combined",
    ):
        _ = literalize_call(
            source="[[1]]",
            input_format=InputFormat.JSON,
            language=Python(),
            target_function="calculate",
            parameter_names=["value"],
            print_result=True,
            call_transform=transform,
            variable_form=binding,
            zip_source=zip_source,
            zip_input_format=None if zip_source is None else InputFormat.JSON,
        )


def test_unsupported_printing() -> None:
    """Languages without the explicit capability reject printing."""
    with pytest.raises(
        expected_exception=UnsupportedCallShapeError,
        match="print_result is not supported",
    ):
        _ = literalize_call(
            source="[[1]]",
            input_format=InputFormat.JSON,
            language=Yaml(),
            target_function="calculate",
            parameter_names=["value"],
            print_result=True,
        )


def test_wrapped_print_preamble() -> None:
    """Printing dependencies are included before the wrapped program."""
    result = literalize_call(
        source="[[1]]",
        input_format=InputFormat.JSON,
        language=Cpp(language_version=Cpp.VersionFormats["CPP14"]),
        target_function="calculate",
        parameter_names=["value"],
        print_result=True,
        wrap_in_file=True,
    )
    assert result.code.count("#include <iostream>") == 1
    assert "std::cout << calculate(1) << '\\n';" in result.code


def test_custom_transform_remains_available() -> None:
    """Custom expressions retain their original dependency contract."""
    result = literalize_call(
        source="[[1]]",
        input_format=InputFormat.JSON,
        language=Cpp(),
        target_function="calculate",
        parameter_names=["value"],
        call_transform=_identity,
    )
    assert result.code == "calculate(1);"
    assert "#include <iostream>" not in result.preamble
