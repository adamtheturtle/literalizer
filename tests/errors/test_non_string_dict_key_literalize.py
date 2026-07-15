"""End-to-end rejection of non-string dict keys via
:func:`literalizer.literalize`.

The YAML parser preserves the native key type (e.g. ``int``,
``datetime.date``, ``bool``), so YAML inputs with non-string keys now
reach the per-language guard in :func:`literalizer._literalize`.
Languages that set ``supports_non_string_dict_keys = False`` raise
:class:`~literalizer.exceptions.UnrepresentableInputError`; this module
locks in the contract for JSON-family targets and for the
statically-typed-map languages whose typed-map output would otherwise
emit a key type that disagrees with the literal.
"""

import re

import pytest

import literalizer
from literalizer.exceptions import (
    MixedDictKeysError,
    UnrepresentableInputError,
)
from literalizer.languages import (
    CSharp,
    Dhall,
    Go,
    Haskell,
    Json5,
    Jsonnet,
    Kotlin,
    Mojo,
    Nix,
    Scala,
    Toml,
    TypeScript,
)

_INT_KEY_YAML = "1: one\n2: two\n"
_DATE_KEY_YAML = "2024-01-01: new_year\n"
_BOOL_KEY_YAML = "true: yes\nfalse: no\n"
_MIXED_INT_STR_KEY_YAML = "1: one\nfoo: bar\n"


@pytest.mark.parametrize(
    argnames="lang_cls",
    argvalues=[Json5, Jsonnet, Toml, Nix, Dhall],
)
@pytest.mark.parametrize(
    argnames="source",
    argvalues=[_INT_KEY_YAML, _DATE_KEY_YAML, _BOOL_KEY_YAML],
    ids=["int_key", "date_key", "bool_key"],
)
def test_string_keyed_languages_reject_non_string_keys(
    lang_cls: literalizer.LanguageCls,
    source: str,
) -> None:
    """Languages whose key syntax is string-only raise on non-string
    keys.
    """
    with pytest.raises(expected_exception=UnrepresentableInputError):
        literalizer.literalize(
            source=source,
            input_format=literalizer.InputFormat.YAML,
            language=lang_cls(),
        )


@pytest.mark.parametrize(
    argnames="lang_cls",
    argvalues=[Go, Kotlin, CSharp, Haskell, Scala, TypeScript],
)
def test_typed_map_languages_reject_non_string_keys(
    lang_cls: literalizer.LanguageCls,
) -> None:
    """Statically-typed-map languages reject non-string keys until
    proper typed-map syntax is implemented for each.
    """
    with pytest.raises(expected_exception=UnrepresentableInputError):
        literalizer.literalize(
            source=_INT_KEY_YAML,
            input_format=literalizer.InputFormat.YAML,
            language=lang_cls(),
            variable_form=literalizer.NewVariable(
                name="my_data", modifiers=frozenset()
            ),
        )


def test_rejection_names_target_language_and_key_type() -> None:
    """The error identifies the target language and the offending key
    type.
    """
    expected_msg = re.escape(
        pattern="Json5 cannot represent dict key of type int",
    )
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match=f"^{expected_msg}$",
    ):
        literalizer.literalize(
            source=_INT_KEY_YAML,
            input_format=literalizer.InputFormat.YAML,
            language=Json5(),
        )


def test_mixed_int_string_keys_reject_on_homogeneous_target() -> None:
    """A YAML input with mixed-type keys raises on a target that
    accepts non-string keys but requires homogeneity (the foundation
    check from #2201).
    """
    with pytest.raises(expected_exception=MixedDictKeysError):
        literalizer.literalize(
            source=_MIXED_INT_STR_KEY_YAML,
            input_format=literalizer.InputFormat.YAML,
            language=Mojo(),
            variable_form=literalizer.NewVariable(
                name="my_data", modifiers=frozenset()
            ),
        )
