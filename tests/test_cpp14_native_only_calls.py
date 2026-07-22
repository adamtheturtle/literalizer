"""C++14 native-only call rendering coverage."""

from literalizer import InputFormat, literalize_call
from literalizer.languages import Cpp


def test_cpp14_call_renders_tuple_eligible_argument_natively() -> None:
    """Tuple-eligible call arguments do not need a variant carrier."""
    result = literalize_call(
        source='[1, "x"]',
        input_format=InputFormat.JSON,
        language=Cpp(language_version=Cpp.version_formats.CPP14),
        target_function="process",
        parameter_names=(),
        per_element=False,
    )

    assert result.code == 'process(std::make_tuple(1, "x"));'
    assert "#include <tuple>" in result.preamble
