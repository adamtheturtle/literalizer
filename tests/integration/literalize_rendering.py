"""Render a golden case through the public API with its declared
options.
"""

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
            wrap_in_file=(
                render.wrap_in_file
                and len(rendering.extra_preamble) == 0
                and not rendering.initialize_variable
            ),
            collection_layout=render.collection_layout,
            record_null_substitutions=render.record_null_substitutions,
        )
