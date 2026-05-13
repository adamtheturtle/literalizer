"""Resolve YAML and TOML comments and apply them to literalized output."""

import dataclasses
from io import StringIO
from typing import Any

from beartype import beartype
from ruamel.yaml.comments import CommentedMap, CommentedSeq, CommentedSet
from tomlkit.toml_document import TOMLDocument

from literalizer._comments import (
    CollectionComments,
    ElementComments,
    apply_collection_comments,
    extract_toml_comments,
    extract_yaml_comments,
    literalize_yaml_scalar,
)
from literalizer._language import Language
from literalizer._parsing import get_yaml


@beartype
def _filter_null_dict_comments(
    *,
    data: dict[Any, Any],
    collection_comments: CollectionComments,
) -> CollectionComments:
    """Remove comments for null-valued dict entries.

    When a language skips null dict values, the associated comments
    are redistributed to the next non-null entry.
    """
    pending: list[str] = []
    filtered_elements_list: list[ElementComments] = []
    for key, ec in zip(data, collection_comments.elements, strict=True):
        if data[key] is None:
            pending.extend(ec.before)
            if ec.inline:
                pending.append(ec.inline)
        else:
            new_before = (*pending, *ec.before)
            pending = []
            filtered_elements_list.append(
                dataclasses.replace(ec, before=new_before),
            )
    return dataclasses.replace(
        collection_comments,
        elements=tuple(filtered_elements_list),
        trailing=(*pending, *collection_comments.trailing),
    )


@dataclasses.dataclass(frozen=True)
class ResolvedComments:
    """Result of resolving YAML comments for a collection or scalar."""

    result: str
    pending: CollectionComments | None
    pending_scalar_before: tuple[str, ...]
    """Already-formatted comment lines to prepend before the variable
    declaration.  Used for scalar before-comments when the language
    does not support them inline (see
    :attr:`~literalizer.Language.supports_scalar_before_comments`).
    """


@beartype
def _resolve_collection_comments(
    *,
    collection_comments: CollectionComments,
    base: str,
    language: Language,
    comment_prefix: str,
    comment_suffix: str,
    comment_line_prefix: str,
    include_delimiters: bool,
) -> ResolvedComments:
    """Resolve pre-extracted collection comments."""
    if not language.supports_collection_comments:
        return ResolvedComments(
            result=base,
            pending=collection_comments,
            pending_scalar_before=(),
        )
    result = apply_collection_comments(
        collection_comments=collection_comments,
        base=base,
        comment_prefix=comment_prefix,
        comment_suffix=comment_suffix,
        comment_line_prefix=comment_line_prefix,
        include_delimiters=include_delimiters,
    )
    return ResolvedComments(
        result=result,
        pending=None,
        pending_scalar_before=(),
    )


@beartype
def _resolve_yaml_collection_comments(
    *,
    ruamel_data: CommentedSeq | CommentedMap,
    data: object,
    base: str,
    language: Language,
    comment_prefix: str,
    comment_suffix: str,
    comment_line_prefix: str,
    include_delimiters: bool,
) -> ResolvedComments:
    """Resolve comments for a YAML list or dict."""
    collection_comments = extract_yaml_comments(
        ruamel_data=ruamel_data,
    )

    if (
        language.skip_null_dict_values
        and isinstance(ruamel_data, CommentedMap)
        and isinstance(data, dict)
    ):
        collection_comments = _filter_null_dict_comments(
            data=data,  # pyright: ignore[reportUnknownArgumentType]
            collection_comments=collection_comments,
        )

    return _resolve_collection_comments(
        collection_comments=collection_comments,
        base=base,
        language=language,
        comment_prefix=comment_prefix,
        comment_suffix=comment_suffix,
        comment_line_prefix=comment_line_prefix,
        include_delimiters=include_delimiters,
    )


@beartype
def resolve_yaml_comments(
    *,
    yaml_string: str,
    raw_data: object,
    base: str,
    language: Language,
    comment_prefix: str,
    comment_suffix: str,
    comment_line_prefix: str,
    line_prefix: str,
    include_delimiters: bool,
) -> ResolvedComments:
    """Resolve comments using the already-parsed round-trip YAML data.

    *raw_data* is the comment-preserving structure produced by
    :func:`_parse_yaml` (a :class:`CommentedMap`, :class:`CommentedSeq`,
    :class:`CommentedSet`, or scalar).  Scalars still need a separate
    token scan because :meth:`YAML.load` discards comment tokens that
    are not attached to a collection.
    """
    # https://sourceforge.net/p/ruamel-yaml/tickets/328/
    match raw_data:
        case CommentedSet():
            return _resolve_collection_comments(
                collection_comments=extract_yaml_comments(
                    ruamel_data=raw_data,
                ),
                base=base,
                language=language,
                comment_prefix=comment_prefix,
                comment_suffix=comment_suffix,
                comment_line_prefix=comment_line_prefix,
                include_delimiters=include_delimiters,
            )
        case CommentedSeq() | CommentedMap():
            return _resolve_yaml_collection_comments(
                ruamel_data=raw_data,
                data=raw_data,
                base=base,
                language=language,
                comment_prefix=comment_prefix,
                comment_suffix=comment_suffix,
                comment_line_prefix=comment_line_prefix,
                include_delimiters=include_delimiters,
            )
        case _:
            stream = StringIO(initial_value=yaml_string)
            tokens = get_yaml().scan(stream=stream)  # pyright: ignore[reportUnknownMemberType]
            scalar_result = literalize_yaml_scalar(
                tokens=tokens,
                base=base,
                comment_prefix=comment_prefix,
                comment_suffix=comment_suffix,
                line_prefix=line_prefix,
                supports_scalar_before_comments=(
                    language.supports_scalar_before_comments
                ),
                supports_scalar_inline_comments=(
                    language.supports_scalar_inline_comments
                ),
            )
            return ResolvedComments(
                result=scalar_result.result,
                pending=None,
                pending_scalar_before=scalar_result.pending_before,
            )


@beartype
def resolve_toml_comments(
    *,
    toml_doc: TOMLDocument,
    base: str,
    language: Language,
    comment_prefix: str,
    comment_suffix: str,
    comment_line_prefix: str,
    include_delimiters: bool,
) -> ResolvedComments:
    """Extract and resolve comments from a tomlkit document."""
    return _resolve_collection_comments(
        collection_comments=extract_toml_comments(toml_doc=toml_doc),
        base=base,
        language=language,
        comment_prefix=comment_prefix,
        comment_suffix=comment_suffix,
        comment_line_prefix=comment_line_prefix,
        include_delimiters=include_delimiters,
    )
