"""External C++ record ownership is unknown to the generated fragment.

The caller supplies the named class, so this incomplete reference cannot
use a compiling golden without inventing its resource ownership.
"""

import enum

import pytest

from literalizer import InputFormat, LanguageCls, literalize
from literalizer.languages import Cpp


@pytest.mark.parametrize(
    argnames="version", argvalues=list(Cpp.VersionFormats)
)
def test_external_record_reference_keeps_its_move(
    version: enum.Enum,
) -> None:
    """Scalar input fields do not prove an external class is trivial."""
    language_cls: LanguageCls = Cpp
    result = literalize(
        source='{"$ref":"first"}',
        input_format=InputFormat.JSON,
        ref_key="$ref",
        ref_values={"first": {"child": {"value": 1}}},
        language=language_cls(
            language_version=version,
            heterogeneous_strategy=Cpp.heterogeneous_strategies["RECORD"],
            record_shape_names={frozenset({"value"}): "UserRecord"},
        ),
    )

    assert result.bare_code == "std::move(first)"
