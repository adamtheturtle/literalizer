"""Public configuration and rendering for move-only C++ records."""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import InvalidRecordNameError
from literalizer.languages import Cpp


@pytest.mark.parametrize(
    argnames=("use_record_strategy", "record_name"),
    argvalues=[
        (False, "UserRecord"),
        (True, "UnknownRecord"),
    ],
)
def test_move_only_record_requires_a_configured_record_type(
    *, use_record_strategy: bool, record_name: str
) -> None:
    """Reject move-only types outside the configured record names."""
    strategies = Cpp.heterogeneous_strategies
    with pytest.raises(
        expected_exception=InvalidRecordNameError,
        match="move_only_record_names requires",
    ):
        _ = Cpp(
            heterogeneous_strategy=(
                strategies.RECORD if use_record_strategy else strategies.ERROR
            ),
            record_shape_names={frozenset({"value"}): "UserRecord"},
            move_only_record_names=frozenset({record_name}),
        )


def test_move_only_record_ownership_member_avoids_data_fields() -> None:
    """Keep the input field when selecting the generated member's name."""
    result = literalize(
        source='{"move_guard": 1}',
        input_format=InputFormat.JSON,
        language=Cpp(
            heterogeneous_strategy=Cpp.heterogeneous_strategies.RECORD,
            record_shape_names={frozenset({"move_guard"}): "UserRecord"},
            move_only_record_names=frozenset({"UserRecord"}),
        ),
        variable_form=NewVariable(name="record", modifiers=frozenset()),
        wrap_in_file=True,
    )

    assert "int move_guard{};" in result.code
    assert "std::unique_ptr<int> move_guardx = nullptr;" in result.code
