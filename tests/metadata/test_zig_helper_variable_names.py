"""Copied Zig specifications recompute their occupied helper names."""

import dataclasses

from literalizer.languages import Zig


def test_replaced_spec_drops_previous_mode_reservations() -> None:
    """Derived binding metadata follows the options in a spec copy."""
    default = dataclasses.replace(
        Zig(json_type=Zig.JsonTypes["STD_JSON_VALUE"]), json_type=None
    )
    record = dataclasses.replace(
        Zig(), heterogeneous_strategy=Zig.HeterogeneousStrategies["RECORD"]
    )
    json = dataclasses.replace(
        Zig(), json_type=Zig.JsonTypes["STD_JSON_VALUE"]
    )
    assert default.reserved_variable_identifiers == (
        Zig().reserved_variable_identifiers
    )
    assert record.reserved_variable_identifiers == (
        Zig(
            heterogeneous_strategy=Zig.HeterogeneousStrategies["RECORD"]
        ).reserved_variable_identifiers
    )
    assert json.reserved_variable_identifiers == (
        Zig(
            json_type=Zig.JsonTypes["STD_JSON_VALUE"]
        ).reserved_variable_identifiers
    )
    assert json.reserved_identifiers == record.reserved_identifiers
