"""COBOL language specification (GnuCOBOL free-format)."""

import dataclasses
import datetime
import enum
import re
import textwrap
from collections.abc import Callable, Sequence
from functools import cached_property, partial
from typing import ClassVar

from beartype import beartype

from literalizer._formatters.collection_openers import (
    fixed_open,
)
from literalizer._formatters.format_dates import (
    format_date_iso,
    format_datetime_epoch,
    format_datetime_iso,
    format_time_iso,
)
from literalizer._formatters.format_entries import (
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    strip_key_quotes,
)
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_integers import (
    I64_MAX,
    I64_MIN,
    make_overflow_fallback_formatter,
    raise_for_unrepresentable_int,
)
from literalizer._formatters.format_json_value import JsonValue, to_jsonable
from literalizer._formatters.format_strings import (
    reject_nul_string_formatter,
)
from literalizer._language import (
    ALL_REF_CASES,
    NO_CALL_PARAMETER_LIMIT,
    NO_HETEROGENEOUS_BEHAVIOR,
    BareIntegerWidthStrategies,
    CallStyle,
    CommandCallStyle,
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
    DeclarationStyleConfig,
    DictFormatConfig,
    FileSection,
    FloatSpecialsMixin,
    HeterogeneousBehavior,
    IdentifierCase,
    JsonType,
    LanguageCls,
    ModifierCombination,
    NestedMapWideningVariant,
    NewVariableNameSyntax,
    OrderedMapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    VariantMetadata,
    body_preamble_from_scalars,
    decode_file_sections,
    default_format_call_variable_assignment,
    default_format_call_variable_declaration,
    default_sequence_binding_declarations,
    default_wrap_calls_with_declarations,
    encode_file_sections,
    identity_constructor_target,
    never_inhibits_consuming_form,
    no_call_binding_body_preamble,
    no_call_binding_file_pragmas,
    no_call_stub,
    no_data_preamble,
    no_format_integer_beyond_i64,
    no_format_integer_widened,
    no_leading_preamble,
    no_type_hint_preamble,
    no_validate_call_arg,
    no_validate_spec_for_data,
    prepend_body_preamble,
)
from literalizer._types import Value
from literalizer.exceptions import CallArgNotSupportedError

_COBOL_EMPTY_LITERAL = "05 FILLER PIC X(1) VALUE SPACES."


@beartype
def _cobol_narrowed_empty_form(_siblings: Sequence[list[Value]]) -> str:
    """Keep COBOL's structured empty literal beside typed siblings.

    Inheriting a sibling's COMP-5 group opener for the empty slot
    would produce a malformed COBOL record; the language's
    ``PIC X(1) VALUE SPACES`` placeholder is the structurally valid
    empty form here.
    """
    return _COBOL_EMPTY_LITERAL


@beartype
def _format_string_cobol(value: str) -> str:
    """Format a COBOL alphanumeric string literal.

    Control characters (newlines, tabs, carriage returns) are replaced
    with spaces because COBOL string literals cannot span multiple lines
    and have no escape sequences.  Double quotes are escaped by doubling
    them, then the whole string is wrapped in double quotes.

    Example: ``say "hi" loud`` becomes ``"say ""hi"" loud"``.
    """
    cleaned = value
    for char, replacement in {"\n": " ", "\r": " ", "\t": " "}.items():
        cleaned = cleaned.replace(char, replacement)
    escaped = cleaned.replace('"', '""')
    return f'"{escaped}"'


@beartype
def _is_data_entry(s: str) -> bool:
    """Return True if *s* looks like a COBOL DATA DIVISION entry.

    A DATA DIVISION entry starts with two decimal digits followed by a
    space (e.g. ``05 FILLER ...``).
    """
    return bool(re.match(pattern=r"^\d{2} ", string=s))


@beartype
def _pic_from_value(value: str) -> str:
    """Return a COBOL PIC (or storage) clause for a formatted literal.

    Inspects the pre-formatted value string to choose the narrowest
    appropriate clause.
    """
    if value == "SPACES":
        return "PIC X(1)"
    if value in {'"TRUE"', '"FALSE"'}:
        return "PIC X(5)"
    if value.startswith('"') and value.endswith('"'):
        inner = value[1:-1].replace('""', '"')
        return f"PIC X({max(1, len(inner.encode(encoding='utf-8')))})"
    if re.match(pattern=r"^-?\d+$", string=value):
        return "PIC S9(18) COMP-5"
    # Float or other numeric
    return "COMP-2"


@beartype
def _to_cobol_entry(value: str, name: str, level: int) -> str:
    """Wrap a scalar literal in a COBOL DATA DIVISION entry.

    Example: ``"42"`` → ``"05 FILLER PIC S9(18) COMP-5 VALUE 42."``
    """
    picture_clause = _pic_from_value(value=value)
    return f"{level:02d} {name} {picture_clause} VALUE {value}."


@beartype
def _bump_levels(content: str) -> str:
    """Increment every COBOL level number in *content* by 5.

    Only lines whose first non-space token is a two-digit level number
    are modified.
    """

    def _bump(m: re.Match[str]) -> str:
        """Return the matched level-number prefix with its level
        incremented by 5.
        """
        new_level = min(int(m.group(2)) + 5, 49)
        return f"{m.group(1)}{new_level:02d}{m.group(3)}"

    return re.sub(
        pattern=r"^(\s*)(\d{2})(\s)",
        repl=_bump,
        string=content,
        flags=re.MULTILINE,
    )


@beartype
def _format_cobol_sequence_entry(_original: Value, item: str) -> str:
    """Format a sequence item as a COBOL DATA DIVISION entry.

    Scalar values become ``05 FILLER PIC … VALUE …`` items.
    Nested collections are wrapped in a ``05 FILLER.`` group with
    inner level numbers bumped by 5.
    """
    if "\n" in item:
        bumped = _bump_levels(content=item)
        return f"05 FILLER.\n{bumped}"
    if _is_data_entry(s=item.strip()):
        return item.strip()
    return _to_cobol_entry(value=item, name="FILLER", level=5)


@beartype
def _key_to_cobol_name(key_str: str) -> str:
    """Convert a formatted COBOL string literal to a valid COBOL data name.

    Strips outer quotes, converts doubled double-quotes back to single,
    converts the result to upper case, replaces non-alphanumeric characters
    with hyphens, and adds the ``F-`` prefix to avoid clashes with COBOL
    reserved words.  The result is truncated to 28 characters (leaving
    room for the prefix).

    This mapping discards information, so two distinct keys can collapse
    onto the same name (the character rewriting above, or the 28-character
    truncation).  Sibling clashes within a group are resolved afterwards
    by :func:`_disambiguate_data_names`.
    """
    name = strip_key_quotes(key=key_str).replace('""', '"')
    name = name.upper()
    name = re.sub(pattern=r"[^A-Z0-9]", repl="-", string=name)
    name = re.sub(pattern=r"-+", repl="-", string=name).strip("-")
    name = name[:28].strip("-") or "FILLER"
    return f"F-{name}"


# COBOL user-defined words are limited to 30 characters in the COBOL 2002
# dialect this module targets.  ``_key_to_cobol_name`` already truncates a
# single name's body to fit that budget (``F-`` prefix plus 28 characters);
# the collision suffix appended below stays within it too.
_MAX_COBOL_NAME_LENGTH = 30

_DATA_NAME_LINE_RE = re.compile(
    pattern=(
        r"^(?P<indent>\s*)(?P<level>\d{2}) "
        r"(?P<name>[A-Za-z0-9-]+)(?P<rest>.*)$"
    )
)


@dataclasses.dataclass
class _NameScope:
    """Mutable record of the data names already used in one COBOL group.

    ``level`` is the group header's level number; ``used`` holds the
    direct-child names emitted so far so a colliding sibling can be given
    a distinct numeric suffix.
    """

    level: int
    used: set[str]


@beartype
def _unique_cobol_name(base: str, used: set[str]) -> str:
    """Return *base*, or a suffixed variant of it, not present in *used*.

    On collision a ``-2``, ``-3``, ... suffix is appended; the base is
    truncated first when needed so the result stays within
    :data:`_MAX_COBOL_NAME_LENGTH`.  The chosen name is recorded in
    *used*.
    """
    if base not in used:
        used.add(base)
        return base
    counter = 2
    while True:
        suffix = f"-{counter}"
        head = base[: _MAX_COBOL_NAME_LENGTH - len(suffix)].rstrip("-")
        candidate = f"{head}{suffix}"
        if candidate not in used:
            used.add(candidate)
            return candidate
        counter += 1


@beartype
def _disambiguate_data_names(content: str) -> str:
    """Make sibling COBOL data names unique within each group.

    ``_key_to_cobol_name`` can map distinct JSON keys to the same COBOL
    data name (its character rewriting or the 28-character truncation
    collapses them), producing two sibling items with identical names in
    one group -- ambiguous COBOL that GnuCOBOL refuses to compile once
    the name is referenced.  This pass walks the rendered DATA DIVISION
    entries level by level and appends a numeric suffix to any name that
    repeats among the direct children of one group, leaving ``FILLER``
    (the explicit unnamed placeholder, which may legitimately repeat)
    untouched.
    """
    scopes: list[_NameScope] = []
    out_lines: list[str] = []
    for line in content.split(sep="\n"):
        match = _DATA_NAME_LINE_RE.match(string=line)
        if match is None:
            out_lines.append(line)
            continue
        level = int(match["level"])
        while scopes and scopes[-1].level >= level:
            scopes.pop()
        name = match["name"]
        if name == "FILLER" or not scopes:
            new_name = name
        else:
            new_name = _unique_cobol_name(base=name, used=scopes[-1].used)
        scopes.append(_NameScope(level=level, used=set()))
        out_lines.append(
            f"{match['indent']}{match['level']} {new_name}{match['rest']}"
        )
    return "\n".join(out_lines)


@beartype
def _format_cobol_dict_entry(
    key: str,
    _raw_value: Value,
    formatted_value: str,
) -> str:
    """Format a COBOL DATA DIVISION entry for a dict key-value pair.

    The key string is converted to a valid COBOL data name.  Scalar
    values produce elementary items; nested collections produce group
    items with bumped level numbers.
    """
    name = _key_to_cobol_name(key_str=key)
    if "\n" in formatted_value:
        bumped = _bump_levels(content=formatted_value)
        return f"05 {name}.\n{bumped}"
    if _is_data_entry(s=formatted_value.strip()):
        bumped = _bump_levels(content=formatted_value.strip())
        return f"05 {name}.\n{bumped}"
    picture_clause = _pic_from_value(value=formatted_value)
    return f"05 {name} {picture_clause} VALUE {formatted_value}."


@beartype
def _to_cobol_name(python_name: str) -> str:
    """Convert a Python-style identifier to a COBOL data name.

    Converts the name to upper case and replaces underscores with hyphens.
    """
    return python_name.upper().replace("_", "-")


@beartype
def _cobol_call_target(parts: Sequence[str], /) -> str:
    """Return the COBOL CALL literal and USING keyword for a call target.

    Only the innermost name is used: ``app.client.fetch`` produces
    ``"FETCH" USING`` so that the call site emits
    ``CALL "FETCH" USING BY CONTENT ...``.
    """
    return f'"{_to_cobol_name(python_name=parts[-1])}" USING'


@beartype
def _cobol_format_call_arg(_value: Value, formatted: str, /) -> str:
    """Prepend ``BY CONTENT`` to a COBOL CALL argument."""
    return f"BY CONTENT {formatted}"


@beartype
def _cobol_call_statement(call: str, /) -> str:
    """Wrap a COBOL call expression as a complete CALL statement."""
    return f"CALL {call}."


@beartype
def _cobol_call_stub(
    parts: Sequence[str],
    _params: Sequence[str],
    _stub_return: StubReturn,
    _args: Sequence[Value],
    /,
    *,
    indent: str,
) -> tuple[str, ...]:
    """Return a nested COBOL program stub for a call target.

    The stub is a minimal nested program that accepts any arguments
    and stops immediately, acting as a valid placeholder for the
    called subprogram.
    """
    name = _to_cobol_name(python_name=parts[-1])
    stub = "\n".join(
        [
            "IDENTIFICATION DIVISION.",
            f"PROGRAM-ID. {name}.",
            "PROCEDURE DIVISION.",
            f"{indent}STOP RUN.",
            f"END PROGRAM {name}.",
        ]
    )
    return (stub,)


@beartype
def _format_variable_declaration(
    name: str,
    value: str,
    _data: Value,
    _modifiers: frozenset[enum.Enum],
) -> str:
    """Format a COBOL 01-level variable declaration.

    Scalars become an elementary 01-level item; collections become a
    group 01-level item containing 05-level sub-items.
    """
    cobol_name = _to_cobol_name(python_name=name)
    stripped = value.strip("\n")
    scalar = stripped.strip()
    if "\n" in stripped or _is_data_entry(s=scalar):
        return _disambiguate_data_names(
            content=f"01 {cobol_name}.\n{stripped}"
        )
    picture_clause = _pic_from_value(value=scalar)
    return f"01 {cobol_name} {picture_clause} VALUE {scalar}."


@beartype
def _format_variable_assignment(name: str, value: str, _data: Value) -> str:
    """Format a COBOL PROCEDURE DIVISION assignment statement.

    Scalars use a ``MOVE … TO …`` statement; complex group items use
    ``INITIALIZE`` (which resets alphanumeric sub-items to SPACES and
    numeric sub-items to ZEROS).
    """
    cobol_name = _to_cobol_name(python_name=name)
    stripped = value.strip("\n")
    scalar = stripped.strip()
    if "\n" in stripped or _is_data_entry(s=scalar):
        return f"INITIALIZE {cobol_name}."
    return f"MOVE {scalar} TO {cobol_name}."


# Names of the two file regions a ``json_type=CJSON`` payload carries.
# COBOL forces declarations and statements into different divisions, but
# ``format_variable_declaration`` returns a single string, so the two
# halves travel joined as :class:`FileSection` regions (see
# :func:`encode_file_sections`); :meth:`Cobol.wrap_in_file` /
# :meth:`Cobol.wrap_combined_in_file` split them back out, and
# :attr:`~literalizer.LiteralizeResult.sections` exposes them to callers
# composing their own program.
_CJSON_WORKING_STORAGE_SECTION = "WORKING-STORAGE"
_CJSON_PROCEDURE_SECTION = "PROCEDURE"

_CJSON_CALL_ARG_MSG = (
    "COBOL json_type=CJSON builds each value as a multi-statement cJSON "
    "node tree, and COBOL has no inline call-expression form to pass one "
    "as a CALL argument"
)


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class _CobolStringLiteral:
    """A COBOL alphanumeric literal expression and its byte length.

    :attr:`expr` is the text that follows ``VALUE`` (a quoted run, or a
    ``&``-joined mix of quoted runs and ``X"NN"`` hex bytes); :attr:`size`
    is the byte count a ``PIC X(size)`` clause must reserve to hold it.
    """

    expr: str
    size: int


# A byte in this inclusive range is a printable ASCII character that
# can sit inside a quoted COBOL literal run; anything else (control
# bytes, the trailing bytes of a multi-byte UTF-8 character) is spliced
# in as an ``X"NN"`` hex literal instead.
_ASCII_PRINTABLE_MIN = 0x20
_ASCII_PRINTABLE_MAX = 0x7E
# A double quote inside a quoted run is escaped by doubling it.
_ASCII_DOUBLE_QUOTE = 0x22


@beartype
def _cobol_null_terminated_literal(text: str, /) -> _CobolStringLiteral:
    """Return a null-terminated COBOL literal expression for *text*.

    cJSON's ``cJSON_CreateString`` / ``cJSON_AddItemToObject`` take a C
    ``const char *``, so every string and object key must be a
    null-terminated buffer.  COBOL alphanumeric literals have no escape
    sequences and cannot span lines, so non-printable bytes (and the
    trailing ``X"00"`` terminator) are spliced in as ``X"NN"`` hex
    literals joined with ``&``; printable ASCII stays a readable quoted
    run, with an embedded double quote doubled per COBOL's own escaping.
    The string is encoded as UTF-8 so multi-byte characters survive.
    """
    data = text.encode(encoding="utf-8")
    tokens: list[str] = []
    run = ""
    for byte in data:
        if _ASCII_PRINTABLE_MIN <= byte <= _ASCII_PRINTABLE_MAX:
            run += '""' if byte == _ASCII_DOUBLE_QUOTE else chr(byte)
            continue
        if run:
            tokens.append(f'"{run}"')
            run = ""
        tokens.append(f'X"{byte:02X}"')
    if run:
        tokens.append(f'"{run}"')
    tokens.append('X"00"')
    return _CobolStringLiteral(expr=" & ".join(tokens), size=len(data) + 1)


# A child is composed into its parent with ``cJSON_AddItemTo*``, which
# returns a ``cJSON_bool`` (1 on success).  A CALL return that is not
# captured lands in GnuCOBOL's ``RETURN-CODE`` special register, which
# ``STOP RUN`` then propagates as the process exit status, so a
# container build would exit non-zero; capturing the status into a
# throwaway item keeps ``RETURN-CODE`` at zero.  The item is named after
# the build's node *prefix* (``N-STATUS`` / ``M-STATUS``) and declared by
# the build itself, so each build stays self-contained: the combined
# declaration+assignment form gets two distinct items instead of sharing
# (and so duplicating) one declaration.
_CJSON_STATUS_PIC = "PIC S9(9) COMP-5"


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class _CobolCJsonBuild:
    """The two-division build of one cJSON node tree.

    :attr:`ws_lines` are the WORKING-STORAGE entries (one ``USAGE
    POINTER`` per node plus the literal items its constructor reads),
    :attr:`proc_lines` the PROCEDURE DIVISION ``CALL`` statements that
    build and compose the nodes, and :attr:`root` the data name of the
    outermost node.  A build is self-contained: ``ws_lines`` already
    includes its own ``{prefix}-STATUS`` capture item when any
    ``cJSON_AddItemTo*`` CALL needs it.
    """

    ws_lines: tuple[str, ...]
    proc_lines: tuple[str, ...]
    root: str


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class _CobolScalarNode:
    """A leaf cJSON node's optional value item and its create CALL.

    :attr:`value_line` is the WORKING-STORAGE item the constructor reads
    (``None`` for ``cJSON_CreateNull``, which takes no argument);
    :attr:`create_call` is the ``cJSON_Create*`` statement that binds the
    node pointer.
    """

    value_line: str | None
    create_call: str


@beartype
def _cobol_cjson_scalar_node(
    name: str,
    node: JsonValue,
    /,
    *,
    format_integer: Callable[[int], str],
    format_float: Callable[[float], str],
) -> _CobolScalarNode:
    """Return the value item and create CALL for a leaf *node*.

    cJSON has no integer constructor, so a number (``int`` or ``float``)
    is stored in a ``COMP-2`` (C ``double``) item and passed ``BY
    VALUE``; *format_integer* supplies the literal (and raises for a
    value beyond COBOL's widest integer, matching the default record
    mode).  A boolean becomes a 0/1 ``COMP-5`` int and a string a
    null-terminated ``PIC X`` buffer.
    """
    create = (
        'CALL "cJSON_Create{verb}" USING {passing} {name}-V RETURNING {name}.'
    )
    match node:
        case bool():
            return _CobolScalarNode(
                value_line=(
                    f"01 {name}-V PIC S9(9) COMP-5 VALUE {1 if node else 0}."
                ),
                create_call=create.format(
                    verb="Bool", passing="BY VALUE", name=name
                ),
            )
        case int():
            return _CobolScalarNode(
                value_line=(
                    f"01 {name}-V USAGE COMP-2 VALUE {format_integer(node)}."
                ),
                create_call=create.format(
                    verb="Number", passing="BY VALUE", name=name
                ),
            )
        case float():
            return _CobolScalarNode(
                value_line=(
                    f"01 {name}-V USAGE COMP-2 VALUE {format_float(node)}."
                ),
                create_call=create.format(
                    verb="Number", passing="BY VALUE", name=name
                ),
            )
        case str():
            literal = _cobol_null_terminated_literal(node)
            return _CobolScalarNode(
                value_line=(
                    f"01 {name}-V PIC X({literal.size}) VALUE {literal.expr}."
                ),
                create_call=create.format(
                    verb="String", passing="BY REFERENCE", name=name
                ),
            )
        case _:
            return _CobolScalarNode(
                value_line=None,
                create_call=f'CALL "cJSON_CreateNull" RETURNING {name}.',
            )


@beartype
def _cobol_cjson_build(
    jsonable: JsonValue,
    /,
    *,
    prefix: str,
    format_integer: Callable[[int], str],
    format_float: Callable[[float], str],
) -> _CobolCJsonBuild:
    """Walk a JSON-able tree and return its COBOL cJSON build.

    Each node is bound to its own ``{prefix}{n}`` ``USAGE POINTER`` data
    item, created with the matching ``cJSON_Create*`` CALL, and composed
    into its parent with ``cJSON_AddItemToObject`` /
    ``cJSON_AddItemToArray`` in a following statement.  Nodes are numbered
    in pre-order, so the document root is always ``{prefix}0``.  A
    distinct *prefix* keeps the declaration and assignment builds of the
    combined form from defining the same data name twice.

    cJSON has no integer constructor, so a number is stored in a
    ``COMP-2`` (C ``double``) item and passed ``BY VALUE``; *format_integer*
    supplies the literal (and raises for a value beyond COBOL's widest
    integer, matching the default record mode).
    """
    ws_lines: list[str] = []
    proc_lines: list[str] = []
    counter = 0
    status_item = f"{prefix}-STATUS"
    uses_status = False

    @beartype
    def _emit(node: JsonValue, /) -> str:
        """Emit the build entries for *node*; return its data name."""
        nonlocal counter, uses_status
        name = f"{prefix}{counter}"
        counter += 1
        ws_lines.append(f"01 {name} USAGE POINTER.")
        match node:
            case dict():
                proc_lines.append(
                    f'CALL "cJSON_CreateObject" RETURNING {name}.'
                )
                for key, child_value in node.items():
                    child = _emit(child_value)
                    uses_status = True
                    key_literal = _cobol_null_terminated_literal(
                        str(object=key)
                    )
                    ws_lines.append(
                        f"01 {child}-K PIC X({key_literal.size}) "
                        f"VALUE {key_literal.expr}."
                    )
                    proc_lines.append(
                        'CALL "cJSON_AddItemToObject" USING BY VALUE '
                        f"{name} BY REFERENCE {child}-K BY VALUE {child} "
                        f"RETURNING {status_item}."
                    )
            case list():
                proc_lines.append(
                    f'CALL "cJSON_CreateArray" RETURNING {name}.'
                )
                for item in node:
                    child = _emit(item)
                    uses_status = True
                    proc_lines.append(
                        'CALL "cJSON_AddItemToArray" USING BY VALUE '
                        f"{name} BY VALUE {child} "
                        f"RETURNING {status_item}."
                    )
            case _:
                scalar = _cobol_cjson_scalar_node(
                    name,
                    node,
                    format_integer=format_integer,
                    format_float=format_float,
                )
                if scalar.value_line is not None:
                    ws_lines.append(scalar.value_line)
                proc_lines.append(scalar.create_call)
        return name

    root = _emit(jsonable)
    if uses_status:
        ws_lines.append(f"01 {status_item} {_CJSON_STATUS_PIC}.")
    return _CobolCJsonBuild(
        ws_lines=tuple(ws_lines),
        proc_lines=tuple(proc_lines),
        root=root,
    )


@beartype
def _render_cjson_payload(
    *,
    ws_lines: tuple[str, ...],
    proc_lines: tuple[str, ...],
) -> str:
    """Join a cJSON build's two halves as encoded file-section regions."""
    return encode_file_sections(
        (
            FileSection(
                name=_CJSON_WORKING_STORAGE_SECTION,
                content="\n".join(ws_lines),
            ),
            FileSection(
                name=_CJSON_PROCEDURE_SECTION,
                content="\n".join(proc_lines),
            ),
        )
    )


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class _CobolCJsonSections:
    """The WORKING-STORAGE and PROCEDURE halves of a split payload."""

    working_storage: str
    procedure: str


@beartype
def _split_cjson_payload(payload: str, /) -> _CobolCJsonSections:
    """Split a :func:`_render_cjson_payload` string into its regions."""
    by_name = {
        section.name: section.content
        for section in decode_file_sections(payload)
    }
    return _CobolCJsonSections(
        working_storage=by_name[_CJSON_WORKING_STORAGE_SECTION],
        procedure=by_name[_CJSON_PROCEDURE_SECTION],
    )


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Cobol(metaclass=LanguageCls):
    """GnuCOBOL free-format language specification.

    Data is represented as COBOL WORKING-STORAGE SECTION level items:
    scalars become elementary data items with VALUE clauses, and
    sequences / dicts become group items with 05-level sub-items.
    """

    new_variable_name_syntax: ClassVar[NewVariableNameSyntax] = (
        NewVariableNameSyntax.ASCII_KEBAB
    )

    #: :attr:`~literalizer.FileSection.name` of the declarations region a
    #: ``json_type=CJSON`` ``wrap_in_file=False`` result exposes through
    #: :attr:`~literalizer.LiteralizeResult.sections`; its content belongs
    #: in a program's WORKING-STORAGE SECTION.
    CJSON_WORKING_STORAGE_SECTION: ClassVar[str] = (
        _CJSON_WORKING_STORAGE_SECTION
    )
    #: :attr:`~literalizer.FileSection.name` of the statements region a
    #: ``json_type=CJSON`` ``wrap_in_file=False`` result exposes; its
    #: content belongs in a program's PROCEDURE DIVISION.
    CJSON_PROCEDURE_SECTION: ClassVar[str] = _CJSON_PROCEDURE_SECTION

    format_integer_widened = no_format_integer_widened
    format_integer_beyond_i64 = no_format_integer_beyond_i64
    format_constructor_target: ClassVar["staticmethod[[str], str]"] = (
        staticmethod(identity_constructor_target)
    )
    format_call_variable_declaration = default_format_call_variable_declaration
    format_call_variable_assignment = default_format_call_variable_assignment
    sequence_binding_declarations = default_sequence_binding_declarations
    format_call_binding_body_preamble = no_call_binding_body_preamble
    format_call_binding_file_pragmas = no_call_binding_file_pragmas

    leading_preamble = no_leading_preamble
    extension = ".cob"
    pygments_name = "cobol"
    supports_special_floats = True
    supports_variable_names = True
    supports_no_variable_wrap_in_file = False
    dict_supports_heterogeneous_values = True
    supports_dotted_calls = True
    has_free_function_calls = True
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset()
    reserved_variable_identifiers_case_sensitive: bool = False
    reserved_variable_identifiers: frozenset[str] = frozenset(
        {
            "accept",
            "add",
            "alter",
            "call",
            "cancel",
            "close",
            "compute",
            "continue",
            "delete",
            "display",
            "divide",
            "else",
            "end",
            "evaluate",
            "exec",
            "exit",
            "goback",
            "if",
            "initialize",
            "inspect",
            "move",
            "multiply",
            "next",
            "not",
            "open",
            "perform",
            "program",
            "read",
            "return",
            "rewrite",
            "search",
            "set",
            "sort",
            "start",
            "stop",
            "subtract",
            "then",
            "transform",
            "use",
            "when",
            "write",
        }
    )
    allows_empty_call_parens = True
    supports_dotted_call_stub = False
    call_returns_expression = False
    supports_zero_parameter_calls = False
    max_call_parameters = NO_CALL_PARAMETER_LIMIT
    supports_inline_multiline_dict_args = False
    supports_standalone_comments_in_wrapped_calls = True
    supports_multi_param_call_wrapper_stub = True
    supports_dict_literal_as_free_expression = True
    supports_module_name = False
    supports_empty_dict_key = False
    supports_call_style = True
    supports_default_dict_key_type = False
    supports_default_dict_value_type = False
    supports_default_sequence_element_type = False
    supports_default_set_element_type = False
    supports_default_ordered_map_value_type = False
    non_default_kwargs: ClassVar[dict[str, str]] = {}
    declaration_style_sequence_format_overrides: ClassVar[dict[str, str]] = {}
    json_type_variant_name_suffix: ClassVar[str | None] = None
    supports_non_ascii_string_literals = True
    variant_metadata: ClassVar[VariantMetadata] = VariantMetadata(
        string_literals_escape_null_byte=False,
        pre_indent_comment_scalar_variant=False,
        fixture_module_name_template=None,
        fixture_module_name_lowercase=False,
        golden_filename_lowercase=False,
        collection_layout_category="layout",
        record_variants=frozenset(),
        nested_map_widening=NestedMapWideningVariant.NONE,
        modifier_sequence_format_overrides={},
    )
    supports_record_struct_name_prefix = False
    supports_record_shape_names = False
    supports_non_string_dict_keys = False

    class DateFormats(enum.Enum):
        """Date format options for Cobol."""

        ISO = DateFormatConfig(
            formatter=format_date_iso, type_produced=str, preamble_lines=()
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Cobol."""

        ISO = DatetimeFormatConfig(
            formatter=format_datetime_iso,
            type_produced=str,
            preamble_lines=(),
        )

        EPOCH = DatetimeFormatConfig(
            formatter=format_datetime_epoch,
            type_produced=int,
            preamble_lines=(),
        )

        def __call__(self, dt_value: datetime.datetime, /) -> str:
            """Format a datetime."""
            return self.value.formatter(dt_value)

    class BytesFormats(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=format_bytes_hex)
        BASE64 = enum.member(value=format_bytes_base64)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

    class SequenceFormats(enum.Enum):
        """Sequence type options for COBOL."""

        SEQUENCE = SequenceFormatConfig(
            sequence_open=fixed_open(open_str=""),
            close="",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence=_COBOL_EMPTY_LITERAL,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
            narrowed_empty_form=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for COBOL."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str=""),
            close="",
            empty_set=_COBOL_EMPTY_LITERAL,
            preamble_lines=(),
            set_opener_template="",
            supports_heterogeneity=True,
            supports_trailing_comma=True,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        STAR_ANGLE = CommentConfig(
            prefix="*>",
            suffix="",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        TYPED = DeclarationStyleConfig(
            formatter=_format_variable_declaration,
            supports_redefinition=True,
        )

    class DictEntryStyles(enum.Enum):
        """Dict entry style options."""

        DEFAULT = enum.auto()

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DEFAULT = enum.auto()

    class EmptyDictKey(enum.Enum):
        """Empty dict key options."""

        ALLOW = enum.auto()

    class FloatFormats(
        FloatSpecialsMixin,
        enum.Enum,
        positive_infinity="9.99E99",
        negative_infinity="-9.99E99",
        nan="0.0",
    ):
        """Float format options."""

        REPR = enum.member(value=format_float_repr)
        SCIENTIFIC = enum.member(value=format_float_scientific)
        FIXED = enum.member(value=format_float_fixed)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = enum.auto()

    class NumericLiteralSuffixes(enum.Enum):
        """Numeric literal suffix options."""

        NONE = enum.auto()

    class NumericSeparators(enum.Enum):
        """Numeric separator options."""

        NONE = enum.auto()

    class NumericStyles(enum.Enum):
        """Numeric literal style options."""

        OVERLOADED = enum.auto()

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = enum.auto()

    class TrailingCommas(enum.Enum):
        """Trailing comma options."""

        NO = TrailingCommaConfig(multiline_trailing_comma=False)

    date_formats = DateFormats
    datetime_formats = DatetimeFormats
    bytes_formats = BytesFormats
    sequence_formats = SequenceFormats
    set_formats = SetFormats
    comment_formats = CommentFormats

    class VariableTypeHints(enum.Enum):
        """Variable type hint options."""

        NEVER = enum.auto()
        SAFE = enum.auto()

    variable_type_hints_formats = VariableTypeHints
    declaration_styles = DeclarationStyles
    dict_entry_styles = DictEntryStyles
    dict_formats = DictFormats
    empty_dict_keys = EmptyDictKey
    float_formats = FloatFormats
    integer_formats = IntegerFormats
    integer_width_strategies = BareIntegerWidthStrategies
    numeric_literal_suffixes = NumericLiteralSuffixes
    numeric_separators = NumericSeparators
    numeric_styles = NumericStyles
    string_formats = StringFormats
    trailing_commas = TrailingCommas

    class StatementTerminatorStyles(enum.Enum):
        """Statement terminator options."""

        SEMICOLON = enum.auto()

    statement_terminator_styles = StatementTerminatorStyles

    class CallStyles(enum.Enum):
        """Cobol call style options."""

        POSITIONAL = CommandCallStyle(arg_separator=" ")

    call_styles = CallStyles

    class Modifiers(enum.Enum):
        """C++/Java/C#-style declaration modifiers: this language has none."""

    modifiers = Modifiers

    class HeterogeneousStrategies(enum.Enum):
        """Heterogeneous-scalar strategy options — this language only
        supports raising.
        """

        ERROR = NO_HETEROGENEOUS_BEHAVIOR

    heterogeneous_strategies = HeterogeneousStrategies

    class JsonTypes(JsonType):
        """JSON value type options for COBOL."""

        CJSON = "cJSON"
        """The ``cJSON`` library's ``cJSON *`` dynamic JSON value, built
        through GnuCOBOL's C ``CALL`` interface.

        The document is rendered as a tree of ``cJSON_Create*`` CALLs
        composed with ``cJSON_AddItemTo*`` rather than a WORKING-STORAGE
        record, so arbitrary string keys, JSON booleans, real numbers,
        heterogeneous arrays, and the empty string are all faithful.
        """

        @property
        def string_literals_escape_null_byte(self) -> bool:
            """Return whether this JSON type faithfully encodes null
            bytes.
            """
            return self is self.CJSON

    json_types = JsonTypes

    class BoolFormats(enum.Enum):
        """Empty: this language has no alternative boolean formats."""

    bool_formats = BoolFormats

    class VersionFormats(enum.Enum):
        """Version options for COBOL."""

        V2002 = enum.auto()

    version_formats = VersionFormats

    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.UPPER_SNAKE,
    )
    supported_ref_cases: ClassVar[frozenset[IdentifierCase]] = ALL_REF_CASES

    validate_spec_for_data = no_validate_spec_for_data

    @cached_property
    def validate_call_arg(self) -> Callable[[Value], None]:
        """Return call-argument validation for this language."""
        return no_validate_call_arg

    wrap_calls_with_declarations = default_wrap_calls_with_declarations

    _PROGRAM_PREFIX: ClassVar[str] = (
        "IDENTIFICATION DIVISION.\n"
        "PROGRAM-ID. CHECK.\n"
        "DATA DIVISION.\n"
        "WORKING-STORAGE SECTION.\n"
    )
    _PROGRAM_SUFFIX: ClassVar[str] = "PROCEDURE DIVISION.\n    STOP RUN."

    def wrap_in_file(
        self,
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a COBOL variable declaration or call block in a program.

        In variable-declaration mode (*variable_name* is non-empty),
        *content* goes in the DATA DIVISION and *body_preamble* is
        prepended before it.  In call mode (*variable_name* is empty),
        *content* holds PROCEDURE DIVISION statements and *body_preamble*
        holds nested-program stubs that follow ``STOP RUN.``.

        Under ``json_type=CJSON`` *content* is a two-region payload (see
        :func:`_render_cjson_payload`): its WORKING-STORAGE half supplies
        the node pointers and literal items and its PROCEDURE half the
        ``CALL`` statements that build the tree.
        """
        if decode_file_sections(content):
            sections = _split_cjson_payload(content)
            indented = textwrap.indent(
                text=sections.procedure,
                prefix=self.indent,
            )
            return (
                Cobol._PROGRAM_PREFIX
                + f"{sections.working_storage}\n"
                + "PROCEDURE DIVISION.\n"
                + f"{indented}\n"
                + f"{self.indent}STOP RUN."
            )
        if variable_name:
            content = prepend_body_preamble(
                content=content,
                body_preamble=body_preamble,
            )
            return (
                Cobol._PROGRAM_PREFIX + f"{content}\n" + Cobol._PROGRAM_SUFFIX
            )
        indented = textwrap.indent(text=content, prefix=self.indent)
        stubs = "\n".join(body_preamble)
        return (
            Cobol._PROGRAM_PREFIX
            + "PROCEDURE DIVISION.\n"
            + f"{indented}\n"
            + f"{self.indent}STOP RUN.\n"
            + f"{stubs}\n"
            + "END PROGRAM CHECK."
        )

    @staticmethod
    def wrap_combined_in_file(
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap COBOL declaration and assignment in a complete program.

        Under ``json_type=CJSON`` both *declaration* and *assignment* are
        two-region payloads: their WORKING-STORAGE halves merge into one
        DATA DIVISION (the declaration already declares the binding
        pointer; the assignment build only adds its ``M`` nodes) and their
        PROCEDURE halves run one after the other.  The file-section
        markers in *declaration* are the reliable discriminator, so this
        stays a :func:`staticmethod`.
        """
        del variable_name
        if decode_file_sections(declaration):
            decl_sections = _split_cjson_payload(declaration)
            assign_sections = _split_cjson_payload(assignment)
            working_storage = (
                f"{decl_sections.working_storage}\n"
                f"{assign_sections.working_storage}"
            )
            procedure = textwrap.indent(
                text=(
                    f"{decl_sections.procedure}\n{assign_sections.procedure}"
                ),
                prefix="    ",
            )
            return (
                Cobol._PROGRAM_PREFIX
                + f"{working_storage}\n"
                + "PROCEDURE DIVISION.\n"
                + f"{procedure}\n"
                + "    STOP RUN."
            )
        declaration = prepend_body_preamble(
            content=declaration,
            body_preamble=body_preamble,
        )
        return (
            Cobol._PROGRAM_PREFIX
            + f"{declaration}\n"
            + "PROCEDURE DIVISION.\n"
            + f"    {assignment}\n"
            + "    STOP RUN."
        )

    date_format: DateFormats = DateFormats.ISO
    datetime_format: DatetimeFormats = DatetimeFormats.ISO
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.SEQUENCE
    set_format: SetFormats = SetFormats.SET
    variable_type_hints: VariableTypeHints = VariableTypeHints.NEVER
    comment_format: CommentFormats = CommentFormats.STAR_ANGLE
    declaration_style: DeclarationStyles = DeclarationStyles.TYPED
    dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT
    dict_format: DictFormats = DictFormats.DEFAULT
    float_format: FloatFormats = FloatFormats.REPR
    integer_format: IntegerFormats = IntegerFormats.DECIMAL
    integer_width_strategy: BareIntegerWidthStrategies = (
        BareIntegerWidthStrategies.BARE
    )
    numeric_literal_suffix: NumericLiteralSuffixes = (
        NumericLiteralSuffixes.NONE
    )
    numeric_separator: NumericSeparators = NumericSeparators.NONE
    numeric_style: NumericStyles = NumericStyles.OVERLOADED
    string_format: StringFormats = StringFormats.DOUBLE
    trailing_comma: TrailingCommas = TrailingCommas.NO
    statement_terminator_style: StatementTerminatorStyles = (
        StatementTerminatorStyles.SEMICOLON
    )
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    # Keep in sync with the ``GNUCOBOL_VERSION`` pin in the
    # ``lint-cobol`` job of ``.github/workflows/lint.yml``; the pinned
    # GnuCOBOL must support COBOL ``>=`` this ``V2002`` default.
    language_version: VersionFormats = VersionFormats.V2002
    json_type: JsonTypes | None = None
    indent: str = "    "

    null_literal: ClassVar[str] = "SPACES"
    true_literal: ClassVar[str] = '"TRUE"'
    false_literal: ClassVar[str] = '"FALSE"'
    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = "\n"
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = False
    supports_scalar_inline_comments: ClassVar[bool] = False
    statement_terminator: ClassVar[str] = ""
    static_preamble: ClassVar[Sequence[str]] = ()
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ()
    call_style: CallStyles = CallStyles.POSITIONAL

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Format a string value as a quoted literal.

        Plain COBOL string literals have no escape for an embedded null
        byte and a raw null byte terminates the literal, so such values
        are rejected.  Under ``json_type=CJSON`` the value tree is
        discarded and each string is rebuilt as a null-terminated
        ``cJSON`` node (which can splice a null byte as an ``X"00"``
        fragment), so no rejection applies there.
        """
        if self._json_type_active:
            return _format_string_cobol
        return reject_nul_string_formatter(
            _format_string_cobol,
            language_name="COBOL",
        )

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Format an int value as a literal."""
        return make_overflow_fallback_formatter(
            base=str,
            fallback=raise_for_unrepresentable_int(language_name="Cobol"),
            min_value=I64_MIN,
            max_value=I64_MAX,
        )

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Format a sequence entry."""
        return _format_cobol_sequence_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        return _format_cobol_sequence_entry

    @cached_property
    def format_variable_assignment(self) -> Callable[[str, str, Value], str]:
        """Format an assignment to an existing variable.

        Under ``json_type=CJSON`` the value is rebuilt as a fresh
        ``cJSON`` node tree (a distinct ``M`` node prefix keeps the combined
        declaration+assignment form from defining a data name twice) and
        the existing pointer is reset to its root.
        """
        if self._json_type_active:
            format_integer = self.format_integer
            format_float = self.format_float

            @beartype
            def _format_cjson_assign(
                name: str,
                _value: str,
                data: Value,
            ) -> str:
                """Build a cJSON node tree and reset the binding
                pointer.
                """
                build = _cobol_cjson_build(
                    to_jsonable(data=data),
                    prefix="M",
                    format_integer=format_integer,
                    format_float=format_float,
                )
                cobol_name = _to_cobol_name(python_name=name)
                return _render_cjson_payload(
                    ws_lines=build.ws_lines,
                    proc_lines=(
                        *build.proc_lines,
                        f"SET {cobol_name} TO {build.root}.",
                    ),
                )

            return _format_cjson_assign
        return _format_variable_assignment

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Format one ordered-map entry."""
        return _format_cobol_dict_entry

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines."""
        return no_data_preamble

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the heterogeneous-behavior config."""
        return self.heterogeneous_strategy.value

    @cached_property
    def call_data_dependent_preamble(
        self,
    ) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines for call rendering."""
        return self.data_dependent_preamble

    @cached_property
    def type_hint_collection_preamble_lines(
        self,
    ) -> Callable[[frozenset[type]], tuple[str, ...]]:
        """Return preamble lines for empty-collection type hints."""
        return no_type_hint_preamble

    @cached_property
    def call_style_config(self) -> CallStyle:
        """Configuration for the chosen call style."""
        return self.call_style.value

    @cached_property
    def format_call_stub(
        self,
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
        """Return nested-program stub declarations for a call
        expression.
        """
        return partial(_cobol_call_stub, indent=self.indent)

    @cached_property
    def format_call_preamble_stub(
        self,
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
        """Return file-scope stubs for a call expression."""
        return no_call_stub

    @cached_property
    def format_call_target(self) -> Callable[[Sequence[str]], str]:
        """Return the quoted COBOL program name and USING keyword."""
        return _cobol_call_target

    @cached_property
    def format_call_arg(self) -> Callable[[Value, str], str]:
        """Prepend ``BY CONTENT`` to each COBOL CALL argument.

        Under ``json_type=CJSON`` a value is a multi-statement ``cJSON``
        node tree, and COBOL has no inline call-expression form to pass one
        as
        a CALL argument, so call binding is rejected (the case is skipped,
        no golden emitted).
        """
        if self._json_type_active:

            @beartype
            def _reject_cjson_call_arg(
                _value: Value,
                _formatted: str,
                /,
            ) -> str:
                """Reject a cJSON call argument."""
                raise CallArgNotSupportedError(
                    language_name="COBOL",
                    reason=_CJSON_CALL_ARG_MSG,
                )

            return _reject_cjson_call_arg
        return _cobol_format_call_arg

    @cached_property
    def format_call_statement(self) -> Callable[[str], str]:
        """Wrap a call expression as a complete COBOL CALL statement."""
        return _cobol_call_statement

    @cached_property
    def format_call_ref_identifier(
        self,
    ) -> Callable[[str, Value | None], str]:
        """Raise for any ``{"$ref": "name"}`` identifier.

        COBOL DATA DIVISION VALUE clauses only accept literals, not
        identifier references, so refs are not supported.
        """

        def _raise_for_cobol_ref(name: str, _value: Value | None, /) -> str:
            """Raise ``CallArgNotSupportedError`` unconditionally."""
            raise CallArgNotSupportedError(
                language_name="COBOL",
                reason=(
                    "COBOL DATA DIVISION VALUE clauses only accept "
                    f"literals, not identifier references (got {name!r})"
                ),
            )

        return _raise_for_cobol_ref

    @cached_property
    def format_call_arg_ref_identifier(
        self,
    ) -> Callable[[str, Value | None], str]:
        """Rewrite a ``{"$ref": "name"}`` identifier in a call-argument
        context.

        Delegates to :attr:`format_call_ref_identifier`.  Override this to
        allow call-argument ``$ref`` values that would otherwise be rejected.
        """
        return self.format_call_ref_identifier

    @cached_property
    def format_call_arg_ref_identifier_consumable(
        self,
    ) -> Callable[[str, Value | None], str]:
        """Format a ``$ref`` the caller authorized as consumable.

        Delegates to :attr:`format_call_arg_ref_identifier`.  Override
        this to opt into a consuming form (e.g. C++ ``std::move``).
        """
        return self.format_call_arg_ref_identifier

    @cached_property
    def consumable_ref_value_inhibits_consuming_form(
        self,
    ) -> Callable[[Value], bool]:
        """Predicate deciding whether a ref's underlying value type
        inhibits the consume form.

        Delegates to :data:`never_inhibits_consuming_form`.  Languages
        whose consume operator rejects certain value types (notably
        the Mojo ``^`` on register-trivial scalars) override this.
        """
        return never_inhibits_consuming_form

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        return dataclasses.replace(
            self.sequence_format.value,
            narrowed_empty_form=_cobol_narrowed_empty_form,
        )

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        return self.set_format.value

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        return self.sequence_format.value.sequence_open

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        return DictFormatConfig(
            dict_open=fixed_open(open_str=""),
            close="",
            format_entry=_format_cobol_dict_entry,
            empty_dict=_COBOL_EMPTY_LITERAL,
            preamble_lines=(),
            narrowed_open=None,
            supports_trailing_comma=True,
            narrowed_empty_form=None,
        )

    @cached_property
    def trailing_comma_config(self) -> TrailingCommaConfig:
        """Configuration for trailing-comma behavior."""
        return self.trailing_comma.value

    @cached_property
    def format_bytes(self) -> Callable[[bytes], str]:
        """Callable that formats a bytes value as a string literal."""
        return self.bytes_format

    @cached_property
    def format_date(self) -> Callable[[datetime.date], str]:
        """Callable that formats a date as a string literal."""
        return self.date_format

    @cached_property
    def format_datetime(self) -> Callable[[datetime.datetime], str]:
        """Callable that formats a datetime as a string literal."""
        return self.datetime_format

    @cached_property
    def format_time(self) -> Callable[[datetime.time], str]:
        """Callable that formats a time as a string literal."""
        return format_time_iso

    @cached_property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        return self.float_format

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(open_str=""),
            close="",
            preamble_lines=(),
        )

    @cached_property
    def _json_type_active(self) -> bool:
        """Return whether COBOL renders via cJSON's ``cJSON *`` type."""
        return self.json_type is not None

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration.

        Under ``json_type=CJSON`` the rendered record value is discarded:
        the data is built as a ``cJSON`` node tree (WORKING-STORAGE
        pointer items plus PROCEDURE DIVISION ``CALL`` statements, joined
        as encoded file-section regions) and the binding pointer is set to
        its root.
        """
        if self._json_type_active:
            format_integer = self.format_integer
            format_float = self.format_float

            @beartype
            def _format_cjson_decl(
                name: str,
                _value: str,
                data: Value,
                _modifiers: frozenset[enum.Enum],
            ) -> str:
                """Build a cJSON node tree and declare its root
                pointer.
                """
                build = _cobol_cjson_build(
                    to_jsonable(data=data),
                    prefix="N",
                    format_integer=format_integer,
                    format_float=format_float,
                )
                cobol_name = _to_cobol_name(python_name=name)
                return _render_cjson_payload(
                    ws_lines=(
                        *build.ws_lines,
                        f"01 {cobol_name} USAGE POINTER.",
                    ),
                    proc_lines=(
                        *build.proc_lines,
                        f"SET {cobol_name} TO {build.root}.",
                    ),
                )

            return _format_cjson_decl
        return self.declaration_style.value.formatter

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble (COBOL needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (COBOL needs none)."""
        return {}

    @cached_property
    def compute_body_preamble(
        self,
    ) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
        """Compute body-preamble lines from the scalar map."""
        return body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
            format_lines=tuple,
        )
