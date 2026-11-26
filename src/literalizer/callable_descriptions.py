"""Short callable references for prose, independent of sample values."""

from collections.abc import Callable, Mapping

from beartype import beartype

from literalizer import _native_call_data
from literalizer._language import Language
from literalizer._literalize import validate_call_target
from literalizer._native_rendering import validate_native_selector
from literalizer.exceptions import NativeCallError
from literalizer.native_calls import NativeInvocationLanguage


def _text(value: object, /) -> str:
    """Require a nonempty single-line description field."""
    text = _native_call_data.native_recipe_text(value)
    if len(text.strip()) == 0 or "\n" in text or "\r" in text:
        msg = "Callable description fields must be single-line text"
        raise NativeCallError(msg)
    return text


def _flag(value: object, /) -> bool:
    """Require an actual boolean without accepting other schema values."""
    if not isinstance(value, bool):
        msg = "Callable description spacing flags must be booleans"
        raise NativeCallError(msg)
    return value


@beartype
def describe_callable(
    *,
    language: Language,
    description: Mapping[str, object],
    name_renamer: Callable[[str], str] | None = None,
    parameter_renamer: Callable[[str], str] | None = None,
) -> str:
    """Describe a callable without sample data or an implementation.

    Accept a description or a shared recipe with ``default`` and
    ``languages`` mappings.
    ``name`` and ``parameter-names`` are required. Optional fields are
    ``selector``, ``return-annotation``, ``space-before-paren``, and
    ``space-after-paren``. Names and annotations are caller-owned display
    spellings; this is a short reference, not a function declaration.
    Optional naming callbacks transform default names and parameter names.
    Explicit language overrides are already display spellings and take
    precedence over naming callbacks. Selectors and annotations are
    never renamed.
    A selector requires a native-message backend and must have exactly
    one label per parameter. An arrow separates a return annotation from
    the reference.
    """
    shared = "default" in description or "languages" in description
    selected = (
        _native_call_data.select_language_recipe(description, language)
        if shared
        else dict(description)
    )
    _native_call_data.validate_native_fields(
        selected,
        {
            "name",
            "parameter-names",
            "selector",
            "return-annotation",
            "space-before-paren",
            "space-after-paren",
        },
        {"name", "parameter-names"},
    )
    overrides: dict[str, object] = {}
    if shared and language.pygments_name is not None:
        overrides = _native_call_data.native_recipe_mapping(
            _native_call_data.native_recipe_mapping(
                description.get("languages", {})
            ).get(language.pygments_name, {})
        )
    name = _text(selected["name"])
    if name_renamer is not None and "name" not in overrides:
        name = _text(name_renamer(name))
    validate_call_target(
        target_function=name,
        language=language,
        target_function_parts=tuple(name.split(sep=".")),
    )
    parameters = [
        _text(value)
        for value in _native_call_data.native_recipe_list(
            selected["parameter-names"]
        )
    ]
    if parameter_renamer is not None and "parameter-names" not in overrides:
        parameters = [_text(parameter_renamer(value)) for value in parameters]
    if not all(parameter.isidentifier() for parameter in parameters):
        msg = "Callable parameter names must be identifiers"
        raise NativeCallError(msg)
    before = " " if _flag(selected.get("space-before-paren", False)) else ""
    after = " " if _flag(selected.get("space-after-paren", False)) else ""
    if "selector" in selected:
        if (
            not isinstance(language, NativeInvocationLanguage)
            or not language.supports_native_invocations
        ):
            msg = "This language does not support native message selectors"
            raise NativeCallError(msg)
        rendered = _text(selected["selector"])
        _ = validate_native_selector(rendered, len(parameters))
    else:
        rendered = f"{name}{before}({after}{', '.join(parameters)})"
    if "return-annotation" in selected:
        rendered += " -> " + _text(selected["return-annotation"])
    return rendered
