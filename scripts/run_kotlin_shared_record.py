"""Check compatible Kotlin record composition in both orders (#5494).

Only the first document's declarations are emitted. The second literal
consumes those declarations, and runtime checks verify the values. Schemas
with incompatible independently inferred fields are outside this oracle.
"""

import shutil
import sys
from pathlib import Path

from literalizer.languages import Kotlin
from scripts import roundtrip_common, shared_record_common

_PAIRS = (
    (
        "mixed-maps",
        shared_record_common.DECLARING_DOCUMENT,
        """[
  {"name":"row_3","attributes":{"colour":"green","count":4}},
  {"name":"row_4","attributes":{"colour":"white"}}
]""",
        """check(declaringData.map { it.name } == listOf("row_1", "row_2"))
check(dependentData.map { it.name } == listOf("row_3", "row_4"))
check(declaringData[0].attributes ==
    mapOf("colour" to "red", "discounted" to true))
check(declaringData[1].attributes ==
    mapOf("colour" to "blue", "size" to "large"))
check(dependentData[0].attributes ==
    mapOf("colour" to "green", "count" to 4))
check(dependentData[1].attributes == mapOf("colour" to "white"))
""",
    ),
    (
        "nested-list-fields",
        '[{"name":"a","values":[1,2]},{"name":"b","values":[3]}]',
        '[{"name":"c","values":[4]},{"name":"d","values":[5,6]}]',
        """check(declaringData.map { it.name } == listOf("a", "b"))
check(dependentData.map { it.name } == listOf("c", "d"))
check(declaringData.map { it.values.toList() } ==
    listOf(listOf(1, 2), listOf(3)))
check(dependentData.map { it.values.toList() } ==
    listOf(listOf(4), listOf(5, 6)))
""",
    ),
)


def _program(
    *, declaring: str, dependent: str, checks: str, reverse: bool
) -> str:
    """Reuse only the first independently generated set of
    declarations.
    """
    language = Kotlin(
        heterogeneous_strategy=Kotlin.heterogeneous_strategies.RECORD
    )
    first = roundtrip_common.literalize_new_variable(
        language=language,
        json_text=declaring,
        var_name="declaringData",
        pre_indent_level=0,
    )
    second = roundtrip_common.literalize_new_variable(
        language=language,
        json_text=dependent,
        var_name="dependentData",
        pre_indent_level=0,
    )
    if (first.preamble, first.body_preamble) != (
        second.preamble,
        second.body_preamble,
    ):
        msg = (
            "the probe requires compatible independently inferred declarations"
        )
        raise ValueError(msg)
    left, right = (second, first) if reverse else (first, second)
    preamble = "\n".join((*left.preamble, *left.body_preamble))
    return f"{preamble}\n{left.code}\n{right.code}\n{checks}\n"


def main() -> None:
    """Run four existing-host checks with the shared subprocess
    deadline.
    """
    kotlin = shutil.which(cmd="kotlin")
    if kotlin is None:
        msg = "Kotlin is required for shared-record composition"
        raise FileNotFoundError(msg)
    compiler = Path(kotlin).resolve().parent.parent / "lib/kotlin-compiler.jar"
    host = Path(__file__).resolve().parent / "lint-kotlin.kts"
    programs: dict[str, str] = {}
    for name, declaring, dependent, checks in _PAIRS:
        for reverse in (False, True):
            programs[f"{name}-{reverse}.kts"] = _program(
                declaring=declaring,
                dependent=dependent,
                checks=checks,
                reverse=reverse,
            )
    marker = "done.kts"
    try:
        roundtrip_common.execute(
            label="Kotlin shared-record composition (four programs)",
            source_filename=marker,
            program=f'print("""{shared_record_common.OK_DOCUMENT}""")\n',
            steps=[
                roundtrip_common.Step(
                    args=[
                        kotlin,
                        "-classpath",
                        str(object=compiler),
                        str(object=host),
                        *programs,
                        marker,
                    ],
                    failure_label="Kotlin composition compile/value failure",
                )
            ],
            excluded_keys=(),
            expected_json=shared_record_common.OK_DOCUMENT,
            extra_files=programs,
        )
    except SystemExit:
        for name, program in programs.items():
            _ = sys.stderr.write(f"Program {name}:\n{program}\n")
        raise


if __name__ == "__main__":
    main()
