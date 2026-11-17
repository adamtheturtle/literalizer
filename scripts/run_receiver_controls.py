"""Native controls for the integer receiver's independent event
contract.
"""

import dataclasses
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import click

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
    *, lang_cls: literalizer.LanguageCls, root: Path
) -> list[tuple[str, Path, str]]:
    """Render every positive and mutation control for one language."""
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
        directory = root / control
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
            if control not in {"binding", "wrong_binding"}:
                raise
            continue
        _ = path.write_text(data=program, encoding="utf-8")
        programs.append((control, path, module_name))
    return programs


def _run_controls(*, lang_cls: literalizer.LanguageCls, root: Path) -> None:
    """Valid calls pass; six behavior mutations fail in the native runtime."""
    programs = _control_programs(lang_cls=lang_cls, root=root)
    syntax = integer_receiver_syntax()[lang_cls.language_id]
    command = syntax.compile if len(syntax.compile) > 0 else syntax.execute
    executable = command[0].format(python=sys.executable)
    resolved_executable = shutil.which(cmd=executable)
    if resolved_executable is None:
        raise click.ClickException(
            message=f"Missing required tool: {executable}"
        )
    for control, path, module_name in programs:
        directory = path.parent
        fields = {
            "python": sys.executable,
            "source": str(object=path),
            "output": str(object=directory / "run.exe"),
            "directory": str(object=directory),
            "module_name": module_name,
            "repository": str(object=Path(__file__).resolve().parents[1]),
        }
        if len(syntax.compile) > 0:
            built = subprocess.run(
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
            if built.returncode != 0:
                raise click.ClickException(
                    message=f"{lang_cls.language_id}/{control}: "
                    + built.stderr
                    + built.stdout
                )
            execution = [arg.format(**fields) for arg in syntax.execute]
        else:
            execution = [
                resolved_executable,
                *(arg.format(**fields) for arg in syntax.execute[1:]),
            ]
        completed = subprocess.run(
            args=execution,
            input=str(object=path) + "\0" if syntax.path_on_stdin else None,
            capture_output=True,
            text=True,
            # Allow cold runtime startup on hosted workers.
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
        if (completed.returncode == 0) is not expected_success:
            raise click.ClickException(
                message=(
                    f"{lang_cls.language_id}/{control}: expected "
                    f"{'success' if expected_success else 'failure'}, "
                    f"got exit {completed.returncode}\n"
                    + completed.stdout
                    + completed.stderr
                )
            )
        click.echo(message=f"{lang_cls.language_id}/{control}: passed")


_LANGUAGES = {
    cls.language_id: cls
    for cls in sorted_languages()
    if cls.supports_stateful_free_call_consumers
}


@click.command()
@click.argument(
    "languages",
    nargs=-1,
    type=click.Choice(choices=tuple(_LANGUAGES)),
    required=True,
)
def main(*, languages: tuple[str, ...]) -> None:
    """Execute receiver controls with each selected native toolchain.

    Missing compilers, runtimes, SDKs and platform support are failures.
    """
    for language in languages:
        with tempfile.TemporaryDirectory(
            suffix="-literalizer-receivers"
        ) as directory:
            _run_controls(lang_cls=_LANGUAGES[language], root=Path(directory))


if __name__ == "__main__":
    main()
