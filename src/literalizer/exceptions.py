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


class PerElementNotListError(Exception):
    """Raised when ``per_element=True`` but the parsed data is not a
    list.
    """


class UnsupportedCallStyleError(Exception):
    """Raised when a language does not support function call rendering."""

    def __init__(self, *, language_name: str) -> None:
        """Create an ``UnsupportedCallStyleError``."""
        super().__init__(
            f"{language_name} does not support function call rendering"
        )
        self.language_name = language_name


class IncompatibleFormatsError(Exception):
    """Raised when a combination of format options produces invalid code.

    For example, Rust ``CONST`` and ``STATIC`` declaration styles
    require constant-expression initializers, but the ``VEC`` sequence
    format produces ``vec![…]`` which is not a constant expression.
    """
