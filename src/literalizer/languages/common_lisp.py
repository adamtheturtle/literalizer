"""Common Lisp language specification."""

import dataclasses
import datetime
import enum
import math
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
    passthrough_set_entry,
    variable_declaration_formatter,
    variable_formatter,
)
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._language import (
    ALL_REF_CASES,
    NO_CALL_PARAMETER_LIMIT,
    NO_HETEROGENEOUS_BEHAVIOR,
    BareIntegerWidthStrategies,
    CallParameterShadowing,
    CallStyle,
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
    DeclarationStyleConfig,
    DictFormatConfig,
    FloatSpecialsMixin,
    HeterogeneousBehavior,
    IdentifierCase,
    JsonType,
    LanguageCls,
    ModifierCombination,
    NewVariableNameSyntax,
    OrderedMapFormatConfig,
    PrefixCallStyle,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    VariantMetadata,
    body_preamble_from_scalars,
    default_format_call_variable_assignment,
    default_format_call_variable_declaration,
    default_sequence_binding_declarations,
    default_wrap_calls_with_declarations,
    identity_call_arg,
    identity_call_statement,
    identity_call_target,
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
    reject_empty_dicts,
    wrap_combined_in_file_noop,
    wrap_in_file_noop,
)
from literalizer._types import Value
from literalizer.exceptions import CallArgNotSupportedError


@beartype
def _format_common_lisp_float(
    value: float, /, *, base: Callable[[float], str]
) -> str:
    """Mark finite literals as double-floats independently of reader state."""
    formatted = base(value)
    if not math.isfinite(value):
        return formatted
    if "e" in formatted.lower():
        return formatted.replace("e", "d").replace("E", "d")
    return f"{formatted}d0"


@beartype
def _format_string(value: str) -> str:
    r"""Format a Common Lisp string literal.

    Common Lisp strings only recognize ``\\`` and ``\"`` escapes, so
    actual newlines, carriage returns, tabs, and other control characters
    are embedded literally.
    """
    if "\0" not in value:
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    parts: list[str] = []
    segments = value.split(sep="\0")
    for index, segment in enumerate(iterable=segments):
        if segment:
            parts.append(_format_string(value=segment))
        if index < len(segments) - 1:
            parts.append("(string (code-char 0))")
    return f"(concatenate 'string {' '.join(parts)})"


@beartype
def _format_cons_entry(
    key: str,
    _raw_value: Value,
    formatted_value: str,
) -> str:
    """Format a Common Lisp association-list entry as a ``cons`` pair."""
    return f"(cons {key} {formatted_value})"


@beartype
def _common_lisp_call_stub(
    parts: Sequence[str],
    _params: Sequence[str],
    stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return Common Lisp stub definitions for a call name.

    For dotted names like ``app.client.fetch``, one ``defun`` is
    emitted per prefix so that intermediate identifiers are bound.
    Each stub declares ``&rest args`` and ignores them, so the
    generated function accepts any combination of positional and
    keyword arguments — necessary because the same formatter is used
    both for the call target (invoked with ``:key value`` pairs) and
    for transform wrapper functions (invoked positionally).  Stub
    bodies return ``nil`` for void stubs and ``0`` for value stubs.
    """
    body = "nil" if stub_return is StubReturn.VOID else "0"
    return tuple(
        f"(defun {'.'.join(parts[: i + 1])} "
        f"(&rest args) (declare (ignore args)) {body})"
        for i in range(len(parts))
    )


# Names whose declaration form -- the name between asterisks, as
# ``defparameter`` writes it -- is a symbol in the locked
# ``COMMON-LISP`` package.  Declaring one aborts with a
# ``SYMBOL-PACKAGE-LOCKED-ERROR`` (issue #3947).
_COMMON_LISP_SPECIAL_VARIABLES: frozenset[str] = frozenset(
    {
        "break-on-signals",
        "compile-file-pathname",
        "compile-file-truename",
        "compile-print",
        "compile-verbose",
        "debug-io",
        "debugger-hook",
        "default-pathname-defaults",
        "error-output",
        "features",
        "gensym-counter",
        "load-pathname",
        "load-print",
        "load-truename",
        "load-verbose",
        "macroexpand-hook",
        "modules",
        "package",
        "print-array",
        "print-base",
        "print-case",
        "print-circle",
        "print-escape",
        "print-gensym",
        "print-length",
        "print-level",
        "print-lines",
        "print-miser-width",
        "print-pprint-dispatch",
        "print-pretty",
        "print-radix",
        "print-readably",
        "print-right-margin",
        "query-io",
        "random-state",
        "read-base",
        "read-default-float-format",
        "read-eval",
        "read-suppress",
        "readtable",
        "standard-input",
        "standard-output",
        "terminal-io",
        "trace-output",
    }
)

# The external symbols of the ``COMMON-LISP`` package.  A generated
# file declares its call target with ``defun``, and SBCL locks that
# package, so naming a function after any of these aborts with a
# ``SYMBOL-PACKAGE-LOCKED-ERROR``; the standard itself leaves the
# consequences undefined (CLHS 11.1.2.1.2).  A variable name escapes
# this because it is written between asterisks -- those that do not
# are listed in ``_COMMON_LISP_SPECIAL_VARIABLES`` -- and a call
# parameter escapes it because it is passed as a keyword rather than
# bound (issue #4547).  Only the leading component of a dotted target
# can name one: the stub declares each prefix, and a prefix carrying a
# dot is a fresh symbol.
_COMMON_LISP_PACKAGE_SYMBOLS: frozenset[str] = frozenset(
    {
        "&allow-other-keys",
        "&aux",
        "&body",
        "&environment",
        "&key",
        "&optional",
        "&rest",
        "&whole",
        "*",
        "**",
        "***",
        "*break-on-signals*",
        "*compile-file-pathname*",
        "*compile-file-truename*",
        "*compile-print*",
        "*compile-verbose*",
        "*debug-io*",
        "*debugger-hook*",
        "*default-pathname-defaults*",
        "*error-output*",
        "*features*",
        "*gensym-counter*",
        "*load-pathname*",
        "*load-print*",
        "*load-truename*",
        "*load-verbose*",
        "*macroexpand-hook*",
        "*modules*",
        "*package*",
        "*print-array*",
        "*print-base*",
        "*print-case*",
        "*print-circle*",
        "*print-escape*",
        "*print-gensym*",
        "*print-length*",
        "*print-level*",
        "*print-lines*",
        "*print-miser-width*",
        "*print-pprint-dispatch*",
        "*print-pretty*",
        "*print-radix*",
        "*print-readably*",
        "*print-right-margin*",
        "*query-io*",
        "*random-state*",
        "*read-base*",
        "*read-default-float-format*",
        "*read-eval*",
        "*read-suppress*",
        "*readtable*",
        "*standard-input*",
        "*standard-output*",
        "*terminal-io*",
        "*trace-output*",
        "+",
        "++",
        "+++",
        "-",
        "/",
        "//",
        "///",
        "/=",
        "1+",
        "1-",
        "<",
        "<=",
        "=",
        ">",
        ">=",
        "abort",
        "abs",
        "acons",
        "acos",
        "acosh",
        "add-method",
        "adjoin",
        "adjust-array",
        "adjustable-array-p",
        "allocate-instance",
        "alpha-char-p",
        "alphanumericp",
        "and",
        "append",
        "apply",
        "apropos",
        "apropos-list",
        "aref",
        "arithmetic-error",
        "arithmetic-error-operands",
        "arithmetic-error-operation",
        "array",
        "array-dimension",
        "array-dimension-limit",
        "array-dimensions",
        "array-displacement",
        "array-element-type",
        "array-has-fill-pointer-p",
        "array-in-bounds-p",
        "array-rank",
        "array-rank-limit",
        "array-row-major-index",
        "array-total-size",
        "array-total-size-limit",
        "arrayp",
        "ash",
        "asin",
        "asinh",
        "assert",
        "assoc",
        "assoc-if",
        "assoc-if-not",
        "atan",
        "atanh",
        "atom",
        "base-char",
        "base-string",
        "bignum",
        "bit",
        "bit-and",
        "bit-andc1",
        "bit-andc2",
        "bit-eqv",
        "bit-ior",
        "bit-nand",
        "bit-nor",
        "bit-not",
        "bit-orc1",
        "bit-orc2",
        "bit-vector",
        "bit-vector-p",
        "bit-xor",
        "block",
        "boole",
        "boole-1",
        "boole-2",
        "boole-and",
        "boole-andc1",
        "boole-andc2",
        "boole-c1",
        "boole-c2",
        "boole-clr",
        "boole-eqv",
        "boole-ior",
        "boole-nand",
        "boole-nor",
        "boole-orc1",
        "boole-orc2",
        "boole-set",
        "boole-xor",
        "boolean",
        "both-case-p",
        "boundp",
        "break",
        "broadcast-stream",
        "broadcast-stream-streams",
        "built-in-class",
        "butlast",
        "byte",
        "byte-position",
        "byte-size",
        "caaaar",
        "caaadr",
        "caaar",
        "caadar",
        "caaddr",
        "caadr",
        "caar",
        "cadaar",
        "cadadr",
        "cadar",
        "caddar",
        "cadddr",
        "caddr",
        "cadr",
        "call-arguments-limit",
        "call-method",
        "call-next-method",
        "car",
        "case",
        "catch",
        "ccase",
        "cdaaar",
        "cdaadr",
        "cdaar",
        "cdadar",
        "cdaddr",
        "cdadr",
        "cdar",
        "cddaar",
        "cddadr",
        "cddar",
        "cdddar",
        "cddddr",
        "cdddr",
        "cddr",
        "cdr",
        "ceiling",
        "cell-error",
        "cell-error-name",
        "cerror",
        "change-class",
        "char",
        "char-code",
        "char-code-limit",
        "char-downcase",
        "char-equal",
        "char-greaterp",
        "char-int",
        "char-lessp",
        "char-name",
        "char-not-equal",
        "char-not-greaterp",
        "char-not-lessp",
        "char-upcase",
        "char/=",
        "char<",
        "char<=",
        "char=",
        "char>",
        "char>=",
        "character",
        "characterp",
        "check-type",
        "cis",
        "class",
        "class-name",
        "class-of",
        "clear-input",
        "clear-output",
        "close",
        "clrhash",
        "code-char",
        "coerce",
        "compilation-speed",
        "compile",
        "compile-file",
        "compile-file-pathname",
        "compiled-function",
        "compiled-function-p",
        "compiler-macro",
        "compiler-macro-function",
        "complement",
        "complex",
        "complexp",
        "compute-applicable-methods",
        "compute-restarts",
        "concatenate",
        "concatenated-stream",
        "concatenated-stream-streams",
        "cond",
        "condition",
        "conjugate",
        "cons",
        "consp",
        "constantly",
        "constantp",
        "continue",
        "control-error",
        "copy-alist",
        "copy-list",
        "copy-pprint-dispatch",
        "copy-readtable",
        "copy-seq",
        "copy-structure",
        "copy-symbol",
        "copy-tree",
        "cos",
        "cosh",
        "count",
        "count-if",
        "count-if-not",
        "ctypecase",
        "debug",
        "decf",
        "declaim",
        "declaration",
        "declare",
        "decode-float",
        "decode-universal-time",
        "defclass",
        "defconstant",
        "defgeneric",
        "define-compiler-macro",
        "define-condition",
        "define-method-combination",
        "define-modify-macro",
        "define-setf-expander",
        "define-symbol-macro",
        "defmacro",
        "defmethod",
        "defpackage",
        "defparameter",
        "defsetf",
        "defstruct",
        "deftype",
        "defun",
        "defvar",
        "delete",
        "delete-duplicates",
        "delete-file",
        "delete-if",
        "delete-if-not",
        "delete-package",
        "denominator",
        "deposit-field",
        "describe",
        "describe-object",
        "destructuring-bind",
        "digit-char",
        "digit-char-p",
        "directory",
        "directory-namestring",
        "disassemble",
        "division-by-zero",
        "do",
        "do*",
        "do-all-symbols",
        "do-external-symbols",
        "do-symbols",
        "documentation",
        "dolist",
        "dotimes",
        "double-float",
        "double-float-epsilon",
        "double-float-negative-epsilon",
        "dpb",
        "dribble",
        "dynamic-extent",
        "ecase",
        "echo-stream",
        "echo-stream-input-stream",
        "echo-stream-output-stream",
        "ed",
        "eighth",
        "elt",
        "encode-universal-time",
        "end-of-file",
        "endp",
        "enough-namestring",
        "ensure-directories-exist",
        "ensure-generic-function",
        "eq",
        "eql",
        "equal",
        "equalp",
        "error",
        "etypecase",
        "eval",
        "eval-when",
        "evenp",
        "every",
        "exp",
        "export",
        "expt",
        "extended-char",
        "fboundp",
        "fceiling",
        "fdefinition",
        "ffloor",
        "fifth",
        "file-author",
        "file-error",
        "file-error-pathname",
        "file-length",
        "file-namestring",
        "file-position",
        "file-stream",
        "file-string-length",
        "file-write-date",
        "fill",
        "fill-pointer",
        "find",
        "find-all-symbols",
        "find-class",
        "find-if",
        "find-if-not",
        "find-method",
        "find-package",
        "find-restart",
        "find-symbol",
        "finish-output",
        "first",
        "fixnum",
        "flet",
        "float",
        "float-digits",
        "float-precision",
        "float-radix",
        "float-sign",
        "floating-point-inexact",
        "floating-point-invalid-operation",
        "floating-point-overflow",
        "floating-point-underflow",
        "floatp",
        "floor",
        "fmakunbound",
        "force-output",
        "format",
        "formatter",
        "fourth",
        "fresh-line",
        "fround",
        "ftruncate",
        "ftype",
        "funcall",
        "function",
        "function-keywords",
        "function-lambda-expression",
        "functionp",
        "gcd",
        "generic-function",
        "gensym",
        "gentemp",
        "get",
        "get-decoded-time",
        "get-dispatch-macro-character",
        "get-internal-real-time",
        "get-internal-run-time",
        "get-macro-character",
        "get-output-stream-string",
        "get-properties",
        "get-setf-expansion",
        "get-universal-time",
        "getf",
        "gethash",
        "go",
        "graphic-char-p",
        "handler-bind",
        "handler-case",
        "hash-table",
        "hash-table-count",
        "hash-table-p",
        "hash-table-rehash-size",
        "hash-table-rehash-threshold",
        "hash-table-size",
        "hash-table-test",
        "host-namestring",
        "identity",
        "if",
        "ignorable",
        "ignore",
        "ignore-errors",
        "imagpart",
        "import",
        "in-package",
        "incf",
        "initialize-instance",
        "inline",
        "input-stream-p",
        "inspect",
        "integer",
        "integer-decode-float",
        "integer-length",
        "integerp",
        "interactive-stream-p",
        "intern",
        "internal-time-units-per-second",
        "intersection",
        "invalid-method-error",
        "invoke-debugger",
        "invoke-restart",
        "invoke-restart-interactively",
        "isqrt",
        "keyword",
        "keywordp",
        "labels",
        "lambda",
        "lambda-list-keywords",
        "lambda-parameters-limit",
        "last",
        "lcm",
        "ldb",
        "ldb-test",
        "ldiff",
        "least-negative-double-float",
        "least-negative-long-float",
        "least-negative-normalized-double-float",
        "least-negative-normalized-long-float",
        "least-negative-normalized-short-float",
        "least-negative-normalized-single-float",
        "least-negative-short-float",
        "least-negative-single-float",
        "least-positive-double-float",
        "least-positive-long-float",
        "least-positive-normalized-double-float",
        "least-positive-normalized-long-float",
        "least-positive-normalized-short-float",
        "least-positive-normalized-single-float",
        "least-positive-short-float",
        "least-positive-single-float",
        "length",
        "let",
        "let*",
        "lisp-implementation-type",
        "lisp-implementation-version",
        "list",
        "list*",
        "list-all-packages",
        "list-length",
        "listen",
        "listp",
        "load",
        "load-logical-pathname-translations",
        "load-time-value",
        "locally",
        "log",
        "logand",
        "logandc1",
        "logandc2",
        "logbitp",
        "logcount",
        "logeqv",
        "logical-pathname",
        "logical-pathname-translations",
        "logior",
        "lognand",
        "lognor",
        "lognot",
        "logorc1",
        "logorc2",
        "logtest",
        "logxor",
        "long-float",
        "long-float-epsilon",
        "long-float-negative-epsilon",
        "long-site-name",
        "loop",
        "loop-finish",
        "lower-case-p",
        "machine-instance",
        "machine-type",
        "machine-version",
        "macro-function",
        "macroexpand",
        "macroexpand-1",
        "macrolet",
        "make-array",
        "make-broadcast-stream",
        "make-concatenated-stream",
        "make-condition",
        "make-dispatch-macro-character",
        "make-echo-stream",
        "make-hash-table",
        "make-instance",
        "make-instances-obsolete",
        "make-list",
        "make-load-form",
        "make-load-form-saving-slots",
        "make-method",
        "make-package",
        "make-pathname",
        "make-random-state",
        "make-sequence",
        "make-string",
        "make-string-input-stream",
        "make-string-output-stream",
        "make-symbol",
        "make-synonym-stream",
        "make-two-way-stream",
        "makunbound",
        "map",
        "map-into",
        "mapc",
        "mapcan",
        "mapcar",
        "mapcon",
        "maphash",
        "mapl",
        "maplist",
        "mask-field",
        "max",
        "member",
        "member-if",
        "member-if-not",
        "merge",
        "merge-pathnames",
        "method",
        "method-combination",
        "method-combination-error",
        "method-qualifiers",
        "min",
        "minusp",
        "mismatch",
        "mod",
        "most-negative-double-float",
        "most-negative-fixnum",
        "most-negative-long-float",
        "most-negative-short-float",
        "most-negative-single-float",
        "most-positive-double-float",
        "most-positive-fixnum",
        "most-positive-long-float",
        "most-positive-short-float",
        "most-positive-single-float",
        "muffle-warning",
        "multiple-value-bind",
        "multiple-value-call",
        "multiple-value-list",
        "multiple-value-prog1",
        "multiple-value-setq",
        "multiple-values-limit",
        "name-char",
        "namestring",
        "nbutlast",
        "nconc",
        "next-method-p",
        "nil",
        "nintersection",
        "ninth",
        "no-applicable-method",
        "no-next-method",
        "not",
        "notany",
        "notevery",
        "notinline",
        "nreconc",
        "nreverse",
        "nset-difference",
        "nset-exclusive-or",
        "nstring-capitalize",
        "nstring-downcase",
        "nstring-upcase",
        "nsublis",
        "nsubst",
        "nsubst-if",
        "nsubst-if-not",
        "nsubstitute",
        "nsubstitute-if",
        "nsubstitute-if-not",
        "nth",
        "nth-value",
        "nthcdr",
        "null",
        "number",
        "numberp",
        "numerator",
        "nunion",
        "oddp",
        "open",
        "open-stream-p",
        "optimize",
        "or",
        "otherwise",
        "output-stream-p",
        "package",
        "package-error",
        "package-error-package",
        "package-name",
        "package-nicknames",
        "package-shadowing-symbols",
        "package-use-list",
        "package-used-by-list",
        "packagep",
        "pairlis",
        "parse-error",
        "parse-integer",
        "parse-namestring",
        "pathname",
        "pathname-device",
        "pathname-directory",
        "pathname-host",
        "pathname-match-p",
        "pathname-name",
        "pathname-type",
        "pathname-version",
        "pathnamep",
        "peek-char",
        "phase",
        "pi",
        "plusp",
        "pop",
        "position",
        "position-if",
        "position-if-not",
        "pprint",
        "pprint-dispatch",
        "pprint-exit-if-list-exhausted",
        "pprint-fill",
        "pprint-indent",
        "pprint-linear",
        "pprint-logical-block",
        "pprint-newline",
        "pprint-pop",
        "pprint-tab",
        "pprint-tabular",
        "prin1",
        "prin1-to-string",
        "princ",
        "princ-to-string",
        "print",
        "print-not-readable",
        "print-not-readable-object",
        "print-object",
        "print-unreadable-object",
        "probe-file",
        "proclaim",
        "prog",
        "prog*",
        "prog1",
        "prog2",
        "progn",
        "program-error",
        "progv",
        "provide",
        "psetf",
        "psetq",
        "push",
        "pushnew",
        "quote",
        "random",
        "random-state",
        "random-state-p",
        "rassoc",
        "rassoc-if",
        "rassoc-if-not",
        "ratio",
        "rational",
        "rationalize",
        "rationalp",
        "read",
        "read-byte",
        "read-char",
        "read-char-no-hang",
        "read-delimited-list",
        "read-from-string",
        "read-line",
        "read-preserving-whitespace",
        "read-sequence",
        "reader-error",
        "readtable",
        "readtable-case",
        "readtablep",
        "real",
        "realp",
        "realpart",
        "reduce",
        "reinitialize-instance",
        "rem",
        "remf",
        "remhash",
        "remove",
        "remove-duplicates",
        "remove-if",
        "remove-if-not",
        "remove-method",
        "remprop",
        "rename-file",
        "rename-package",
        "replace",
        "require",
        "rest",
        "restart",
        "restart-bind",
        "restart-case",
        "restart-name",
        "return",
        "return-from",
        "revappend",
        "reverse",
        "room",
        "rotatef",
        "round",
        "row-major-aref",
        "rplaca",
        "rplacd",
        "safety",
        "satisfies",
        "sbit",
        "scale-float",
        "schar",
        "search",
        "second",
        "sequence",
        "serious-condition",
        "set",
        "set-difference",
        "set-dispatch-macro-character",
        "set-exclusive-or",
        "set-macro-character",
        "set-pprint-dispatch",
        "set-syntax-from-char",
        "setf",
        "setq",
        "seventh",
        "shadow",
        "shadowing-import",
        "shared-initialize",
        "shiftf",
        "short-float",
        "short-float-epsilon",
        "short-float-negative-epsilon",
        "short-site-name",
        "signal",
        "signed-byte",
        "signum",
        "simple-array",
        "simple-base-string",
        "simple-bit-vector",
        "simple-bit-vector-p",
        "simple-condition",
        "simple-condition-format-arguments",
        "simple-condition-format-control",
        "simple-error",
        "simple-string",
        "simple-string-p",
        "simple-type-error",
        "simple-vector",
        "simple-vector-p",
        "simple-warning",
        "sin",
        "single-float",
        "single-float-epsilon",
        "single-float-negative-epsilon",
        "sinh",
        "sixth",
        "sleep",
        "slot-boundp",
        "slot-exists-p",
        "slot-makunbound",
        "slot-missing",
        "slot-unbound",
        "slot-value",
        "software-type",
        "software-version",
        "some",
        "sort",
        "space",
        "special",
        "special-operator-p",
        "speed",
        "sqrt",
        "stable-sort",
        "standard",
        "standard-char",
        "standard-char-p",
        "standard-class",
        "standard-generic-function",
        "standard-method",
        "standard-object",
        "step",
        "storage-condition",
        "store-value",
        "stream",
        "stream-element-type",
        "stream-error",
        "stream-error-stream",
        "stream-external-format",
        "streamp",
        "string",
        "string-capitalize",
        "string-downcase",
        "string-equal",
        "string-greaterp",
        "string-left-trim",
        "string-lessp",
        "string-not-equal",
        "string-not-greaterp",
        "string-not-lessp",
        "string-right-trim",
        "string-stream",
        "string-trim",
        "string-upcase",
        "string/=",
        "string<",
        "string<=",
        "string=",
        "string>",
        "string>=",
        "stringp",
        "structure",
        "structure-class",
        "structure-object",
        "style-warning",
        "sublis",
        "subseq",
        "subsetp",
        "subst",
        "subst-if",
        "subst-if-not",
        "substitute",
        "substitute-if",
        "substitute-if-not",
        "subtypep",
        "svref",
        "sxhash",
        "symbol",
        "symbol-function",
        "symbol-macrolet",
        "symbol-name",
        "symbol-package",
        "symbol-plist",
        "symbol-value",
        "symbolp",
        "synonym-stream",
        "synonym-stream-symbol",
        "t",
        "tagbody",
        "tailp",
        "tan",
        "tanh",
        "tenth",
        "terpri",
        "the",
        "third",
        "throw",
        "time",
        "trace",
        "translate-logical-pathname",
        "translate-pathname",
        "tree-equal",
        "truename",
        "truncate",
        "two-way-stream",
        "two-way-stream-input-stream",
        "two-way-stream-output-stream",
        "type",
        "type-error",
        "type-error-datum",
        "type-error-expected-type",
        "type-of",
        "typecase",
        "typep",
        "unbound-slot",
        "unbound-slot-instance",
        "unbound-variable",
        "undefined-function",
        "unexport",
        "unintern",
        "union",
        "unless",
        "unread-char",
        "unsigned-byte",
        "untrace",
        "unuse-package",
        "unwind-protect",
        "update-instance-for-different-class",
        "update-instance-for-redefined-class",
        "upgraded-array-element-type",
        "upgraded-complex-part-type",
        "upper-case-p",
        "use-package",
        "use-value",
        "user-homedir-pathname",
        "values",
        "values-list",
        "variable",
        "vector",
        "vector-pop",
        "vector-push",
        "vector-push-extend",
        "vectorp",
        "warn",
        "warning",
        "when",
        "wild-pathname-p",
        "with-accessors",
        "with-compilation-unit",
        "with-condition-restarts",
        "with-hash-table-iterator",
        "with-input-from-string",
        "with-open-file",
        "with-open-stream",
        "with-output-to-string",
        "with-package-iterator",
        "with-simple-restart",
        "with-slots",
        "with-standard-io-syntax",
        "write",
        "write-byte",
        "write-char",
        "write-line",
        "write-sequence",
        "write-string",
        "write-to-string",
        "y-or-n-p",
        "yes-or-no-p",
        "zerop",
    }
)


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class CommonLisp(metaclass=LanguageCls):
    """Common Lisp language specification."""

    reserved_module_identifiers = frozenset()
    immutable_variable_modifiers = frozenset()
    wrap_in_file_tolerates_pre_indent = True
    module_name_shares_variable_scope = False
    reserved_variable_identifier_pattern = None
    reserved_call_parameter_identifiers = frozenset()
    reserved_call_parameter_identifier_pattern = None
    accepts_type_name_call_target = True
    declares_type_name_call_target = True
    dotted_call_root_shares_entrypoint_namespace = True
    reserved_bare_call_target_identifiers = frozenset()
    contextual_call_target_identifiers = frozenset()
    call_parameter_shadowing = CallParameterShadowing.ALLOWED
    reserved_call_target_keywords_case_sensitive = True
    module_name_must_start_uppercase = False
    max_variable_identifier_length = None
    call_target_name_syntax = None
    supports_multiline_dict_layout = True
    pools_map_integer_width = True

    new_variable_name_syntax: ClassVar[NewVariableNameSyntax] = (
        NewVariableNameSyntax.ASCII_KEBAB
    )

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
    extension = ".lisp"
    pygments_name = "common-lisp"
    stringifies_nested_collections = False
    supports_special_floats = True
    supports_variable_names = True
    supports_no_variable_wrap_in_file = True
    wraps_data_dependent_preamble_in_body = False
    dict_supports_heterogeneous_values = True
    supports_dotted_calls = True
    has_free_function_calls = True
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset()
    reserved_call_target_head_identifiers: ClassVar[frozenset[str]] = (
        _COMMON_LISP_PACKAGE_SYMBOLS
    )
    # The reader folds a symbol name to upper case, so a reserved name
    # is reserved in every spelling.
    reserved_variable_identifiers_case_sensitive: bool = False
    reserved_variable_identifiers: frozenset[str] = (
        _COMMON_LISP_SPECIAL_VARIABLES
    ) | frozenset(
        {
            "nil",
            "t",
        }
    )
    allows_empty_call_parens = True
    supports_dotted_call_stub = True
    call_returns_expression = True
    supports_json_call_result_binding = False
    supports_zero_parameter_calls = True
    max_call_parameters = NO_CALL_PARAMETER_LIMIT
    supports_inline_multiline_dict_args = True
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
    json_type_variant_name_suffix: ClassVar[str | None] = None
    supports_non_ascii_string_literals = True
    supports_multiline_string_literals = False
    supports_empty_sibling_sequence_type_hints = True
    supports_typed_dict_open = False
    language_id: ClassVar[str] = "common_lisp"
    variant_metadata: ClassVar[VariantMetadata] = VariantMetadata(
        round_trip_capabilities=frozenset(),
        modifier_sequence_format_overrides={},
        string_literals_escape_null_byte=True,
        supports_ref_elements_in_tuple_strategy=False,
    )
    supports_record_struct_name_prefix = False
    supports_record_shape_names = False
    record_shape_names_emit_declarations = False
    supports_non_string_dict_keys = True
    checks_raw_control_dict_keys_separately = False

    format_call_arg: ClassVar["staticmethod[[Value, str], str]"] = (
        staticmethod(
            identity_call_arg,
        )
    )
    """Callable that rewrites a formatted direct call argument."""

    class DateFormats(enum.Enum):
        """Date format options for CommonLisp."""

        ISO = DateFormatConfig(
            formatter=format_date_iso, type_produced=str, preamble_lines=()
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for CommonLisp."""

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
        """Sequence type options for Common Lisp."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="(list "),
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            single_element_template=None,
            supports_trailing_comma=False,
            empty_sequence="nil",
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
            narrowed_empty_form=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for Common Lisp."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str="(list "),
            close=")",
            empty_set="nil",
            preamble_lines=(),
            set_opener_template="",
            supports_heterogeneity=True,
            supports_trailing_comma=True,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        SEMICOLON = CommentConfig(
            prefix=";",
            suffix="",
        )
        BLOCK = CommentConfig(
            prefix="#|",
            suffix=" |#",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        DEFPARAMETER = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="(defparameter *{name}* {value})",
            ),
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
        positive_infinity="sb-ext:double-float-positive-infinity",
        negative_infinity="sb-ext:double-float-negative-infinity",
        nan=(
            "#.(sb-int:with-float-traps-masked (:invalid)"
            " (- sb-ext:double-float-positive-infinity"
            " sb-ext:double-float-positive-infinity))"
        ),
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
        """CommonLisp call style options."""

        PREFIX_KEYWORD = PrefixCallStyle(
            arg_separator=" ",
            keyword_prefix=":",
        )

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
        """Empty: this language has no JSON value-type variants."""

    json_types = JsonTypes

    class BoolFormats(enum.Enum):
        """Empty: this language has no alternative boolean formats."""

    bool_formats = BoolFormats

    class VersionFormats(enum.Enum):
        """Version options for Common Lisp."""

        ANSI = enum.auto()

    version_formats = VersionFormats

    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.KEBAB,
    )
    supported_ref_cases: ClassVar[frozenset[IdentifierCase]] = ALL_REF_CASES

    def validate_spec_for_data(self, data: Value) -> None:
        """Reject mappings that collapse onto the empty list."""
        reject_empty_dicts(data=data, language_name=type(self).__name__)

    @cached_property
    def validate_call_arg(self) -> Callable[[Value], None]:
        """Return call-argument validation for this language."""
        return no_validate_call_arg

    @cached_property
    def format_call_statement(self) -> Callable[[str], str]:
        """Return call-statement formatting for this language."""
        return identity_call_statement

    wrap_calls_with_declarations = default_wrap_calls_with_declarations

    @staticmethod
    def wrap_in_file(
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap code in a valid file (no-op)."""
        return wrap_in_file_noop(
            content=content,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    @staticmethod
    def wrap_combined_in_file(
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap declaration and assignment in a valid file (no-op)."""
        return wrap_combined_in_file_noop(
            declaration=declaration,
            assignment=assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    date_format: DateFormats = DateFormats.ISO
    datetime_format: DatetimeFormats = DatetimeFormats.ISO
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.LIST
    set_format: SetFormats = SetFormats.SET
    variable_type_hints: VariableTypeHints = VariableTypeHints.NEVER
    comment_format: CommentFormats = CommentFormats.SEMICOLON
    declaration_style: DeclarationStyles = DeclarationStyles.DEFPARAMETER
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
    call_style: CallStyles = CallStyles.PREFIX_KEYWORD
    statement_terminator_style: StatementTerminatorStyles = (
        StatementTerminatorStyles.SEMICOLON
    )
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    # Keep in sync with the ``LISP`` environment variable of the
    # ``lint-commonlisp`` job in ``.github/workflows/lint.yml``, which pins
    # ``sbcl-bin/2.6.4``. ``ANSI`` is a fixed standard; the pin keeps the
    # installed SBCL build stable across CI runs rather than selecting a
    # language standard.
    language_version: VersionFormats = VersionFormats.ANSI
    indent: str = "    "

    null_literal: ClassVar[str] = "nil"
    true_literal: ClassVar[str] = "t"
    false_literal: ClassVar[str] = "nil"
    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = " "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = True
    supports_scalar_inline_comments: ClassVar[bool] = False
    statement_terminator: ClassVar[str] = ""
    static_preamble: ClassVar[Sequence[str]] = ()
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ()

    @cached_property
    def call_style_config(self) -> CallStyle:
        """Configuration for Common Lisp's call style."""
        return self.call_style.value

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Format a string value as a quoted literal."""
        return _format_string

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Format an int value as a literal."""
        return str

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Format a sequence entry."""
        return passthrough_sequence_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        return passthrough_set_entry

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Format one ordered-map entry."""
        return _format_cons_entry

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
    def format_call_stub(
        self,
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
        """Return stub declarations for a call expression."""
        return _common_lisp_call_stub

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
        """Rewrite a dotted call target into the language's call
        syntax.
        """
        return identity_call_target

    @cached_property
    def format_call_ref_identifier(
        self,
    ) -> Callable[[str, Value | None], str]:
        """Raise for any ``{"$ref": "name"}`` identifier.

        Common Lisp output is not wrapped in a function body, so
        ``*name*`` global-variable references require a surrounding
        ``DEFPARAMETER`` that cannot be injected.
        """

        def _raise_for_common_lisp_ref(
            name: str, _value: Value | None, /
        ) -> str:
            """Raise ``CallArgNotSupportedError`` unconditionally."""
            raise CallArgNotSupportedError(
                language_name="CommonLisp",
                reason=(
                    "Common Lisp output is not wrapped in a function "
                    "body; ``*name*`` references require a surrounding "
                    f"DEFPARAMETER that cannot be injected (got {name!r})"
                ),
            )

        return _raise_for_common_lisp_ref

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
        return self.sequence_format.value

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
            dict_open=fixed_open(open_str="(list "),
            close=")",
            format_entry=_format_cons_entry,
            empty_dict="nil",
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
        return partial(_format_common_lisp_float, base=self.float_format)

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(open_str="(list "),
            close=")",
            preamble_lines=(),
        )

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration."""
        return self.declaration_style.value.formatter

    @cached_property
    def format_variable_assignment(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment to an existing variable."""
        return variable_formatter(template="(setf *{name}* {value})")

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble (Common Lisp needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (Common Lisp needs none)."""
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
