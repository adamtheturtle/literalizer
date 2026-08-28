"""PHP language specification."""

import dataclasses
import datetime
import enum
import re
from collections.abc import Callable, Sequence
from functools import cached_property
from types import MappingProxyType
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
    dict_entry_with_separator,
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
from literalizer._formatters.format_integers import (
    I64_MAX,
    I64_MIN,
    format_integer_binary,
    format_integer_hex,
    format_integer_octal,
    format_integer_octal_c_style,
    format_integer_underscore,
    make_overflow_fallback_formatter,
    raise_for_unrepresentable_int,
)
from literalizer._formatters.format_strings import (
    format_string_backslash_control,
    format_string_backslash_dollar_nul_hex,
    format_string_backslash_single_minimal,
)
from literalizer._language import (
    NO_CALL_PARAMETER_LIMIT,
    NO_HETEROGENEOUS_BEHAVIOR,
    NON_KEBAB_REF_CASES,
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
    KeywordCallStyle,
    LanguageCls,
    ModifierCombination,
    NewVariableNameSyntax,
    OrderedMapFormatConfig,
    PositionalCallStyle,
    RoundTripCapability,
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
    never_inhibits_consuming_form,
    new_constructor_target,
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
from literalizer.exceptions import UnrepresentableInputError


@beartype
def _format_date_php(value: datetime.date) -> str:
    """Format a date at a deterministic UTC midnight."""
    return f'new DateTime("{value.isoformat()}", new DateTimeZone("UTC"))'


@beartype
def _format_datetime_php(value: datetime.datetime) -> str:
    """Format a datetime without consulting PHP's default time zone."""
    iso = value.isoformat()
    if value.utcoffset() is None:
        return f'new DateTime("{iso}", new DateTimeZone("UTC"))'
    return f'new DateTime("{iso}")'


_UNSAFE_MULTILINE_CONTROL = re.compile(pattern=r"[\x00-\x08\x0b-\x1f]")
_TRAILING_LINE_WHITESPACE = re.compile(pattern=r"[ \t]+(?=\n)")
_INTEGER_STRING_KEY = re.compile(pattern=r"(?:0|-[1-9][0-9]*|[1-9][0-9]*)\Z")


def _reject_numeric_string_keys(data: Value) -> None:
    """Reject mapping keys that PHP arrays coerce from strings to integers."""
    stack = [data]
    while stack:
        value = stack.pop()
        if isinstance(value, dict):
            for key, child in value.items():
                if (
                    isinstance(key, str)
                    and _INTEGER_STRING_KEY.fullmatch(string=key) is not None
                ):
                    msg = (
                        "PHP arrays coerce numeric string mapping key "
                        f"{key!r} "
                        "to an integer key"
                    )
                    raise UnrepresentableInputError(msg)
                stack.append(child)
        elif isinstance(value, list | set):
            stack.extend(value)


def _php_integer_formatter(
    *, base: Callable[[int], str]
) -> Callable[[int], str]:
    """Preserve PHP's signed minimum without a positive overflow
    operand.
    """
    checked = make_overflow_fallback_formatter(
        base=base,
        fallback=raise_for_unrepresentable_int(language_name="PHP"),
        min_value=I64_MIN,
        max_value=I64_MAX,
    )

    def _format(value: int) -> str:
        """Format one PHP integer."""
        return "PHP_INT_MIN" if value == I64_MIN else checked(value)

    return _format


@beartype
def _format_string_multiline_fallback(value: str) -> str:
    r"""Format *value* as an interpolation-safe escaped PHP string."""
    escaped = format_string_backslash_control(
        value=value,
        control_char_fmt=r"\x{:02x}",
        escape_delete=False,
    )
    return escaped.replace("$", r"\$")


@beartype
def _format_string_multiline(value: str) -> str:
    r"""Format *value* as a non-interpolating multiline PHP string."""
    if (
        _UNSAFE_MULTILINE_CONTROL.search(string=value) is not None
        or _TRAILING_LINE_WHITESPACE.search(string=value) is not None
    ):
        return _format_string_multiline_fallback(value=value)
    return format_string_backslash_single_minimal(value=value)


@beartype
def _format_string_single(value: str) -> str:
    """Fall back when a single-quoted source literal is not exact."""
    if "\0" in value or "\r" in value:
        return format_string_backslash_dollar_nul_hex(value=value)
    return format_string_backslash_single_minimal(value=value)


@beartype
def _format_string_double(value: str) -> str:
    r"""Format *value* as an interpolation-safe double-quoted PHP string."""
    return format_string_backslash_dollar_nul_hex(value=value)


@beartype
def _php_format_call_target(parts: Sequence[str], /) -> str:
    """Rewrite a dotted call target into PHP's ``$obj->method`` form."""
    if len(parts) == 1:
        return parts[0]
    return "$" + parts[0] + "".join(f"->{p}" for p in parts[1:])


@beartype
def _php_format_call_ref_identifier(name: str, _value: Value | None, /) -> str:
    """Prepend PHP's ``$`` variable sigil to a call-ref identifier."""
    return f"${name}"


@beartype
def _php_call_stub(
    parts: Sequence[str],
    params: Sequence[str],
    _stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return PHP stub declarations for a call name."""
    param_list = ", ".join(f"${p}" for p in params)
    if len(parts) == 1:
        return (f"function {parts[0]}({param_list}) {{}}",)
    root = parts[0]
    method = parts[-1]
    fields = parts[1:-1]
    if not fields:
        cls = root.capitalize() + "Type"
        return (
            f"class {cls} {{ function {method}({param_list}) {{}} }}",
            f"${root} = new {cls}();",
        )
    lines: list[str] = []
    inner_cls = fields[-1].capitalize() + "Type"
    lines.append(
        f"class {inner_cls} {{ function {method}({param_list}) {{}} }}",
    )
    prev_cls = inner_cls
    for i in range(len(fields) - 2, -1, -1):
        cls = fields[i].capitalize() + "Type"
        field = fields[i + 1]
        lines.append(
            f"class {cls} {{ public ${field}; "
            f"function __construct() {{ "
            f"$this->{field} = new {prev_cls}(); }} }}"
        )
        prev_cls = cls
    root_cls = root.capitalize() + "Type"
    lines.append(
        f"class {root_cls} {{ public ${fields[0]}; "
        f"function __construct() {{ "
        f"$this->{fields[0]} = new {prev_cls}(); }} }}"
    )
    lines.append(f"${root} = new {root_cls}();")
    return tuple(lines)


# The functions PHP always defines: the ``Core`` and ``standard``
# extensions, neither of which can be disabled.  Declaring one of
# these names again is a fatal error, so a generated stub named after
# it does not load (issue #4495).
_PHP_ALWAYS_DEFINED_FUNCTIONS: frozenset[str] = frozenset(
    {
        "abs",
        "acos",
        "acosh",
        "addcslashes",
        "addslashes",
        "array_all",
        "array_any",
        "array_change_key_case",
        "array_chunk",
        "array_column",
        "array_combine",
        "array_count_values",
        "array_diff",
        "array_diff_assoc",
        "array_diff_key",
        "array_diff_uassoc",
        "array_diff_ukey",
        "array_fill",
        "array_fill_keys",
        "array_filter",
        "array_find",
        "array_find_key",
        "array_first",
        "array_flip",
        "array_intersect",
        "array_intersect_assoc",
        "array_intersect_key",
        "array_intersect_uassoc",
        "array_intersect_ukey",
        "array_is_list",
        "array_key_exists",
        "array_key_first",
        "array_key_last",
        "array_keys",
        "array_last",
        "array_map",
        "array_merge",
        "array_merge_recursive",
        "array_multisort",
        "array_pad",
        "array_pop",
        "array_product",
        "array_push",
        "array_rand",
        "array_reduce",
        "array_replace",
        "array_replace_recursive",
        "array_reverse",
        "array_search",
        "array_shift",
        "array_slice",
        "array_splice",
        "array_sum",
        "array_udiff",
        "array_udiff_assoc",
        "array_udiff_uassoc",
        "array_uintersect",
        "array_uintersect_assoc",
        "array_uintersect_uassoc",
        "array_unique",
        "array_unshift",
        "array_values",
        "array_walk",
        "array_walk_recursive",
        "arsort",
        "asin",
        "asinh",
        "asort",
        "assert",
        "assert_options",
        "atan",
        "atan2",
        "atanh",
        "base64_decode",
        "base64_encode",
        "base_convert",
        "basename",
        "bin2hex",
        "bindec",
        "boolval",
        "call_user_func",
        "call_user_func_array",
        "ceil",
        "chdir",
        "checkdnsrr",
        "chgrp",
        "chmod",
        "chop",
        "chown",
        "chr",
        "chunk_split",
        "class_alias",
        "class_exists",
        "clearstatcache",
        "cli_get_process_title",
        "cli_set_process_title",
        "clone",
        "closedir",
        "closelog",
        "compact",
        "connection_aborted",
        "connection_status",
        "constant",
        "convert_uudecode",
        "convert_uuencode",
        "copy",
        "cos",
        "cosh",
        "count",
        "count_chars",
        "crc32",
        "crypt",
        "current",
        "debug_backtrace",
        "debug_print_backtrace",
        "debug_zval_dump",
        "decbin",
        "dechex",
        "decoct",
        "define",
        "defined",
        "deg2rad",
        "die",
        "dir",
        "dirname",
        "disk_free_space",
        "disk_total_space",
        "diskfreespace",
        "dl",
        "dns_check_record",
        "dns_get_mx",
        "dns_get_record",
        "doubleval",
        "end",
        "enum_exists",
        "error_clear_last",
        "error_get_last",
        "error_log",
        "error_reporting",
        "escapeshellarg",
        "escapeshellcmd",
        "exec",
        "exit",
        "exp",
        "explode",
        "expm1",
        "extension_loaded",
        "extract",
        "fclose",
        "fdatasync",
        "fdiv",
        "feof",
        "fflush",
        "fgetc",
        "fgetcsv",
        "fgets",
        "file",
        "file_exists",
        "file_get_contents",
        "file_put_contents",
        "fileatime",
        "filectime",
        "filegroup",
        "fileinode",
        "filemtime",
        "fileowner",
        "fileperms",
        "filesize",
        "filetype",
        "floatval",
        "flock",
        "floor",
        "flush",
        "fmod",
        "fnmatch",
        "fopen",
        "forward_static_call",
        "forward_static_call_array",
        "fpassthru",
        "fpow",
        "fprintf",
        "fputcsv",
        "fputs",
        "fread",
        "fscanf",
        "fseek",
        "fsockopen",
        "fstat",
        "fsync",
        "ftell",
        "ftok",
        "ftruncate",
        "func_get_arg",
        "func_get_args",
        "func_num_args",
        "function_exists",
        "fwrite",
        "gc_collect_cycles",
        "gc_disable",
        "gc_enable",
        "gc_enabled",
        "gc_mem_caches",
        "gc_status",
        "get_browser",
        "get_called_class",
        "get_cfg_var",
        "get_class",
        "get_class_methods",
        "get_class_vars",
        "get_current_user",
        "get_debug_type",
        "get_declared_classes",
        "get_declared_interfaces",
        "get_declared_traits",
        "get_defined_constants",
        "get_defined_functions",
        "get_defined_vars",
        "get_error_handler",
        "get_exception_handler",
        "get_extension_funcs",
        "get_headers",
        "get_html_translation_table",
        "get_include_path",
        "get_included_files",
        "get_loaded_extensions",
        "get_mangled_object_vars",
        "get_meta_tags",
        "get_object_vars",
        "get_parent_class",
        "get_required_files",
        "get_resource_id",
        "get_resource_type",
        "get_resources",
        "getcwd",
        "getenv",
        "gethostbyaddr",
        "gethostbyname",
        "gethostbynamel",
        "gethostname",
        "getimagesize",
        "getimagesizefromstring",
        "getlastmod",
        "getmxrr",
        "getmygid",
        "getmyinode",
        "getmypid",
        "getmyuid",
        "getopt",
        "getprotobyname",
        "getprotobynumber",
        "getrusage",
        "getservbyname",
        "getservbyport",
        "gettimeofday",
        "gettype",
        "glob",
        "header",
        "header_register_callback",
        "header_remove",
        "headers_list",
        "headers_sent",
        "hebrev",
        "hex2bin",
        "hexdec",
        "highlight_file",
        "highlight_string",
        "hrtime",
        "html_entity_decode",
        "htmlentities",
        "htmlspecialchars",
        "htmlspecialchars_decode",
        "http_build_query",
        "http_clear_last_response_headers",
        "http_get_last_response_headers",
        "http_response_code",
        "hypot",
        "ignore_user_abort",
        "image_type_to_extension",
        "image_type_to_mime_type",
        "implode",
        "in_array",
        "inet_ntop",
        "inet_pton",
        "ini_alter",
        "ini_get",
        "ini_get_all",
        "ini_parse_quantity",
        "ini_restore",
        "ini_set",
        "intdiv",
        "interface_exists",
        "intval",
        "ip2long",
        "iptcembed",
        "iptcparse",
        "is_a",
        "is_array",
        "is_bool",
        "is_callable",
        "is_countable",
        "is_dir",
        "is_double",
        "is_executable",
        "is_file",
        "is_finite",
        "is_float",
        "is_infinite",
        "is_int",
        "is_integer",
        "is_iterable",
        "is_link",
        "is_long",
        "is_nan",
        "is_null",
        "is_numeric",
        "is_object",
        "is_readable",
        "is_resource",
        "is_scalar",
        "is_string",
        "is_subclass_of",
        "is_uploaded_file",
        "is_writable",
        "is_writeable",
        "join",
        "key",
        "key_exists",
        "krsort",
        "ksort",
        "lcfirst",
        "lchgrp",
        "lchown",
        "levenshtein",
        "link",
        "linkinfo",
        "localeconv",
        "log",
        "log10",
        "log1p",
        "long2ip",
        "lstat",
        "ltrim",
        "mail",
        "max",
        "md5",
        "md5_file",
        "memory_get_peak_usage",
        "memory_get_usage",
        "memory_reset_peak_usage",
        "metaphone",
        "method_exists",
        "microtime",
        "min",
        "mkdir",
        "move_uploaded_file",
        "natcasesort",
        "natsort",
        "net_get_interfaces",
        "next",
        "nl2br",
        "nl_langinfo",
        "number_format",
        "ob_clean",
        "ob_end_clean",
        "ob_end_flush",
        "ob_flush",
        "ob_get_clean",
        "ob_get_contents",
        "ob_get_flush",
        "ob_get_length",
        "ob_get_level",
        "ob_get_status",
        "ob_implicit_flush",
        "ob_list_handlers",
        "ob_start",
        "octdec",
        "opendir",
        "openlog",
        "ord",
        "output_add_rewrite_var",
        "output_reset_rewrite_vars",
        "pack",
        "parse_ini_file",
        "parse_ini_string",
        "parse_str",
        "parse_url",
        "passthru",
        "password_algos",
        "password_get_info",
        "password_hash",
        "password_needs_rehash",
        "password_verify",
        "pathinfo",
        "pclose",
        "pfsockopen",
        "php_ini_loaded_file",
        "php_ini_scanned_files",
        "php_sapi_name",
        "php_strip_whitespace",
        "php_uname",
        "phpcredits",
        "phpinfo",
        "phpversion",
        "pi",
        "popen",
        "pos",
        "pow",
        "prev",
        "print_r",
        "printf",
        "proc_close",
        "proc_get_status",
        "proc_nice",
        "proc_open",
        "proc_terminate",
        "property_exists",
        "putenv",
        "quoted_printable_decode",
        "quoted_printable_encode",
        "quotemeta",
        "rad2deg",
        "range",
        "rawurldecode",
        "rawurlencode",
        "readdir",
        "readfile",
        "readlink",
        "realpath",
        "realpath_cache_get",
        "realpath_cache_size",
        "register_shutdown_function",
        "register_tick_function",
        "rename",
        "request_parse_body",
        "reset",
        "restore_error_handler",
        "restore_exception_handler",
        "rewind",
        "rewinddir",
        "rmdir",
        "round",
        "rsort",
        "rtrim",
        "scandir",
        "serialize",
        "set_error_handler",
        "set_exception_handler",
        "set_file_buffer",
        "set_include_path",
        "set_time_limit",
        "setcookie",
        "setlocale",
        "setrawcookie",
        "settype",
        "sha1",
        "sha1_file",
        "shell_exec",
        "show_source",
        "shuffle",
        "similar_text",
        "sin",
        "sinh",
        "sizeof",
        "sleep",
        "socket_get_status",
        "socket_set_blocking",
        "socket_set_timeout",
        "sort",
        "soundex",
        "sprintf",
        "sqrt",
        "sscanf",
        "stat",
        "str_contains",
        "str_decrement",
        "str_ends_with",
        "str_getcsv",
        "str_increment",
        "str_ireplace",
        "str_pad",
        "str_repeat",
        "str_replace",
        "str_rot13",
        "str_shuffle",
        "str_split",
        "str_starts_with",
        "str_word_count",
        "strcasecmp",
        "strchr",
        "strcmp",
        "strcoll",
        "strcspn",
        "stream_bucket_append",
        "stream_bucket_make_writeable",
        "stream_bucket_new",
        "stream_bucket_prepend",
        "stream_context_create",
        "stream_context_get_default",
        "stream_context_get_options",
        "stream_context_get_params",
        "stream_context_set_default",
        "stream_context_set_option",
        "stream_context_set_options",
        "stream_context_set_params",
        "stream_copy_to_stream",
        "stream_filter_append",
        "stream_filter_prepend",
        "stream_filter_register",
        "stream_filter_remove",
        "stream_get_contents",
        "stream_get_filters",
        "stream_get_line",
        "stream_get_meta_data",
        "stream_get_transports",
        "stream_get_wrappers",
        "stream_is_local",
        "stream_isatty",
        "stream_register_wrapper",
        "stream_resolve_include_path",
        "stream_select",
        "stream_set_blocking",
        "stream_set_chunk_size",
        "stream_set_read_buffer",
        "stream_set_timeout",
        "stream_set_write_buffer",
        "stream_socket_accept",
        "stream_socket_client",
        "stream_socket_enable_crypto",
        "stream_socket_get_name",
        "stream_socket_pair",
        "stream_socket_recvfrom",
        "stream_socket_sendto",
        "stream_socket_server",
        "stream_socket_shutdown",
        "stream_supports_lock",
        "stream_wrapper_register",
        "stream_wrapper_restore",
        "stream_wrapper_unregister",
        "strip_tags",
        "stripcslashes",
        "stripos",
        "stripslashes",
        "stristr",
        "strlen",
        "strnatcasecmp",
        "strnatcmp",
        "strncasecmp",
        "strncmp",
        "strpbrk",
        "strpos",
        "strptime",
        "strrchr",
        "strrev",
        "strripos",
        "strrpos",
        "strspn",
        "strstr",
        "strtok",
        "strtolower",
        "strtoupper",
        "strtr",
        "strval",
        "substr",
        "substr_compare",
        "substr_count",
        "substr_replace",
        "symlink",
        "sys_get_temp_dir",
        "sys_getloadavg",
        "syslog",
        "system",
        "tan",
        "tanh",
        "tempnam",
        "time_nanosleep",
        "time_sleep_until",
        "tmpfile",
        "touch",
        "trait_exists",
        "trigger_error",
        "trim",
        "uasort",
        "ucfirst",
        "ucwords",
        "uksort",
        "umask",
        "uniqid",
        "unlink",
        "unpack",
        "unregister_tick_function",
        "unserialize",
        "urldecode",
        "urlencode",
        "user_error",
        "usleep",
        "usort",
        "utf8_decode",
        "utf8_encode",
        "var_dump",
        "var_export",
        "version_compare",
        "vfprintf",
        "vprintf",
        "vsprintf",
        "wordwrap",
        "zend_version",
    }
)


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Php(metaclass=LanguageCls):
    """PHP language specification."""

    reserved_module_identifiers: ClassVar[frozenset[str]] = frozenset()
    immutable_variable_modifiers: ClassVar[frozenset[enum.Enum]] = frozenset()
    wrap_in_file_tolerates_pre_indent = True
    module_name_shares_variable_scope = False
    reserved_variable_identifier_pattern = None
    reserved_call_parameter_identifiers: ClassVar[frozenset[str]] = frozenset()
    reserved_call_parameter_identifier_pattern = None
    accepts_type_name_call_target = True
    declares_type_name_call_target = True
    dotted_call_root_shares_entrypoint_namespace = True
    reserved_call_target_head_identifiers: ClassVar[frozenset[str]] = (
        frozenset()
    )
    call_parameter_shadowing = CallParameterShadowing.ALLOWED
    module_name_must_start_uppercase = False
    new_variable_name_syntax = NewVariableNameSyntax.ASCII
    max_variable_identifier_length = None
    call_target_name_syntax = None
    supports_multiline_dict_layout = True
    pools_map_integer_width = True

    format_integer_widened = no_format_integer_widened
    format_integer_beyond_i64 = no_format_integer_beyond_i64
    format_constructor_target: ClassVar["staticmethod[[str], str]"] = (
        staticmethod(new_constructor_target)
    )
    format_call_variable_declaration = default_format_call_variable_declaration
    format_call_variable_assignment = default_format_call_variable_assignment
    sequence_binding_declarations = default_sequence_binding_declarations
    format_call_binding_body_preamble = no_call_binding_body_preamble
    format_call_binding_file_pragmas = no_call_binding_file_pragmas

    leading_preamble = no_leading_preamble
    extension = ".php"
    pygments_name = "php"
    stringifies_nested_collections = False
    supports_special_floats = True
    supports_variable_names = True
    supports_no_variable_wrap_in_file = False
    wraps_data_dependent_preamble_in_body = False
    dict_supports_heterogeneous_values = True
    supports_dotted_calls = True
    has_free_function_calls = True
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset()
    reserved_variable_identifiers_case_sensitive: bool = True
    reserved_call_target_keywords_case_sensitive = False
    contextual_call_target_identifiers: ClassVar[frozenset[str]] = frozenset(
        {"self"}
    )
    reserved_variable_identifiers: frozenset[str] = frozenset(
        {
            "__halt_compiler",
            "abstract",
            "and",
            "array",
            "as",
            "break",
            "callable",
            "case",
            "catch",
            "class",
            "clone",
            "const",
            "continue",
            "declare",
            "default",
            "die",
            "do",
            "echo",
            "else",
            "elseif",
            "empty",
            "enddeclare",
            "endfor",
            "endforeach",
            "endif",
            "endswitch",
            "endwhile",
            "eval",
            "exit",
            "extends",
            "final",
            "finally",
            "fn",
            "for",
            "foreach",
            "function",
            "global",
            "goto",
            "if",
            "implements",
            "include",
            "include_once",
            "instanceof",
            "insteadof",
            "interface",
            "isset",
            "list",
            "match",
            "namespace",
            "new",
            "or",
            "parent",
            "print",
            "private",
            "protected",
            "public",
            "readonly",
            "require",
            "require_once",
            "return",
            "self",
            "static",
            "switch",
            "this",
            "throw",
            "trait",
            "try",
            "unset",
            "use",
            "var",
            "while",
            "xor",
            "yield",
        }
    )
    reserved_bare_call_target_identifiers: ClassVar[frozenset[str]] = (
        _PHP_ALWAYS_DEFINED_FUNCTIONS
    )
    allows_empty_call_parens = True
    supports_dotted_call_stub = False
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
    language_id: ClassVar[str] = "php"
    variant_metadata: ClassVar[VariantMetadata] = VariantMetadata(
        round_trip_capabilities=frozenset(
            {
                RoundTripCapability.I64_BOUNDARIES,
                RoundTripCapability.INTERPOLATION_STRINGS,
                RoundTripCapability.EMBEDDED_NUL,
            }
        ),
        modifier_sequence_format_overrides={},
        string_literals_escape_null_byte=True,
        supports_ref_elements_in_tuple_strategy=False,
    )
    supports_record_struct_name_prefix = False
    supports_record_shape_names = False
    record_shape_names_emit_declarations = False
    supports_non_string_dict_keys = False
    checks_raw_control_dict_keys_separately = False

    format_call_arg: ClassVar["staticmethod[[Value, str], str]"] = (
        staticmethod(
            identity_call_arg,
        )
    )
    """Callable that rewrites a formatted direct call argument."""

    class DateFormats(enum.Enum):
        """Date format options for Php."""

        PHP = DateFormatConfig(
            formatter=_format_date_php,
            preamble_lines=(),
            type_produced=datetime.date,
        )
        ISO = DateFormatConfig(
            formatter=format_date_iso, type_produced=str, preamble_lines=()
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Php."""

        PHP = DatetimeFormatConfig(
            formatter=_format_datetime_php,
            preamble_lines=(),
            type_produced=datetime.datetime,
        )
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
        """Sequence type options for PHP."""

        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="["),
            close="]",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            single_element_template=None,
            supports_trailing_comma=True,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
            narrowed_empty_form=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for PHP."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str="["),
            close="]",
            empty_set=None,
            preamble_lines=(),
            set_opener_template="",
            supports_heterogeneity=True,
            supports_trailing_comma=True,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        DOUBLE_SLASH = CommentConfig(
            prefix="//",
            suffix="",
        )
        BLOCK = CommentConfig(
            prefix="/*",
            suffix=" */",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        ASSIGN = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="${name} = {value};"
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
        positive_infinity="INF",
        negative_infinity="-INF",
        nan="NAN",
    ):
        """Float format options."""

        REPR = enum.member(value=format_float_repr)
        SCIENTIFIC = enum.member(value=format_float_scientific)
        FIXED = enum.member(value=format_float_fixed)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = MappingProxyType(
            mapping={
                "NONE": str,
                "UNDERSCORE": format_integer_underscore,
            }
        )
        HEX = MappingProxyType(
            mapping={
                "NONE": format_integer_hex,
                "UNDERSCORE": format_integer_hex,
            }
        )
        OCTAL = MappingProxyType(
            mapping={
                "NONE": format_integer_octal,
                "UNDERSCORE": format_integer_octal,
            }
        )
        OCTAL_C_STYLE = MappingProxyType(
            mapping={
                "NONE": format_integer_octal_c_style,
                "UNDERSCORE": format_integer_octal_c_style,
            }
        )
        BINARY = MappingProxyType(
            mapping={
                "NONE": format_integer_binary,
                "UNDERSCORE": format_integer_binary,
            }
        )

        def get_formatter(
            self,
            numeric_separator: enum.Enum,
        ) -> Callable[[int], str]:
            """Return the integer formatter for the given separator."""
            formatter: Callable[[int], str] = self.value[
                numeric_separator.name
            ]
            return formatter

    class NumericLiteralSuffixes(enum.Enum):
        """Numeric literal suffix options."""

        NONE = enum.auto()

    class NumericSeparators(enum.Enum):
        """Numeric separator options."""

        NONE = enum.auto()
        UNDERSCORE = enum.auto()

    class NumericStyles(enum.Enum):
        """Numeric literal style options."""

        OVERLOADED = enum.auto()

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = enum.member(value=_format_string_double)
        SINGLE = enum.member(value=_format_string_single)
        MULTILINE = enum.member(value=_format_string_multiline)

        def __call__(self, value: str, /) -> str:
            """Format a string."""
            return self.value(value=value)

    class TrailingCommas(enum.Enum):
        """Trailing comma options."""

        YES = TrailingCommaConfig(multiline_trailing_comma=True)
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
        """Php call style options."""

        KEYWORD = KeywordCallStyle(separator=": ")
        POSITIONAL = PositionalCallStyle(
            arg_separator=", ", parenthesize_each_arg=False
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
        """Version options for PHP."""

        V8_1 = enum.auto()

    version_formats = VersionFormats

    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.SNAKE,
        IdentifierCase.CAMEL,
        IdentifierCase.PASCAL,
        IdentifierCase.UPPER_SNAKE,
    )
    supported_ref_cases: ClassVar[frozenset[IdentifierCase]] = (
        NON_KEBAB_REF_CASES
    )

    @staticmethod
    def validate_spec_for_data(data: Value) -> None:
        """Reject mapping shapes that PHP arrays cannot preserve."""
        reject_empty_dicts(data=data, language_name="PHP")
        _reject_numeric_string_keys(data=data)

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

    date_format: DateFormats = DateFormats.PHP
    datetime_format: DatetimeFormats = DatetimeFormats.PHP
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.ARRAY
    set_format: SetFormats = SetFormats.SET
    variable_type_hints: VariableTypeHints = VariableTypeHints.NEVER
    comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH
    declaration_style: DeclarationStyles = DeclarationStyles.ASSIGN
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
    trailing_comma: TrailingCommas = TrailingCommas.YES
    statement_terminator_style: StatementTerminatorStyles = (
        StatementTerminatorStyles.SEMICOLON
    )
    call_style: CallStyles = CallStyles.KEYWORD
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    # Keep in sync with the ``php-version`` pin passed to
    # ``shivammathur/setup-php`` in the ``Set up PHP`` step of
    # ``.github/workflows/lint.yml``. PHP has no ``--langversion``-style
    # flag, so the pinned interpreter is the only mechanism for pinning
    # the language version; ``V8_1`` maps to ``8.1``.
    language_version: VersionFormats = VersionFormats.V8_1
    indent: str = "    "

    null_literal: ClassVar[str] = "null"
    true_literal: ClassVar[str] = "true"
    false_literal: ClassVar[str] = "false"
    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = True
    supports_scalar_inline_comments: ClassVar[bool] = False
    statement_terminator: ClassVar[str] = ";"
    static_preamble: ClassVar[Sequence[str]] = ("<?php",)
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ()

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Format a sequence entry."""
        return passthrough_sequence_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        return passthrough_set_entry

    @cached_property
    def format_variable_assignment(self) -> Callable[[str, str, Value], str]:
        """Format an assignment to an existing variable."""
        return variable_formatter(template="${name} = {value};")

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
        return _php_call_stub

    @cached_property
    def format_call_target(self) -> Callable[[Sequence[str]], str]:
        """Rewrite a dotted call target into PHP's ``$obj->method``
        form.
        """
        return _php_format_call_target

    @cached_property
    def format_call_ref_identifier(
        self,
    ) -> Callable[[str, Value | None], str]:
        """Prepend PHP's ``$`` sigil so a ``{"$ref": "name"}`` argument
        renders as ``$name`` at the call site.
        """
        return _php_format_call_ref_identifier

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
    def format_call_preamble_stub(
        self,
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
        """Return file-scope stubs for a call expression."""
        return no_call_stub

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
    def _dict_entry(self) -> Callable[[str, Value, str], str]:
        """Shared dict-entry formatter used by dict and ordered-map."""
        return dict_entry_with_separator(
            separator=" => ",
            format_value=passthrough_sequence_entry,
        )

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        return DictFormatConfig(
            dict_open=fixed_open(open_str="["),
            close="]",
            format_entry=self._dict_entry,
            empty_dict=None,
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
    def format_string(self) -> Callable[[str], str]:
        """Callable that formats a string value as a quoted literal."""
        return self.string_format

    @cached_property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        return self.float_format

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal."""
        return _php_integer_formatter(
            base=self.integer_format.get_formatter(
                numeric_separator=self.numeric_separator,
            ),
        )

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(open_str="["),
            close="]",
            preamble_lines=(),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return self._dict_entry

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration."""
        return self.declaration_style.value.formatter

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble (PHP needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (PHP needs none)."""
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

    @cached_property
    def call_style_config(self) -> CallStyle:
        """Configuration for the chosen call style."""
        config: CallStyle = self.call_style.value
        return config
