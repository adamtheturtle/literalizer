"""Native controls for the integer receiver's independent event
contract.
"""

import dataclasses
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

import literalizer
from literalizer.exceptions import CallArgNotSupportedError
from tests.integration.call_receivers import (
    compose_integer_calls,
    integer_receiver_syntax,
)
from tests.integration.call_transforms import call_transform_for_case
from tests.integration.case_manifests import (
    CallCaseSpec,
    CallOperandSpec,
    CallWrapperSpec,
    ComposedCallFixture,
    FollowupCallSpec,
)
from tests.integration.language_specs import (
    find_redefinition_styles,
    fixture_module_name,
    make_spec,
    sorted_languages,
    with_per_fixture_module_name,
)


def _call(
    *,
    config: CallCaseSpec,
    spec: literalizer.Language,
    source: str,
    target: str,
    variable_form: literalizer.ExistingVariable | None,
    transform: bool,
) -> literalizer.LiteralizeResult:
    """Render a real call without adding reference inference knowledge."""
    return literalizer.literalize_call(
        source=source,
        input_format=literalizer.InputFormat.JSON,
        language=spec,
        target_function=target,
        ref_key="$ref",
        parameter_names=config.parameter_names,
        per_element=config.per_element,
        variable_form=variable_form,
        call_transform=(
            call_transform_for_case(config=config, spec=spec)
            if transform
            else None
        ),
        zip_source=config.zip_source if transform else None,
        zip_input_format=config.zip_input_format if transform else None,
    )


def _program(*, spec: literalizer.Language, control: str) -> str:
    """Vary public inputs and caller composition, retaining expected
    events.
    """
    config = CallCaseSpec.model_validate(
        obj={
            "target_function": "process",
            "parameter_names": ("value",),
            "per_element": True,
            "integer_receiver_events": (("call", 1), ("call", 2)),
        },
        context={"case_dir_name": "receiver_control"},
    )
    source = {
        "plain": "[[1], [2]]",
        "dropped": "[[1]]",
        "repeated": "[[1], [1], [2]]",
        "reordered": "[[2], [1]]",
    }.get(control, "[[1], [2]]")
    if control in {"zipped", "swapped", "wrong_return"}:
        config = config.model_copy(
            update={
                "integer_receiver_events": (
                    ("call", 1),
                    ("result", 101),
                    ("zipped", 41),
                    ("call", 2),
                    ("result", 102),
                    ("zipped", 42),
                ),
                "zip_source": "[41, 42]",
                "zip_input_format": literalizer.InputFormat.JSON,
                "transform": CallWrapperSpec(
                    kind="wrapper",
                    target="emit",
                    arguments=(
                        CallOperandSpec(
                            role="zipped" if control == "swapped" else "call",
                            parameter="actual",
                        ),
                        CallOperandSpec(
                            role="call" if control == "swapped" else "zipped",
                            parameter="zipped",
                        ),
                    ),
                ),
            }
        )
    if control == "unary_wrapper":
        config = config.model_copy(
            update={
                "integer_receiver_events": (
                    ("call", 1),
                    ("result", 101),
                    ("call", 2),
                    ("result", 102),
                ),
                "transform": CallWrapperSpec(
                    kind="wrapper",
                    target="emit",
                    arguments=(
                        CallOperandSpec(role="call", parameter="actual"),
                    ),
                ),
            }
        )
    fragments: list[literalizer.LiteralizeResult] = []
    if control in {"binding", "wrong_binding"}:
        config = config.model_copy(
            update={
                "per_element": False,
                "integer_receiver_events": (
                    ("result", 0),
                    ("call", 1),
                    ("result", 101),
                ),
                "fixture": ComposedCallFixture(
                    followup=FollowupCallSpec(
                        source='{"$ref": "my_data"}', target_function="consume"
                    )
                ),
                "variable_form": literalizer.ExistingVariable(name="my_data"),
            }
        )
        fragments.append(
            literalizer.literalize(
                source="0",
                input_format=literalizer.InputFormat.JSON,
                language=spec,
                variable_form=literalizer.NewVariable(
                    name="my_data", modifiers=frozenset()
                ),
            )
        )
        fragments.append(
            _call(
                config=config,
                spec=spec,
                source='{"$ref": "my_data"}',
                target="consume",
                variable_form=None,
                transform=False,
            )
        )
        source = "1"
    fragments.append(
        _call(
            config=config,
            spec=spec,
            source=source,
            target="process",
            variable_form=(
                literalizer.ExistingVariable(name="my_data")
                if control in {"binding", "wrong_binding"}
                else None
            ),
            transform=True,
        )
    )
    if control in {"binding", "wrong_binding"}:
        fragments.append(
            _call(
                config=config,
                spec=spec,
                source='{"$ref": "my_data"}',
                target="consume",
                variable_form=None,
                transform=False,
            )
        )
    return compose_integer_calls(
        config=config,
        spec=spec,
        fragments=fragments,
        return_increment=101
        if control in {"wrong_return", "wrong_binding"}
        else 100,
    )


def _control_programs(
    *, lang_cls: literalizer.LanguageCls, tmp_path: Path
) -> list[tuple[str, Path, str]]:
    """Render every control before checking local tool availability."""
    spec = make_spec(lang_cls=lang_cls)
    styles = find_redefinition_styles(spec=spec)
    spec = dataclasses.replace(
        spec, declaration_style=next(iter(styles), spec.declaration_style)
    )
    programs: list[tuple[str, Path, str]] = []
    for control in (
        "plain",
        "dropped",
        "repeated",
        "reordered",
        "unary_wrapper",
        "zipped",
        "swapped",
        "wrong_return",
        "binding",
        "wrong_binding",
    ):
        directory = tmp_path / control
        directory.mkdir()
        # The source filename must match the public class name where required.
        # Other backends need an identifier filename without a version tag.
        identity = directory / ("ReceiverControl" + lang_cls.extension)
        module_name = fixture_module_name(golden_path=identity)
        effective_spec = with_per_fixture_module_name(
            spec=spec, golden_path=identity
        )
        path = directory / (module_name + lang_cls.extension)
        try:
            program = _program(spec=effective_spec, control=control)
        except CallArgNotSupportedError:
            # Some free-function consumers reject reference arguments in
            # the public API. Retain that boundary without supplying hints.
            assert control in {"binding", "wrong_binding"}
            continue
        _ = path.write_text(data=program, encoding="utf-8")
        programs.append((control, path, module_name))
    return programs


@pytest.mark.parametrize(
    argnames="lang_cls",
    argvalues=[
        cls
        for cls in sorted_languages()
        if cls.supports_stateful_free_call_consumers
    ],
    ids=lambda cls: cls.language_id,
)
def test_native_receiver_controls(
    *, lang_cls: literalizer.LanguageCls, tmp_path: Path
) -> None:
    """Valid calls pass; six behavior mutations fail in the native runtime."""
    programs = _control_programs(lang_cls=lang_cls, tmp_path=tmp_path)
    syntax = integer_receiver_syntax()[lang_cls.language_id]
    command = syntax.compile if len(syntax.compile) > 0 else syntax.execute
    executable = command[0].format(python=sys.executable)
    resolved_executable = shutil.which(cmd=executable)
    if resolved_executable is None:
        pytest.skip(reason=f"{executable} is unavailable")
    if executable == "dotnet":
        sdks = subprocess.run(  # noqa: S603 - inspect the selected native tool
            args=[resolved_executable, "--list-sdks"],
            capture_output=True,
            text=True,
            check=True,
        )
        if len(sdks.stdout.strip()) == 0:
            pytest.skip(reason="the .NET SDK is unavailable")
    if lang_cls.language_id == "objective_c" and sys.platform != "darwin":
        pytest.skip(reason="Foundation execution requires macOS")
    for control, path, module_name in programs:
        directory = path.parent
        fields = {
            "python": sys.executable,
            "source": str(object=path),
            "output": str(object=directory / "run.exe"),
            "directory": str(object=directory),
            "module_name": module_name,
            "repository": str(object=Path(__file__).parents[2]),
        }
        if len(syntax.compile) > 0:
            built = subprocess.run(  # noqa: S603 - execute repository-owned native receivers
                args=[
                    resolved_executable,
                    *(arg.format(**fields) for arg in syntax.compile[1:]),
                ],
                capture_output=True,
                text=True,
                timeout=syntax.compile_timeout_seconds,
                check=False,
                cwd=directory,
            )
            assert built.returncode == 0, built.stderr + built.stdout
            execution = [arg.format(**fields) for arg in syntax.execute]
        else:
            execution = [
                resolved_executable,
                *(arg.format(**fields) for arg in syntax.execute[1:]),
            ]
        completed = subprocess.run(  # noqa: S603 - execute repository-owned native receivers
            args=execution,
            input=str(object=path) + "\0" if syntax.path_on_stdin else None,
            capture_output=True,
            text=True,
            # Allow cold runtime startup on hosted Windows workers.
            timeout=180,
            check=False,
            cwd=directory,
        )
        expected_success = control in {
            "plain",
            "unary_wrapper",
            "zipped",
            "binding",
        }
        assert (completed.returncode == 0) is expected_success, (
            control,
            completed.stdout,
            completed.stderr,
        )
