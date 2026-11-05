"""Prove the CI oracle rejects a whitespace-only formatting defect."""

from pathlib import Path

from literalizer import InputFormat, NewVariable, SourceFormat, literalize
from literalizer.languages import ObjectiveC
from tests.integration.source_format_oracle import check_source_format


def main() -> None:
    """Keep the positive and negative controls on freshly rendered
    source.
    """
    program = literalize(
        source='{"value":42}',
        input_format=InputFormat.JSON,
        language=ObjectiveC(source_format=SourceFormat.CANONICAL, indent="  "),
        variable_form=NewVariable(name="data", modifiers=frozenset()),
        wrap_in_file=True,
    ).code
    check_source_format(contents=program, path=Path("positive-control.m"))
    # Adding one space between the type and identifier preserves all tokens.
    damaged = program.replace("id data =", "id  data =")
    if damaged == program:
        message = "The negative control did not change generated source"
        raise AssertionError(message)
    try:
        check_source_format(contents=damaged, path=Path("negative-control.m"))
    except AssertionError:
        return
    message = "The oracle accepted a formatting defect"
    raise AssertionError(message)


if __name__ == "__main__":
    main()
