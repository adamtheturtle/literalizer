"""Golden coverage for unwrapped :class:`LiteralizeResult` prefixes."""

from pathlib import Path
from typing import Literal

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
from literalizer import FileWrapperContext, InputFormat, NewVariable

from .golden_checks import check_golden
from .language_specs import make_golden_path, with_per_fixture_module_name
from .unwrapped_result_cases import RESULT_CASES as _CASES
from .unwrapped_result_cases import RecordConsumer, record_consumer_specs


@pytest.mark.parametrize(
    argnames="lang_cls",
    argvalues=_CASES.prefix.languages,
    ids=lambda lang_cls: lang_cls.__name__,
)
@pytest.mark.parametrize(argnames="attribute", argvalues=_CASES.attributes)
def test_unwrapped_literalize_result_golden(
    *,
    lang_cls: literalizer.LanguageCls,
    attribute: Literal["code", "bare_code"],
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Compile each result view, supplying only its missing preamble."""
    golden_path = make_golden_path(
        parent=cases_dir / _CASES.prefix.input_case,
        name=f"{lang_cls.__name__}_unwrapped_{attribute}",
        extension=lang_cls.extension,
        lang_cls=lang_cls,
        version=lang_cls().language_version,
    )
    spec = with_per_fixture_module_name(
        spec=lang_cls(), golden_path=golden_path
    )
    result = literalizer.literalize(
        source=(cases_dir / _CASES.prefix.input_case / "input.yaml").read_text(
            encoding="utf-8"
        ),
        input_format=InputFormat.YAML,
        language=spec,
        variable_form=NewVariable(
            name=_CASES.prefix.variable_name, modifiers=frozenset()
        ),
        wrap_in_file=False,
    )
    assert len(result.body_preamble) > 0
    assert len(result.pre_declaration_comments) > 0
    contents_by_attribute = {
        "code": result.code,
        "bare_code": result.bare_code,
    }
    contents = spec.wrap_in_file(
        content=contents_by_attribute[attribute],
        context=FileWrapperContext(
            line_prefix="",
            bound_variable_names=(),
            variable_name=_CASES.prefix.variable_name,
            modifiers=frozenset(),
            body_preamble=result.body_preamble
            if attribute == "bare_code"
            else (),
            class_preamble=(),
            has_literal_declarations=True,
            generated_body_preamble=(),
            call_stub_names=frozenset(),
            root_is_object_literal=False,
            root_mapping_entries=None,
            has_existing_bindings=False,
        ),
    )
    check_golden(
        contents=contents + "\n",
        extension=spec.extension,
        golden_path=golden_path,
        file_regression=file_regression,
    )


@pytest.mark.parametrize(
    argnames="consumer",
    argvalues=_CASES.record_consumers,
    ids=lambda consumer: consumer.language.__name__,
)
@pytest.mark.parametrize(argnames="attribute", argvalues=_CASES.attributes)
def test_unwrapped_record_collection_golden(
    *,
    consumer: RecordConsumer,
    attribute: Literal["code", "bare_code"],
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Splice actual result views into a caller's native collection.

    Keep returned preambles in their declared scopes without recomputing
    or reconciling them. A type declaration in the expression breaks the
    consumer (including the Scala regression from issue #3615).
    """
    lang_cls = consumer.language
    for record_spec in record_consumer_specs(consumer=consumer):
        version = record_spec.language_version
        with subtests.test(version=version.name):
            golden_path = make_golden_path(
                parent=cases_dir / _CASES.record_input_case,
                name=f"{lang_cls.__name__}_unwrapped_record_{attribute}",
                extension=lang_cls.extension,
                lang_cls=lang_cls,
                version=version,
            )
            spec = with_per_fixture_module_name(
                spec=record_spec,
                golden_path=golden_path,
            )
            result = literalizer.literalize(
                source=(
                    cases_dir / _CASES.record_input_case / "input.yaml"
                ).read_text(encoding="utf-8"),
                input_format=InputFormat.YAML,
                language=spec,
                wrap_in_file=False,
            )
            contents = consumer.template.format(
                preamble="\n".join(result.preamble),
                body_preamble="\n".join(result.body_preamble)
                if attribute == "bare_code"
                else "",
                code=result.code if attribute == "code" else result.bare_code,
                module_name=(
                    f"Fixture_{golden_path.parent.name}_"
                    f"{golden_path.stem.rsplit(sep='@', maxsplit=1)[0]}"
                ),
            )
            check_golden(
                contents=contents,
                extension=spec.extension,
                golden_path=golden_path,
                file_regression=file_regression,
            )
