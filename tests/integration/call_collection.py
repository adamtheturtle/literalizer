"""Collect call cases and versioned rendering records."""

import dataclasses
import functools
from pathlib import Path

from beartype import beartype

import literalizer
from literalizer._enums import enum_payload

from .call_expectations import expected_call_shape_exception
from .case_manifests import CallCaseSpec, call_case_specs
from .language_specs import make_golden_path, make_spec, sorted_languages

CASES_DIR = Path(__file__).parent / "cases"


@dataclasses.dataclass(frozen=True, kw_only=True)
class CallRendering:
    """One call configuration, effective spec and expected outcome."""

    config: CallCaseSpec
    lang_cls: literalizer.LanguageCls
    spec: literalizer.Language
    golden_name: str
    expected_exception: type[Exception] | None

    def golden_path(self, *, cases_dir: Path) -> Path:
        """Return the fixture used for comparison and stale-file
        cleanup.
        """
        return make_golden_path(
            parent=cases_dir / self.config.case_dir_name,
            name=self.config.golden_name(name=self.golden_name),
            lang_cls=self.lang_cls,
            version=self.spec.language_version,
        )


@dataclasses.dataclass(frozen=True)
class CallCase:
    """A parameterized call-style golden-file test case."""

    config: CallCaseSpec
    lang_cls: literalizer.LanguageCls
    expected_exception: type[Exception] | None

    @property
    def test_id(self) -> str:
        """Return the manifest and language identity of this case."""
        return f"{self.config.coverage_id}/{self.lang_cls.__name__}"

    @property
    def renderings(self) -> tuple[CallRendering, ...]:
        """Exercise the default call once per supported language
        version.
        """
        return tuple(
            CallRendering(
                config=self.config,
                lang_cls=self.lang_cls,
                spec=make_spec(
                    lang_cls=self.lang_cls, language_version=version
                ),
                golden_name=f"{self.lang_cls.__name__}_call",
                expected_exception=self.expected_exception,
            )
            for version in self.lang_cls.VersionFormats
        )


@functools.cache
@beartype
def default_call_case_specs() -> tuple[CallCaseSpec, ...]:
    """Return every call case driven by the default per-language
    matrix.
    """
    return tuple(
        spec
        for spec in call_case_specs(cases_dir=CASES_DIR)
        if not spec.variant_only
    )


@functools.cache
@beartype
def discover_call_cases() -> list[CallCase]:
    """Return call test cases for all languages."""
    cases: list[CallCase] = []
    for config in default_call_case_specs():
        for lang_cls in sorted_languages():
            if not config.admits_language(lang_cls=lang_cls):
                continue
            if len(lang_cls.CallStyles) == 0:
                continue
            if (
                config.requires_heterogeneous_dict_values
                and not lang_cls.dict_supports_heterogeneous_values
            ):
                continue
            if config.call_style_type is not None:
                # Only include languages that have this as a
                # non-default style.
                styles = list(lang_cls.CallStyles)
                matching = [
                    s
                    for s in styles
                    if isinstance(
                        enum_payload(member=s, payload_type=object),
                        config.call_style_type,
                    )
                ]
                if len(matching) == 0:
                    continue
                default_style = styles[0]
                if isinstance(
                    enum_payload(member=default_style, payload_type=object),
                    config.call_style_type,
                ):
                    continue
            expected_exception = expected_call_shape_exception(
                lang_cls=lang_cls,
                config=config,
                spec=make_spec(lang_cls=lang_cls),
            )
            cases.append(
                CallCase(
                    config=config,
                    lang_cls=lang_cls,
                    expected_exception=expected_exception,
                )
            )
    return cases
