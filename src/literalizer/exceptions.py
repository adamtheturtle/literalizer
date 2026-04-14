"""Exceptions raised by literalizer."""


class ParseError(Exception):
    """Raised when input cannot be parsed into a data structure."""


class JSONParseError(ParseError):
    """Raised when a JSON string cannot be parsed."""


class YAMLParseError(ParseError):
    """Raised when a YAML string cannot be parsed."""


class TOMLParseError(ParseError):
    """Raised when a TOML string cannot be parsed."""


class JSON5ParseError(ParseError):
    """Raised when a JSON5 string cannot be parsed."""


class InvalidDictKeyError(Exception):
    """Raised when a dict key cannot be represented in the target language.

    This includes empty-string keys and keys containing characters that
    the language's label syntax does not support (e.g. control characters
    in Dhall backtick-quoted labels).
    """


class HeterogeneousCoercionError(Exception):
    """Raised when a collection contains heterogeneous scalar types and
    the language would coerce them to strings, but the caller opted to
    receive an error instead.
    """


class NullInCollectionError(Exception):
    """Raised when a collection contains null elements and the chosen
    format does not support them (e.g. Java's ``List.of()``).
    """


class UnsupportedCallStyleError(Exception):
    """Raised when a language does not support function call rendering."""
