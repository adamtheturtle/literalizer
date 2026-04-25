"""``literalize_call`` golden-file cases driven by language variants.

Covers call inputs that the language's default heterogeneous strategy
rejects, but which a non-default variant (e.g. Rust's ``TAGGED_ENUM``)
can represent.  Sibling to :mod:`call_cases`.
"""

import dataclasses
import functools
from collections.abc import Callable, Iterable

from beartype import beartype

from .call_cases import CALL_CASE_CONFIGS, CallCaseConfig
from .variant_cases import (
    Variant,
    build_heterogeneous_value_name_variants,
)


@dataclasses.dataclass(frozen=True)
class CallVariantCase:
    """A ``literalize_call`` golden-file case run with a non-default
    language spec (e.g. Rust's ``TAGGED_ENUM`` strategy).
    """

    config: CallCaseConfig
    variant: Variant


# Per-case language variants exercised by
# :func:`test_call_variant_golden_file`.  Each entry names a call-case
# directory and pairs it with the variant builders that produce a spec
# capable of representing that case's heterogeneous input — which the
# default spec rejects, causing :func:`test_call_golden_file` to skip.
CALL_VARIANT_SOURCES: list[tuple[str, Callable[[], Iterable[Variant]]]] = [
    ("call_mixed_type_dicts", build_heterogeneous_value_name_variants),
]


@functools.cache
@beartype
def build_call_variant_cases() -> list[CallVariantCase]:
    """Return call-test cases for language variants that accept
    heterogeneous input the default spec rejects.
    """
    cases: list[CallVariantCase] = []
    for case_dir_name, builder in CALL_VARIANT_SOURCES:
        config = next(
            cfg
            for cfg in CALL_CASE_CONFIGS
            if cfg.case_dir_name == case_dir_name
        )
        cases.extend(
            CallVariantCase(config=config, variant=variant)
            for variant in builder()
        )
    return cases
