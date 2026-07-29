"""Python union-format configuration errors."""

from collections.abc import Callable

import pytest

from literalizer.exceptions import IncompatibleFormatsError
from literalizer.languages import Python


@pytest.mark.parametrize(
    argnames="language_factory",
    argvalues=[
        pytest.param(
            lambda: Python(
                annotation_evaluation=Python.annotation_evaluations.EAGER,
                union_format=Python.union_formats.PIPE,
                language_version=Python.version_formats.PY38,
            ),
            id="py38",
        ),
        pytest.param(
            lambda: Python(
                annotation_evaluation=Python.annotation_evaluations.EAGER,
                union_format=Python.union_formats.PIPE,
                language_version=Python.version_formats.PY39,
            ),
            id="py39",
        ),
    ],
)
def test_pipe_union_rejects_eager_pre_python_310(
    language_factory: Callable[[], Python],
) -> None:
    """Pipe unions cannot be evaluated by supported target runtimes."""
    with pytest.raises(
        expected_exception=IncompatibleFormatsError,
        match="union_format=PIPE is incompatible with eager annotations",
    ):
        language_factory()
