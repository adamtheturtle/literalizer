"""Skip reasons and policies shared by literalize scenarios."""

from beartype import beartype

from literalizer.exceptions import (
    ExcessiveNestingError,
    ExistingVariableNotSelfContainedError,
    HeterogeneousCollectionError,
    IncompatibleFormatsError,
    InvalidDictKeyError,
    NullInCollectionError,
    UnrepresentableEmptyDictError,
    UnrepresentableInputError,
    UnrepresentableIntegerError,
    UnrepresentableSpecialFloatError,
)

from .golden_checks import SkipPolicy, SkipReason, SkipReasons

_COMMON_SKIP_REASONS: SkipReasons = (
    SkipReason(
        error=ExcessiveNestingError,
        reason="exceeds the target's safe collection nesting limit",
    ),
    SkipReason(
        error=ExistingVariableNotSelfContainedError,
        reason="complete file cannot contain an undeclared existing variable",
    ),
    SkipReason(
        error=UnrepresentableIntegerError,
        reason="cannot represent integer in this input",
    ),
    SkipReason(
        error=UnrepresentableEmptyDictError,
        reason="cannot represent an empty dict",
    ),
)

LANGUAGE_SKIP_REASONS: SkipReasons = (
    *_COMMON_SKIP_REASONS,
    SkipReason(
        error=HeterogeneousCollectionError,
        reason="cannot represent this heterogeneous input",
    ),
    SkipReason(
        error=NullInCollectionError,
        reason="cannot represent null in a collection",
    ),
    SkipReason(
        error=UnrepresentableInputError,
        reason="cannot represent this input",
    ),
)

VARIANT_SKIP_REASONS: SkipReasons = (
    *_COMMON_SKIP_REASONS,
    SkipReason(
        error=NullInCollectionError,
        reason="rejects null elements in this input",
    ),
    SkipReason(
        error=HeterogeneousCollectionError,
        reason="cannot represent this heterogeneous input",
    ),
    SkipReason(
        error=IncompatibleFormatsError,
        reason="combination cannot represent this input",
    ),
    SkipReason(
        error=UnrepresentableSpecialFloatError,
        reason="cannot represent special floats in this input",
    ),
    SkipReason(
        error=UnrepresentableInputError,
        reason="cannot represent this input",
    ),
)


@beartype
def _reasons_for(
    *,
    reasons: SkipReasons,
    errors: tuple[type[Exception], ...],
) -> SkipReasons:
    """Return the entries of *reasons* covering exactly *errors*.

    A scenario that should skip on fewer errors than a table lists
    narrows the table rather than restating a reason, so the message
    for an error stays written once.
    """
    return tuple(entry for entry in reasons if entry.error in errors)


# Rendering the paired fixture under a non-default heterogeneous
# strategy skips only where the strategy cannot represent it; every
# other error is a real failure, so the table is narrowed rather than
# reused whole.
STRATEGY_SKIP_REASONS: SkipReasons = _reasons_for(
    reasons=LANGUAGE_SKIP_REASONS,
    errors=(HeterogeneousCollectionError,),
)


LANGUAGE_SKIPS: SkipPolicy = SkipPolicy(
    reasons=LANGUAGE_SKIP_REASONS,
    suffix="",
)
"""An input the language itself cannot represent skips."""

VARIANT_SKIPS: SkipPolicy = SkipPolicy(
    reasons=VARIANT_SKIP_REASONS,
    suffix="",
)
"""An input the variant's spec cannot represent skips."""


VARIANT_MAPPING_KEY_SKIPS: SkipPolicy = SkipPolicy(
    reasons=(
        *VARIANT_SKIP_REASONS,
        SkipReason(
            error=InvalidDictKeyError,
            reason="cannot represent a mapping key",
        ),
    ),
    suffix=VARIANT_SKIPS.suffix,
)
