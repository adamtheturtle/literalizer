"""Caller mutation preserves complete native record consumers."""

import dataclasses
from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from literalizer import Language, LiteralizeResult, literalize
from literalizer.languages import Rust

from .case_manifests import case_input
from .golden_checks import check_golden
from .language_specs import make_golden_path
from .record_snapshot_cases import (
    RECORD_SNAPSHOT_CASES,
    RecordSnapshotCase,
    snapshot_rendering,
)


@pytest.mark.parametrize(
    argnames="case",
    argvalues=RECORD_SNAPSHOT_CASES,
    ids=lambda case: case.name,
)
def test_record_snapshot_golden(
    case: RecordSnapshotCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Compile both actual results around the original caller
    mutations.
    """
    rendering = snapshot_rendering(case=case)
    input_info = case_input(case_dir=cases_dir / case.case_name)
    source = input_info.path.read_text(encoding="utf-8")
    for version in rendering.versions:
        with subtests.test(version=version.name):
            seed = rendering.spec_for(version=version)
            rust_seed = seed
            assert isinstance(rust_seed, Rust)
            caller_names = dict(rust_seed.record_shape_names)
            language = dataclasses.replace(
                seed, record_shape_names=caller_names
            )

            def render(*, spec: Language) -> LiteralizeResult:
                """Return the actual expression and its native
                declarations.
                """
                return literalize(
                    source=source,
                    input_format=input_info.input_format,
                    language=spec,
                    variable_form=rendering.render.variable_form,
                    wrap_in_file=False,
                    pre_indent_level=1,
                    collection_layout=rendering.render.collection_layout,
                    record_null_substitutions=rendering.render.record_null_substitutions,
                )

            before = render(spec=language)
            caller_names[case.parent_fields] = case.parent_name
            caller_names[next(iter(caller_names))] = case.child_name
            after = render(spec=language)
            contents = case.consumer_template.format(
                preamble="\n".join(
                    dict.fromkeys((*before.preamble, *after.preamble))
                ),
                before=before.code,
                after=after.code,
            )
            path = make_golden_path(
                parent=cases_dir / case.case_name,
                name=case.golden_name,
                extension=Rust.extension,
                lang_cls=Rust,
                version=version,
            )
            check_golden(
                contents=contents,
                extension=Rust.extension,
                golden_path=path,
                file_regression=file_regression,
            )
