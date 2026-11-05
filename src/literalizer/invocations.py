"""Shared invocation recipes delegating to the existing call APIs."""

import dataclasses
from collections.abc import Mapping
from typing import ClassVar

from beartype import beartype

from literalizer._language import Language, PositionalCallStyle
from literalizer._literalize import (
    CallContext,
    ExistingVariable,
    LiteralizeResult,
    NewVariable,
    assemble_call_expression,
    format_rendered_call_arguments,
    validate_call_target,
)
from literalizer._parsing import InputFormat
from literalizer.api import literalize_call
from literalizer.exceptions import NativeCallError
from literalizer.languages import ALL_LANGUAGES
from literalizer.native_call_data import (
    literalize_native_calls,
    native_recipe_list,
    native_recipe_mapping,
    native_recipe_text,
    validate_native_fields,
)


@beartype
@dataclasses.dataclass(frozen=True)
class _ResultCheck:
    """Wrap a result and its paired expected value in a positional
    call.
    """

    target: str
    uses_zipped: ClassVar[bool] = True

    def __call__(self, context: CallContext, /) -> str:
        """Compose already-rendered expressions without source
        templates.
        """
        if context.zipped is None:
            msg = "A result-function requires zipped expected values"
            raise NativeCallError(msg)
        style = PositionalCallStyle(
            arg_separator=", ", parenthesize_each_arg=False
        )
        return assemble_call_expression(
            target_function=self.target,
            args_str=format_rendered_call_arguments(
                formatted=[context.call, context.zipped],
                params=("actual", "expected"),
                style=style,
                allows_empty_call_parens=True,
            ),
            style=style,
        )


@beartype
def _select_recipe(
    recipe: Mapping[str, object], language: Language, /
) -> dict[str, object]:
    """Resolve explicit overrides without inferring names or
    signatures.
    """
    validate_native_fields(recipe, {"default", "languages"}, {"default"})
    default = native_recipe_mapping(recipe["default"])
    overrides = native_recipe_mapping(recipe.get("languages", {}))
    language_id = language.pygments_name
    known = {spec.pygments_name for spec in ALL_LANGUAGES} | {language_id}
    if unknown := set(overrides) - known:
        msg = f"Unknown invocation languages: {sorted(unknown)}"
        raise NativeCallError(msg)
    # Native recipes replace the generic default; generic overrides amend it.
    selected = (
        {}
        if language_id is None
        else native_recipe_mapping(overrides.get(language_id, {}))
    )
    return selected if "native" in selected else {**default, **selected}


@beartype
def literalize_invocations(
    *,
    source: str,
    input_format: InputFormat,
    language: Language,
    invocation: Mapping[str, object],
    per_element: bool = True,
    zip_source: str | None = None,
    zip_input_format: InputFormat | None = None,
    variable_form: NewVariable | ExistingVariable | None = None,
    pre_indent_level: int = 0,
    initial_column: int = 0,
) -> LiteralizeResult:
    """Render a shared recipe or a backwards-compatible bare native recipe.

    A shared recipe has a generic ``default`` and optional ``languages``
    overrides keyed by Pygments ID. Generic overrides amend the default;
    a ``native`` override replaces it with an explicit native signature.
    Generic fields are ``target-function`` or ``constructor-class``,
    ``parameter-names``, and optional ``result-function``. The latter
    calls a caller-owned positional checker with the actual and zipped
    expected values. Existing call-style and data-conversion rules apply.
    """
    selected = (
        _select_recipe(invocation, language)
        if "default" in invocation or "languages" in invocation
        else {"native": dict(invocation)}
    )
    if "native" in selected:
        validate_native_fields(selected, {"native"}, {"native"})
        return literalize_native_calls(
            source=source,
            input_format=input_format,
            language=language,
            invocation=native_recipe_mapping(selected["native"]),
            per_element=per_element,
            zip_source=zip_source,
            zip_input_format=zip_input_format,
            variable_form=variable_form,
            pre_indent_level=pre_indent_level,
            initial_column=initial_column,
        )
    validate_native_fields(
        selected,
        {
            "target-function",
            "constructor-class",
            "parameter-names",
            "result-function",
        },
        {"parameter-names"},
    )
    if ("target-function" in selected) == ("constructor-class" in selected):
        msg = "Specify exactly one target-function or constructor-class"
        raise NativeCallError(msg)
    if pre_indent_level < 0 or initial_column != 0:
        msg = (
            "Generic invocations require nonnegative indent "
            "and zero initial_column"
        )
        raise NativeCallError(msg)
    target = (
        language.format_constructor_target(
            native_recipe_text(selected["constructor-class"])
        )
        if "constructor-class" in selected
        else native_recipe_text(selected["target-function"])
    )
    check = None
    if "result-function" in selected:
        name = native_recipe_text(selected["result-function"])
        parts = tuple(name.split(sep="."))
        validate_call_target(
            language=language,
            target_function=name,
            target_function_parts=parts,
        )
        check = _ResultCheck(target=language.format_call_target(parts))
    result = literalize_call(
        source=source,
        input_format=input_format,
        language=language,
        target_function=target,
        parameter_names=tuple(
            native_recipe_text(value)
            for value in native_recipe_list(selected["parameter-names"])
        ),
        call_transform=check,
        zip_source=zip_source,
        zip_input_format=zip_input_format,
        per_element=per_element,
        variable_form=variable_form,
    )
    prefix = language.indent * pre_indent_level
    return dataclasses.replace(
        result,
        declaration_code="\n".join(
            prefix + line if line else line
            for line in result.declaration_code.split(sep="\n")
        ),
    )
