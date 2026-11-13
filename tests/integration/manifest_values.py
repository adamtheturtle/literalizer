"""Typed names and containers shared by test manifest definitions."""

from collections.abc import Callable, Mapping
from typing import Annotated, Literal

from beartype import beartype
from pydantic import BeforeValidator, Field, InstanceOf

import literalizer
from literalizer.languages import ALL_LANGUAGES

from .call_templates import CallTransform, call_transform_from_template

type VariableFormName = Literal["new", "existing", "both"]

_CALL_VARIABLE_FORMS_BY_NAME: Mapping[
    str,
    literalizer.NewVariable | literalizer.ExistingVariable,
] = {
    "new": literalizer.NewVariable(name="my_data", modifiers=frozenset()),
    "existing": literalizer.ExistingVariable(name="my_data"),
}

_VARIABLE_FORMS_BY_NAME: Mapping[
    VariableFormName, literalizer.VariableForm
] = {
    "new": _CALL_VARIABLE_FORMS_BY_NAME["new"],
    "existing": _CALL_VARIABLE_FORMS_BY_NAME["existing"],
    "both": literalizer.BothVariableForms(
        name="my_data",
        modifiers=frozenset(),
    ),
}

_CALL_STYLE_TYPES_BY_NAME: Mapping[str, type[literalizer.CallStyle]] = {
    "keyword": literalizer.KeywordCallStyle,
    "positional": literalizer.PositionalCallStyle,
    "object": literalizer.ObjectCallStyle,
    "command": literalizer.CommandCallStyle,
}

_IDENTIFIER_CASES_BY_NAME: Mapping[str, literalizer.IdentifierCase] = {
    member.value: member for member in literalizer.IdentifierCase
}

_INPUT_FORMATS_BY_NAME: Mapping[str, literalizer.InputFormat] = {
    "json": literalizer.InputFormat.JSON,
    "json5": literalizer.InputFormat.JSON5,
    "jsonc": literalizer.InputFormat.JSONC,
    "toml": literalizer.InputFormat.TOML,
    "yaml": literalizer.InputFormat.YAML,
}


@beartype
def _name_resolver[NamedT](
    *, values_by_name: Mapping[str, NamedT]
) -> Callable[[object], object]:
    """Return a callable resolving a manifest name to its value.

    Names are resolved before the strict-mode type check, so a manifest
    spells a resolved argument as a string while the model field holds
    the ``literalizer`` type itself.  Anything that is not a string is
    passed through for that strict check to reject.
    """

    def resolve(value: object, /) -> object:
        """Resolve one manifest name, or list the accepted names."""
        if not isinstance(value, str):
            return value
        if value not in values_by_name:
            accepted = ", ".join(repr(name) for name in sorted(values_by_name))
            msg = f"Input should be {accepted}"
            raise ValueError(msg)
        return values_by_name[value]

    return resolve


# A manifest spells these as TOML arrays, which ``strict=False`` allows
# to be read as the immutable containers the harness holds.  The item
# type is still checked.
type StringTuple = Annotated[tuple[str, ...], Field(strict=False)]
type StringFrozenSet = Annotated[frozenset[str], Field(strict=False)]
_LANGUAGES_BY_NAME = {
    lang_cls.__name__: lang_cls for lang_cls in ALL_LANGUAGES
}
type ManifestLanguage = Annotated[
    literalizer.LanguageCls,
    BeforeValidator(func=_name_resolver(values_by_name=_LANGUAGES_BY_NAME)),
]
type ManifestLanguages = Annotated[
    tuple[ManifestLanguage, ...],
    Field(strict=False),
]
type CallTransformTemplate = Annotated[
    InstanceOf[CallTransform],
    BeforeValidator(func=call_transform_from_template),
]
type CallStyleType = Annotated[
    type[literalizer.CallStyle],
    BeforeValidator(
        func=_name_resolver(values_by_name=_CALL_STYLE_TYPES_BY_NAME)
    ),
]
type CallInputFormat = Annotated[
    literalizer.InputFormat,
    BeforeValidator(
        func=_name_resolver(values_by_name=_INPUT_FORMATS_BY_NAME)
    ),
]
type CallVariableForm = Annotated[
    InstanceOf[literalizer.NewVariable]
    | InstanceOf[literalizer.ExistingVariable],
    BeforeValidator(
        func=_name_resolver(values_by_name=_CALL_VARIABLE_FORMS_BY_NAME)
    ),
]
type RefIdentifierCase = Annotated[
    literalizer.IdentifierCase,
    BeforeValidator(
        func=_name_resolver(values_by_name=_IDENTIFIER_CASES_BY_NAME)
    ),
]


@beartype
def variable_form_for_name(
    *, name: VariableFormName
) -> literalizer.VariableForm:
    """Resolve a declared variable form without rebuilding its
    defaults.
    """
    return _VARIABLE_FORMS_BY_NAME[name]
