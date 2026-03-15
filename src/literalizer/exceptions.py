"""Exceptions raised by literalizer."""


class ParseError(Exception):
    """Raised when input cannot be parsed into a data structure."""


class JSONParseError(ParseError):
    """Raised when a JSON string cannot be parsed."""


class YAMLParseError(ParseError):
    """Raised when a YAML string cannot be parsed."""
