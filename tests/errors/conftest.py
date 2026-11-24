"""Shared target coverage for errors raised before output rendering."""

from typing import TYPE_CHECKING

import pytest
from pydantic import ConfigDict, TypeAdapter

from literalizer import LanguageCls
from literalizer.languages import ALL_LANGUAGES

if TYPE_CHECKING:
    from collections.abc import Mapping


def _language_id(cls: LanguageCls, /) -> str:
    """Return a stable identifier for a target implementation."""
    return cls.language_id


_LANGUAGE_CLASSES: tuple[LanguageCls, ...] = tuple(
    sorted(ALL_LANGUAGES, key=_language_id)
)
_LANGUAGE_CLASS = TypeAdapter[LanguageCls](
    type=LanguageCls, config=ConfigDict(arbitrary_types_allowed=True)
)


@pytest.fixture(
    params=_LANGUAGE_CLASSES,
    ids=_language_id,
)
def language_cls(request: pytest.FixtureRequest) -> LanguageCls:
    """Run shared error contracts against every target implementation."""
    params: Mapping[str, object] = vars(request)
    return _LANGUAGE_CLASS.validate_python(params["param"], strict=True)
