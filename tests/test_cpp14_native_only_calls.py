"""C++14 heterogeneous value-carrier call rendering coverage."""

from literalizer import InputFormat, literalize_call
from literalizer.languages import Cpp


def test_cpp14_call_uses_value_carrier() -> None:
    """Default C++14 calls expose a usable, non-tool-branded carrier."""
    result = literalize_call(
        source='[1, "x"]',
        input_format=InputFormat.JSON,
        language=Cpp(language_version=Cpp.version_formats.CPP14),
        target_function="process",
        parameter_names=(),
        per_element=False,
    )

    assert result.code == 'process(std::vector<Value>{1, "x"});'
    assert "struct Value {" in result.preamble
    preamble = "\n".join(result.preamble)
    assert "template <typename T> bool is() const {" in preamble
    assert "template <typename T> T& get() {" in preamble
