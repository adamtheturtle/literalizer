"""``literalize_call`` golden-file cases driven by language variants.

Covers call inputs that need a non-default language spec, such as
inputs that a default heterogeneous strategy rejects or calls rendered
with a non-default statement terminator.  Sibling to :mod:`call_cases`.

Which variants drive a case is declared by the case itself, in the
``[[call.variants]]`` tables of its ``case.toml``, so a call case is
described in one place.
"""

import dataclasses
import functools

from beartype import beartype

from .call_cases import CASES_DIR
from .case_manifests import CallCaseSpec, call_case_specs
from .variant_cases import Variant, variants_for_axis


@dataclasses.dataclass(frozen=True)
class CallVariantCase:
    """A ``literalize_call`` golden-file case run with a non-default
    language spec (e.g. a ``TAGGED_ENUM`` strategy).
    """

    config: CallCaseSpec
    variant: Variant


@functools.cache
@beartype
def build_call_variant_cases() -> list[CallVariantCase]:
    """Return call-test cases for the variant axes cases declare.

    A case names an axis when the default spec cannot represent its
    input -- which makes :func:`test_call_golden_file` skip -- or when
    the call is only interesting under a non-default option, such as a
    statement terminator or a JSON-aware result binding.
    """
    return [
        CallVariantCase(config=config, variant=variant)
        for config in call_case_specs(cases_dir=CASES_DIR)
        for manifest_variant in config.variants
        for variant in variants_for_axis(axis_key=manifest_variant.axis)
    ]
