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
            '[{"id":100,"label":"first item","enabled":false,'
            '"related_ids":[102,103]},{"id":101,"label":"second item",'
            '"enabled":true,"related_ids":[100]}]'
        ),
        input_format=InputFormat.JSON,
        language=Cpp(
            heterogeneous_strategy=Cpp.heterogeneous_strategies.RECORD,
            language_version=Cpp.version_formats.CPP14,
            record_shape_names={
                frozenset({"id", "label", "enabled", "related_ids"}): (
                    "NamedType"
                ),
            },
        ),
    )

    assert result.code == (
        "std::vector<NamedType>{\n"
        '    NamedType{100, "first item", false, '
        "std::vector<int>{102, 103}},\n"
        '    NamedType{101, "second item", true, '
        "std::vector<int>{100}},\n"
        "}"
    )
    assert "LiteralizerVariant" not in result.code
    assert "Record" not in result.code
    assert "std::variant" not in result.code
    assert "LiteralizerVariant" not in "\n".join(result.preamble)


def test_cpp14_unmapped_record_shape_uses_deduced_vector() -> None:
    """Unmapped C++14 records retain the generated-record vector form."""
    result = literalize(
        source='[{"id":100},{"id":101}]',
        input_format=InputFormat.JSON,
        language=Cpp(
            heterogeneous_strategy=Cpp.heterogeneous_strategies.RECORD,
            language_version=Cpp.version_formats.CPP14,
        ),
    )

    assert result.code == (
        "std::vector{\n    Record0{100},\n    Record0{101},\n}"
    )


def test_cpp14_record_null_substitutions_drive_field_types() -> None:
    """Different field substitutions are applied before record
    inference.
    """
    result = literalize(
        source=(
            '[{"due_date":null,"parent_id":null,"assignee":null},'
            '{"due_date":10,"parent_id":20,"assignee":"alice"}]'
        ),
        input_format=InputFormat.JSON,
        language=Cpp(
            heterogeneous_strategy=Cpp.heterogeneous_strategies.RECORD,
            language_version=Cpp.version_formats.CPP14,
        ),
        record_null_substitutions={
            "due_date": -1,
            "parent_id": -1,
            "assignee": "",
        },
    )

    assert result.code == (
        "std::vector{\n"
        '    Record0{-1, -1, ""},\n'
        '    Record0{10, 20, "alice"},\n'
        "}"
    )
    assert result.preamble[-1] == (
        "struct Record0 { int due_date{}; int parent_id{}; "
        "std::string assignee; };"
    )
