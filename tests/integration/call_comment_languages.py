"""Test languages adopting shared call bindings through the public API.

Built-in adoption belongs to the dependent language pull requests. These
subclasses let the foundation exercise complete files without changing
built-ins.
"""

import dataclasses

import literalizer
from literalizer._language import (
    line_comment_call_variable_assignment,
    line_comment_call_variable_declaration,
)
from literalizer.languages import Cpp, CSharp, Dart, Haxe
from tests.enum_members import enum_member_by_name


class _CommentCpp(Cpp):
    """Use the shared descriptors with Cpp literal syntax."""

    format_call_variable_declaration = line_comment_call_variable_declaration(
        regex_literals=False,
        raw_string_prefixes=(),
        verbatim_strings=False,
        interpolation_syntax=None,
    )
    format_call_variable_assignment = line_comment_call_variable_assignment(
        regex_literals=False,
        raw_string_prefixes=(),
        verbatim_strings=False,
        interpolation_syntax=None,
    )


class _CSharpCommentBindings:
    """Shared descriptors for the CSharp test language."""

    format_call_variable_declaration = line_comment_call_variable_declaration(
        regex_literals=False,
        raw_string_prefixes=(),
        verbatim_strings=True,
        interpolation_syntax=("{", '"'),
    )
    format_call_variable_assignment = line_comment_call_variable_assignment(
        regex_literals=False,
        raw_string_prefixes=(),
        verbatim_strings=True,
        interpolation_syntax=("{", '"'),
    )


class _CommentCSharp(_CSharpCommentBindings, CSharp):
    """Adopt the shared descriptors ahead of CSharp defaults."""


class _DartCommentBindings:
    """Shared descriptors for the Dart test language."""

    format_call_variable_declaration = line_comment_call_variable_declaration(
        regex_literals=False,
        raw_string_prefixes=("r",),
        verbatim_strings=False,
        interpolation_syntax=("${", "\"'"),
    )
    format_call_variable_assignment = line_comment_call_variable_assignment(
        regex_literals=False,
        raw_string_prefixes=("r",),
        verbatim_strings=False,
        interpolation_syntax=("${", "\"'"),
    )


class _CommentDart(_DartCommentBindings, Dart):
    """Adopt the shared descriptors ahead of Dart defaults."""


class _CommentHaxe(Haxe):
    """Use the shared descriptors with Haxe literal syntax."""

    format_call_variable_declaration = line_comment_call_variable_declaration(
        regex_literals=True,
        raw_string_prefixes=(),
        verbatim_strings=False,
        interpolation_syntax=("${", "'"),
    )
    format_call_variable_assignment = line_comment_call_variable_assignment(
        regex_literals=True,
        raw_string_prefixes=(),
        verbatim_strings=False,
        interpolation_syntax=("${", "'"),
    )


_LANGUAGES: dict[str, literalizer.LanguageCls] = {
    "cpp": _CommentCpp,
    "csharp": _CommentCSharp,
    "dart": _CommentDart,
    "haxe": _CommentHaxe,
}


def shared_call_comment_language(
    *, spec: literalizer.Language
) -> literalizer.Language:
    """Adopt the descriptors while preserving the caller's
    configuration.
    """
    language = _LANGUAGES[spec.language_id](
        **{
            field.name: vars(spec)[field.name]
            for field in dataclasses.fields(class_or_instance=spec)
        }
    )
    if spec.language_id == "haxe":
        return dataclasses.replace(
            language,
            declaration_style=enum_member_by_name(
                enum_cls=language.declaration_styles, name="VAR"
            ),
        )
    return language
