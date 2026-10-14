"""Public callback contracts not expressible by manifest templates."""

import pytest

import literalizer
from literalizer.languages import Python


@pytest.mark.parametrize(
    argnames=("zip_source", "include_zipped", "expected_preamble"),
    argvalues=[
        ("2024-01-15T12:00:00", True, ("import datetime",)),
        ("2024-01-15T12:00:00", False, ()),
        (None, False, ()),
    ],
)
def test_opaque_call_transform_preamble(
    zip_source: str | None,
    *,
    include_zipped: bool,
    expected_preamble: tuple[str, ...],
) -> None:
    """Keep ordinary string callbacks compatible at their source
    boundary.
    """
    contexts: list[literalizer.CallContext] = []

    def transform(context: literalizer.CallContext, /) -> str:
        """Return caller-owned source without a template usage
        attribute.
        """
        contexts.append(context)
        if include_zipped:
            return f"check({context.call}, {context.zipped})"
        return context.call

    result = literalizer.literalize_call(
        source="1",
        input_format=literalizer.InputFormat.JSON,
        language=Python(),
        target_function="process",
        parameter_names=("value",),
        per_element=False,
        call_transform=transform,
        zip_source=zip_source,
        zip_input_format=None
        if zip_source is None
        else literalizer.InputFormat.YAML,
    )
    assert result.preamble == expected_preamble
    assert len(contexts) == 1
    assert contexts[0].index == 0
    assert tuple(contexts[0].row) == (1,)
    expected_code = "process(value=1)"
    if include_zipped:
        expected_code = (
            "check(process(value=1), datetime.datetime(year=2024, month=1, "
            "day=15, hour=12, minute=0, second=0))"
        )
    assert result.code == expected_code
