"""C# record field type regression tests."""

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import CSharp


def test_csharp_record_empty_dict_field_uses_object() -> None:
    """An empty dict field uses the ``object`` top type."""
    result = literalize(
        source='{"title": "report", "extra": {}}',
        input_format=InputFormat.JSON,
        language=CSharp(
            heterogeneous_strategy=CSharp.heterogeneous_strategies.RECORD,
        ),
        variable_form=NewVariable(name="my_data"),
        wrap_in_file=True,
    )

    assert "record Record0(string Title, object Extra);" in (
        result.declaration_code
    )
