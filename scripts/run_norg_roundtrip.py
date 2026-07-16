"""Norg JSON round-trip check (issue #2667).

Literalize the shared ``roundtrip_input.json`` document to a Norg
``* my_data`` heading whose value rides inside a ``@code json`` ranged
verbatim tag, parse the resulting Norg document with the
``tree-sitter-norg`` grammar, pull the verbatim block's text back out,
and hand it to :func:`roundtrip_common.verify`.

Unlike the executable-language round-trips, there is no language runtime
to invoke: the analogous "back to JSON" step is a Norg parser recovering
the embedded code block.  The :class:`literalizer.languages.Norg`
backend stores the literal as a JSON code block, so once the grammar
hands back the verbatim text the stdlib ``json`` parser re-emits the
parsed value directly -- no hand-rolled serializer is needed.

The parser is the same ``tree-sitter-norg`` grammar the ``Lint Norg``
syntax check uses, loaded here through the ``tree-sitter`` Python
binding.  The compiled shared library is built by the ``Build
tree-sitter-norg parser`` step of the ``lint-npm-installed`` job in
``.github/workflows/lint.yml`` and its path is passed in through the
``LITERALIZER_NORG_PARSER`` environment variable; that job is therefore
where the ``Norg roundtrip`` step lives.  It shares the same input and
comparison logic as the other per-language round-trip helpers.
"""

import ctypes
import json
import os
import sys

from tree_sitter import Language, Parser

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Norg
from scripts import roundtrip_common

_VAR_NAME = "my_data"
_LABEL = "Norg"
_CONTENT_NODE_TYPE = "ranged_verbatim_tag_content"


def _build_document(json_text: str) -> str:
    """Return a Norg document literalized from *json_text*."""
    result = literalize(
        source=json_text,
        input_format=InputFormat.JSON,
        language=Norg(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name=_VAR_NAME, modifiers=frozenset()),
        wrap_in_file=False,
    )
    return f"{result.code}\n"


def _load_norg_language(library_path: str) -> Language:
    """Load the compiled ``tree-sitter-norg`` grammar at *library_path*.

    The ``tree-sitter`` binding expects the grammar pointer wrapped in a
    ``PyCapsule`` named ``tree_sitter.Language``; ``ctypes`` only hands
    back a raw address, so :c:func:`PyCapsule_New` rewraps it before the
    :class:`Language` constructor sees it.
    """
    library = ctypes.cdll.LoadLibrary(name=library_path)
    library.tree_sitter_norg.restype = ctypes.c_void_p
    new_capsule = ctypes.pythonapi.PyCapsule_New
    new_capsule.restype = ctypes.py_object
    new_capsule.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p]
    capsule: object = new_capsule(
        library.tree_sitter_norg(),
        b"tree_sitter.Language",
        None,
    )
    return Language(capsule)


def _extract_code_block(document: str, language: Language) -> str:
    """Return the text of *document*'s single ``@code`` verbatim block."""
    parser = Parser(language=language)
    tree = parser.parse(document.encode(encoding="utf-8"))
    pending = [tree.root_node]
    while pending:
        node = pending.pop()
        if node.type == _CONTENT_NODE_TYPE and node.text is not None:
            return node.text.decode(encoding="utf-8")
        pending.extend(node.children)
    sys.stderr.write(
        f"{_LABEL}: no {_CONTENT_NODE_TYPE} node found\n"
        f"\nProgram:\n{document}\n",
    )
    sys.exit(1)


def main() -> None:
    """Round-trip the shared document through the Norg backend."""
    document = _build_document(json_text=roundtrip_common.read_input())
    language = _load_norg_language(
        library_path=os.environ["LITERALIZER_NORG_PARSER"],
    )
    code_block = _extract_code_block(document=document, language=language)
    parsed: dict[str, object] = json.loads(s=code_block)
    produced_json = json.dumps(obj=parsed)
    roundtrip_common.verify(
        label=_LABEL,
        produced_json=produced_json,
        exclude_keys=(),
    )
    sys.stdout.write(f"{_LABEL} round-trip OK\n")


if __name__ == "__main__":
    main()
