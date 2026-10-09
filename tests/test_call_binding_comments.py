"""Call-result assignments retain trailing comments outside their
terminator.
"""

import pytest

from literalizer import (
    ExistingVariable,
    InputFormat,
    LanguageCls,
    literalize_call,
)
from literalizer.languages import (
    C,
    Cpp,
    CSharp,
    D,
    Dart,
    Haxe,
    Java,
    ObjectiveC,
    SystemVerilog,
    Zig,
)


@pytest.mark.parametrize(
    argnames=("lang_cls", "argument"),
    argvalues=[
        pytest.param(C, "((CVal){.i = 42})", id="C"),
        pytest.param(Cpp, "42", id="Cpp"),
        pytest.param(CSharp, "42", id="CSharp"),
        pytest.param(D, "42", id="D"),
        pytest.param(Haxe, "42", id="Haxe"),
        pytest.param(
            SystemVerilog,
            '_VVal\'{tag: _VVAL_INT, i: 42, r: 0.0, s: ""}',
            id="SystemVerilog",
        ),
        pytest.param(Zig, ".{ .int = 42 }", id="Zig"),
        pytest.param(Dart, "count: 42", id="Dart"),
        pytest.param(Java, "42", id="Java"),
        pytest.param(ObjectiveC, "@42", id="ObjectiveC"),
    ],
)
@pytest.mark.parametrize(
    argnames="suffix",
    argvalues=[
        pytest.param(" // note", id="inline"),
        pytest.param("\n// note", id="comment-line"),
        pytest.param(" // note\n// extra", id="inline-and-comment-line"),
    ],
)
def test_existing_call_binding_comments(
    lang_cls: LanguageCls, argument: str, suffix: str
) -> None:
    """Assignments to externally declared variables keep all final
    comments.
    """
    result = literalize_call(
        source="42",
        input_format=InputFormat.JSON,
        language=lang_cls(),
        target_function="make_widget",
        parameter_names=["count"],
        per_element=False,
        call_transform=lambda context: context.call + suffix,
        variable_form=ExistingVariable(name="my_data"),
        wrap_in_file=False,
    )
    assert result.code == f"my_data = make_widget({argument});{suffix}"
