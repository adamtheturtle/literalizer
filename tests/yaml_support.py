"""Typed access to the YAML operations used by test infrastructure."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class YamlParser(Protocol):
    """The load operation exposed by the YAML parser."""

    def load(self, stream: object) -> object:
        """Load one YAML document."""
        raise NotImplementedError


def as_yaml_parser(*, parser: object) -> YamlParser:
    """Validate the third-party loading surface used by tests."""
    if isinstance(parser, YamlParser):
        return parser
    raise NotImplementedError
