"""Cross-language tests for the default heterogeneous-strategy error
contract.

Languages with an opt-in wrapping strategy (Rust's ``TAGGED_ENUM``,
Dhall's ``UNION_TYPE``, the Nim ``OBJECT_VARIANT``, and the Mojo
``VARIANT``) must still raise on heterogeneous input under the default
``ERROR`` strategy.  The integration framework catches
``HeterogeneousCollectionError`` and silently skips, so the error
contract has no golden-file surface and needs unit coverage.
"""

import pytest

from literalizer import InputFormat, LanguageCls, literalize
from literalizer.exceptions import (
    HeterogeneousScalarCollectionError,
    HeterogeneousSiblingListsError,
)
from literalizer.languages import Dhall, Mojo, Nim, Rust


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=[Rust, Dhall, Nim, Mojo],
)
@pytest.mark.parametrize(
    argnames=("source", "expected_exception"),
    argvalues=[
        ('{"a": 1, "b": "x"}', HeterogeneousScalarCollectionError),
        ('[[1, 2], ["a", "b"]]', HeterogeneousSiblingListsError),
    ],
)
def test_default_strategy_raises_on_heterogeneous(
    language_cls: LanguageCls,
    source: str,
    expected_exception: type[Exception],
) -> None:
    """Default spec raises on heterogeneous scalar input."""
    with pytest.raises(expected_exception=expected_exception):
        literalize(
            source=source,
            input_format=InputFormat.JSON,
            language=language_cls(),
        )
