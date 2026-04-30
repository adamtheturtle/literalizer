"""``literalize_call`` golden-file tests.

Drives each call-case configuration against every supporting language,
both for default specs and for non-default language variants (e.g.
Rust's ``TAGGED_ENUM`` strategy on inputs the default ``ERROR``
strategy rejects).
"""

from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from literalizer.languages import Sml

from .call_cases import (
    CallCase,
    CallCaseConfig,
    discover_call_cases,
    lang_satisfies_config_constraints,
    run_call_golden_case,
)
from .call_variant_cases import CallVariantCase, build_call_variant_cases
from .language_specs import make_spec


@pytest.mark.parametrize(
    argnames="call_case",
    argvalues=discover_call_cases(),
    ids=[
        f"{c.config.case_dir_name}/{c.lang_cls.__name__}"
        for c in discover_call_cases()
    ],
)
def test_call_golden_file(
    call_case: CallCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Test that literalize_call output matches expected golden file."""
    config = call_case.config
    lang_cls = call_case.lang_cls
    kwargs: dict[str, object] = {}
    if config.call_style_type is not None:
        style = next(
            s
            for s in lang_cls.CallStyles
            if isinstance(s.value, config.call_style_type)
        )
        kwargs["call_style"] = style
    spec = make_spec(lang_cls=lang_cls, **kwargs)
    run_call_golden_case(
        config=config,
        spec=spec,
        golden_name=f"{lang_cls.__name__}_call",
        cases_dir=cases_dir,
        file_regression=file_regression,
    )


@pytest.mark.parametrize(
    argnames="call_variant_case",
    argvalues=build_call_variant_cases(),
    ids=[
        f"{c.config.case_dir_name}/{c.variant.name}"
        for c in build_call_variant_cases()
    ],
)
def test_call_variant_golden_file(
    call_variant_case: CallVariantCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Test ``literalize_call`` for a non-default language spec.

    Covers call inputs that the language's default
    :attr:`Language.heterogeneous_strategy` rejects, which
    :func:`test_call_golden_file` skips — in particular the
    sibling-widening behavior of Rust's ``TAGGED_ENUM`` across
    per-element call arguments.
    """
    run_call_golden_case(
        config=call_variant_case.config,
        spec=call_variant_case.variant.spec,
        golden_name=f"{call_variant_case.variant.name}_call",
        cases_dir=cases_dir,
        file_regression=file_regression,
    )


def test_lang_satisfies_config_constraints_reserved_identifier() -> None:
    """Return False when the target function name is reserved in the
    language.
    """
    config = CallCaseConfig(
        case_dir_name="test",
        target_function="app.mgr.op",
        parameter_names=[],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=False,
        ref_case_per_language=False,
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
    )
    assert not lang_satisfies_config_constraints(lang_cls=Sml, config=config)
