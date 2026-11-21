"""Render a golden case through the public API with its declared
options.
"""

import dataclasses
from collections.abc import Sequence

from beartype import beartype

import literalizer

from .case_inputs import CaseInput
from .golden_renderings import GoldenRendering
from .yaml_warnings import expected_yaml_warnings


@beartype
def literalize_rendering(
    *,
    rendering: GoldenRendering,
    spec: literalizer.Language,
    input_info: CaseInput,
    source_text: str,
    variable_form: literalizer.VariableForm | None,
) -> literalizer.LiteralizeResult:
    """Render one case input under *spec*.

    *variable_form* is passed rather than read off *rendering* so the
    caller can retry without one, which is the only way a language that
    cannot name a variable reaches its golden.
    """
    render = rendering.render
    with expected_yaml_warnings(
        expectation=input_info.expected_reused_anchor_warning,
    ):
        return literalizer.literalize(
            source=source_text,
            input_format=input_info.input_format,
            language=spec,
            pre_indent_level=render.pre_indent_level,
            include_delimiters=True,
            variable_form=variable_form,
            wrap_in_file=rendering.wrap_in_file,
            collection_layout=render.collection_layout,
            record_null_substitutions=render.record_null_substitutions,
        )


@beartype
def compose_rendering(
    *,
    rendering: GoldenRendering,
    spec: literalizer.Language,
    declarations: Sequence[literalizer.LiteralizeResult],
    result: literalizer.LiteralizeResult,
) -> literalizer.LiteralizeResult:
    """Wrap a rendering with its fixture declarations and dependencies."""
    # Keep dependencies before any external type that uses them, even
    # when the rendering requests the same dependencies itself.
    preamble = rendering.extra_preamble
    return literalizer.literalize_call_with_declarations(
        language=spec,
        declarations=declarations,
        call=dataclasses.replace(
            result,
            preamble=preamble + result.preamble,
            data_dependent_preamble=tuple(
                entry
                for entry in result.data_dependent_preamble
                if entry not in preamble
            ),
        ),
    )
