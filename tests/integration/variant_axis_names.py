"""Names a case manifest may use to select variant coverage."""

from collections import Counter
from collections.abc import Collection

from .axis_builders import AxisError
from .variant_axes import AXES


def registered_names(
    *, ordinary: Collection[str], special: tuple[str, ...]
) -> frozenset[str]:
    """Check that every manifest name identifies exactly one expansion."""
    counts = Counter((*ordinary, *special))
    duplicates = sorted(name for name, count in counts.items() if count > 1)
    if len(duplicates) > 0:
        msg = f"duplicate variant axis registrations: {duplicates}"
        raise AxisError(msg)
    return frozenset(counts)


# Case assembly and the custom language builders own these contextual axes.
_SPECIAL_NAMES = (
    "json_type_variable_form",
    "modifier_sequence_format",
    "modifiers",
    "record_modifiers",
    "json_type_modifiers",
    "multiline_string_combined",
    "multiline_string_pre_indent",
    "plain_collection_callbacks",
    "typed_collection_callback",
    "custom_zig_null_policy",
    "copied_json_to_native",
    "copied_native_to_record",
    "copied_native_to_json",
    "existing_integer_suffix",
    "date_formatter_datetime_view",
)
SPECIAL_VARIANT_AXES = frozenset(_SPECIAL_NAMES)
KNOWN_VARIANT_AXES: frozenset[str] = registered_names(
    ordinary=AXES.keys(), special=_SPECIAL_NAMES
)
