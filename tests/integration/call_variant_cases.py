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
from pathlib import Path

from beartype import beartype

from literalizer._enums import enum_payload

from .call_cases import (
    CallCase,
    CallRendering,
    discover_call_cases,
    expected_call_shape_exception,
)
from .case_manifests import CallCaseSpec, call_case_specs
from .variant_cases import Variant, variants_for_axis
from .variant_context import config_with_variant_layout


@dataclasses.dataclass(frozen=True)
class CallVariantCase:
    """A ``literalize_call`` golden-file case run with a non-default
    language spec (e.g. a ``TAGGED_ENUM`` strategy).
    """

    config: CallCaseSpec
    variant: Variant

    @property
    def test_id(self) -> str:
        """Return the manifest and variant identity of this case."""
        return f"{self.config.coverage_id}/{self.variant.name}"

    @property
    def renderings(self) -> tuple[CallRendering, ...]:
        """Exercise the plan's effective version and rejection policy once."""
        return (
            CallRendering(
                config=self.config,
                lang_cls=self.variant.lang_cls,
                spec=self.variant.spec,
                golden_name=f"{self.variant.name}_call",
                expected_exception=expected_call_shape_exception(
                    lang_cls=self.variant.lang_cls,
                    config=self.config,
                    spec=self.variant.spec,
                ),
            ),
        )


@functools.cache
@beartype
def build_call_variant_cases(*, cases_dir: Path) -> list[CallVariantCase]:
    """Return call-test cases for the variant axes cases declare.

    A case names an axis when the default spec cannot represent its
    input -- which makes the default rendering skip -- or when
    the call is only interesting under a non-default option, such as a
    statement terminator or a JSON-aware result binding.
    """
    return [
        CallVariantCase(
            config=config_with_variant_layout(
                config=config, layout=variant.collection_layout
            ),
            variant=variant,
        )
        for config in call_case_specs(cases_dir=cases_dir)
        for manifest_variant in config.variants
        for variant in variants_for_axis(axis_key=manifest_variant.axis)
        if config.admits_language(lang_cls=variant.lang_cls)
        if config.call_style_type is None
        or any(
            isinstance(
                enum_payload(member=style, payload_type=object),
                config.call_style_type,
            )
            for style in variant.lang_cls.CallStyles
        )
    ]


@beartype
def call_golden_cases(
    *, cases_dir: Path
) -> tuple[CallCase | CallVariantCase, ...]:
    """Return the cases shared by the call runner and fixture
    inventory.
    """
    return (
        *discover_call_cases(),
        *build_call_variant_cases(cases_dir=cases_dir),
    )
