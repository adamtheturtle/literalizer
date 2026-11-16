"""Receiver participation and the external-reference inference
boundary.
"""

from pathlib import Path
from unittest.mock import Mock

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
from literalizer.languages import ALL_LANGUAGES, Cpp
from tests.integration import call_cases
from tests.integration.call_collection import (
    CallRendering,
    default_call_case_specs,
)
from tests.integration.call_receivers import integer_receiver_syntax
from tests.integration.language_specs import make_spec


def test_every_stateful_integer_signature_has_native_syntax() -> None:
    """Native syntax tables cannot silently sample capable backends."""
    assert set(integer_receiver_syntax()) == {
        cls.language_id
        for cls in ALL_LANGUAGES
        if cls.supports_stateful_free_call_consumers
    }


def test_external_integer_receiver_keeps_absent_inference_hints(
    *,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    pytestconfig: pytest.Config,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An observable external call needs neither stub inference nor
    hints.
    """
    config = next(
        config
        for config in default_call_case_specs()
        if config.example == "external_integer"
    )
    recorder = Mock(wraps=literalizer.literalize_call)
    monkeypatch.setattr(
        target=literalizer, name="literalize_call", value=recorder
    )
    for name in (
        "_resolve_refs_for_inference",
        "argument_values_for_stub",
        "target_call_declarations",
        "wrapper_call_declarations",
    ):
        monkeypatch.setattr(
            target=call_cases,
            name=name,
            value=Mock(side_effect=AssertionError("synthetic consumer used")),
        )
    call_cases.run_call_golden_case(
        rendering=CallRendering(
            config=config,
            lang_cls=Cpp,
            spec=make_spec(lang_cls=Cpp),
            golden_name="Cpp_call",
            expected_exception=None,
        ),
        cases_dir=cases_dir,
        file_regression=file_regression,
        pytest_config=pytestconfig,
    )
    calls = [
        call.kwargs
        for call in recorder.call_args_list
        if call.kwargs.get("target_function") == "process"
    ]
    assert len(calls) == 1
    assert calls[0]["ref_values"] == {}
    assert calls[0]["bound_refs"] is None
    assert calls[0]["wrap_in_file"] is False
