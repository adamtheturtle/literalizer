"""Record inference starts each pass independently of earlier
documents.
"""

import dataclasses
import enum
from typing import TYPE_CHECKING

import pytest

from literalizer.languages import Cpp
from tests.integration.language_specs import make_spec

if TYPE_CHECKING:
    from literalizer._types import Value


@pytest.mark.parametrize(
    argnames="version", argvalues=list(Cpp.VersionFormats)
)
def test_record_inference_does_not_split_equal_shapes_after_a_prior_pass(
    version: enum.Enum,
) -> None:
    """Shared and copied nested values infer the same record shapes."""
    language = make_spec(
        lang_cls=Cpp,
        language_version=version,
        heterogeneous_strategy=Cpp.HeterogeneousStrategies["RECORD"],
    )
    compute = language.heterogeneous_behavior.compute_record_shapes
    fresh_compute = dataclasses.replace(
        language
    ).heterogeneous_behavior.compute_record_shapes
    assert compute is not None
    assert fresh_compute is not None

    previous: Value = {"name": "first", "values": [1, 2]}
    copied: Value = {"name": "first", "values": [1, 2]}
    data: Value = [{"payload": [[previous]]}, {"payload": [[copied]]}]
    _ = compute(previous)

    assert compute(data) == fresh_compute(data)
