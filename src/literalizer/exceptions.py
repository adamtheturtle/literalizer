"""Exceptions raised by literalizer."""


class ParseError(Exception):
    """Raised when input cannot be parsed into a data structure."""


class JSONParseError(ParseError):
    """Raised when a JSON string cannot be parsed."""


class YAMLParseError(ParseError):
    """Raised when a YAML string cannot be parsed."""


class EmptyDictKeyError(Exception):
    """Raised when a dict contains an empty-string key and the language
    specification is configured to reject them.
    """


class HeterogeneousCoercionError(Exception):
    """Raised when a collection contains heterogeneous scalar types and
    the language would coerce them to strings, but the caller opted to
    receive an error instead.
    """
