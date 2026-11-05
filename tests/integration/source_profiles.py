"""Capability-driven source profiles retaining each golden request."""

import dataclasses
from collections.abc import Iterator

import pytest

from literalizer import Language, LanguageCls, SourceFormat


@dataclasses.dataclass(frozen=True, kw_only=True)
class SourceProfile:
    """One specification and its independently owned golden name."""

    spec: Language
    name: str


def source_profiles(
    *, spec: Language, lang_cls: LanguageCls, name: str
) -> Iterator[SourceProfile]:
    """Retain legacy output and add the declared canonical profile."""
    yield SourceProfile(spec=spec, name=name)
    if lang_cls.supports_canonical_source_format:
        yield SourceProfile(
            spec=dataclasses.replace(
                spec, source_format=SourceFormat.CANONICAL, indent="  "
            ),
            name=name.replace(
                lang_cls.__name__, f"{lang_cls.__name__}_canonical"
            ),
        )


def source_format_marks(
    *, lang_cls: LanguageCls
) -> tuple[pytest.MarkDecorator, ...]:
    """Select the complete supported corpus without backend-name
    filters.
    """
    if lang_cls.supports_canonical_source_format:
        return (pytest.mark.canonical_source,)
    return ()
