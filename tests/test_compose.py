"""Tests for composing literalization results."""

from literalizer import (
    InputFormat,
    LiteralizeResult,
    NewVariable,
    compose,
    literalize,
    literalize_call,
)
from literalizer.languages import Python

PYTHON = Python()


def test_compose_merges_result_parts_in_order() -> None:
    """``compose`` preserves result order and deduplicates preambles."""
    first = LiteralizeResult(
        declaration_code="first = 1",
        preamble=("import a", "import b"),
        body_preamble=("class A: ...", "class B: ..."),
        pre_declaration_comments=("# first",),
        types_present=frozenset({int}),
        source_data=1,
    )
    second = LiteralizeResult(
        declaration_code="second = 2",
        preamble=("import b", "import c"),
        body_preamble=("class B: ...", "class C: ..."),
        pre_declaration_comments=("# second",),
        types_present=frozenset({str}),
        source_data="two",
    )

    result = compose(results=(first, second), language=PYTHON)

    assert result.declaration_code == "first = 1\nsecond = 2"
    assert result.preamble == ("import a", "import b", "import c")
    assert result.body_preamble == (
        "class A: ...",
        "class B: ...",
        "class C: ...",
    )
    assert result.pre_declaration_comments == ("# first", "# second")
    assert result.types_present == frozenset({int, str})
    assert result.source_data == [1, "two"]
    assert result.code == (
        "class A: ...\n"
        "class B: ...\n"
        "class C: ...\n"
        "# first\n"
        "# second\n"
        "first = 1\n"
        "second = 2"
    )


def test_compose_wrap_in_file_folds_preambles_into_code() -> None:
    """``wrap_in_file=True`` returns a self-contained code result."""
    first = LiteralizeResult(
        declaration_code="first = 1",
        preamble=("import a", "import b"),
        body_preamble=("class A: ...", "class B: ..."),
        pre_declaration_comments=("# first",),
    )
    second = LiteralizeResult(
        declaration_code="second = 2",
        preamble=("import b", "import c"),
        body_preamble=("class B: ...", "class C: ..."),
        pre_declaration_comments=("# second",),
    )

    result = compose(
        results=(first, second),
        language=PYTHON,
        wrap_in_file=True,
    )

    assert result.preamble == ()
    assert result.body_preamble == ()
    assert result.pre_declaration_comments == ()
    assert result.declaration_code == (
        "import a\n"
        "import b\n"
        "import c\n"
        "class A: ...\n"
        "class B: ...\n"
        "class C: ...\n"
        "# first\n"
        "# second\n"
        "first = 1\n"
        "second = 2"
    )


def test_compose_literalize_and_call_deduplicates_preamble() -> None:
    """``compose`` supports the declaration-plus-ref-call workflow."""
    python = Python(date_format=Python.date_formats.PYTHON)
    declaration = literalize(
        source="2026-01-01",
        input_format=InputFormat.YAML,
        language=python,
        variable_form=NewVariable(name="my_date"),
    )
    call = literalize_call(
        source='[[{"$ref": "my_date"}, 2026-01-02]]',
        input_format=InputFormat.YAML,
        language=python,
        target_function="process",
        parameter_names=["first", "second"],
    )

    result = compose(
        results=(declaration, call),
        language=python,
        wrap_in_file=True,
    )

    assert result.code == (
        "import datetime\n"
        "my_date = datetime.date(year=2026, month=1, day=1)\n"
        "process("
        "first=my_date, "
        "second=datetime.date(year=2026, month=1, day=2)"
        ")"
    )


def test_compose_merges_multiline_preamble_blocks() -> None:
    """Generated preamble variants with the same wrapper are merged."""
    first = LiteralizeResult(
        declaration_code="first",
        preamble=("pub type GVal {\n  GInt(Int)\n}",),
        body_preamble=(),
    )
    second = LiteralizeResult(
        declaration_code="second",
        preamble=("pub type GVal {\n  GList(List(GVal))\n}",),
        body_preamble=(),
    )

    result = compose(results=(first, second), language=PYTHON)

    assert result.preamble == (
        "pub type GVal {\n  GInt(Int)\n  GList(List(GVal))\n}",
    )
