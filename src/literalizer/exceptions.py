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
