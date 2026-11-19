"""Read documented examples shared with the API rejection suite."""

import functools

from tests.errors.rejection_cases import RejectionCase, rejection_cases
from tests.errors.rejection_expectations import load_expected_messages
from tests.errors.rejection_manifests import (
    REJECTIONS_DIR,
    load_rejection_manifest,
)


@functools.cache
def rejected_examples(
    *, contract: str, error: type[Exception]
) -> tuple[RejectionCase, ...]:
    """Read the backend and option coverage from the existing error
    suite.
    """
    manifest = load_rejection_manifest(
        manifest_path=REJECTIONS_DIR / contract / "rejection.toml"
    )
    rejected = load_expected_messages(golden_path=manifest.golden_path)[
        error.__name__
    ]
    return tuple(
        case
        for case in rejection_cases(manifest=manifest)
        if case.case_id in rejected
    )
