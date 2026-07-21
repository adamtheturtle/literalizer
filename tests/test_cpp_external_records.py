"""C++ caller-declared ``RECORD`` shape coverage."""

from literalizer import InputFormat, literalize
from literalizer.languages import Cpp


def test_cpp14_external_record_shape_uses_typed_positional_aggregate() -> None:
    """Mapped C++14 records use the starter-code type without a
    preamble.
    """
    assert not Cpp.record_shape_names_emit_declarations
    result = literalize(
        source=(
            '[{"id":100,"description":"first task","is_done":false,'
            '"blocks":[102,103]},{"id":101,"description":"second task",'
            '"is_done":true,"blocks":[100]}]'
        ),
        input_format=InputFormat.JSON,
        language=Cpp(
            heterogeneous_strategy=Cpp.heterogeneous_strategies.RECORD,
            language_version=Cpp.version_formats.CPP14,
            record_shape_names={
                frozenset({"id", "description", "is_done", "blocks"}): (
                    "NamedType"
                ),
            },
        ),
    )

    assert result.code == (
        "std::vector<NamedType>{\n"
        '    NamedType{100, "first task", false, '
        "std::vector<int>{102, 103}},\n"
        '    NamedType{101, "second task", true, '
        "std::vector<int>{100}},\n"
        "}"
    )
    assert "LiteralizerVariant" not in result.code
    assert "Record" not in result.code
    assert "std::variant" not in result.code
    assert "LiteralizerVariant" not in "\n".join(result.preamble)
