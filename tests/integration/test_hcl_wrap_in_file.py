"""Targeted ``Hcl.wrap_in_file`` regression tests.

Covers content that the broad ``test_call_golden_file`` parametrization
does not exercise but that ``literalize_call`` can still produce — most
notably HCL strings with backslash-escaped double quotes — to guard
the statement-splitting scanner used by :func:`Hcl.wrap_in_file`.
"""

import literalizer
from literalizer.languages import Hcl


def test_call_string_with_escaped_quote_preserved() -> None:
    r"""A call line with ``\"`` in a string argument is not dropped."""
    spec = Hcl()
    result = literalizer.literalize_call(
        source='---\n- - "a\\"b"\n',
        input_format=literalizer.InputFormat.YAML,
        language=spec,
        target_function="process",
        parameter_names=["v"],
    )
    wrapped = spec.wrap_in_file(
        content=result.bare_code,
        variable_name="",
        body_preamble=(),
    )
    assert wrapped == '_0 = process("a\\"b")'


def test_call_after_decl_with_escaped_quote_preserved() -> None:
    """A ref-decl whose value contains ``"`` keeps the trailing call.

    Reproduces a scanner bug where an odd number of escaped quotes left
    ``in_string`` flipped at end-of-line, causing the splitter to merge
    the next line into the ongoing string and silently drop everything
    that followed.
    """
    spec = Hcl()
    decl = literalizer.literalize(
        source='"a\\"b"',
        input_format=literalizer.InputFormat.JSON,
        language=spec,
        variable_form=literalizer.NewVariable(name="my_str"),
    )
    call = literalizer.literalize_call(
        source="---\n- - {ref: my_str}\n",
        input_format=literalizer.InputFormat.YAML,
        language=spec,
        target_function="process",
        parameter_names=["v"],
    )
    content = decl.bare_code + "\n" + call.bare_code
    wrapped = spec.wrap_in_file(
        content=content,
        variable_name="",
        body_preamble=(),
    )
    assert wrapped == 'my_str = "a\\"b"\n_0 = process(my_str)'
