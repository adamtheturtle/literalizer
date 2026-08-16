"""Reject target-induced collisions between distinct mapping keys."""

import pytest

from literalizer import InputFormat, literalize
from literalizer._language import Language
from literalizer.exceptions import MixedDictKeysError
from literalizer.languages import Bash, Hcl, Perl, Raku, Tcl


@pytest.mark.parametrize(
    argnames="language",
    argvalues=[Bash(), Perl(), Tcl(), Raku(), Hcl()],
)
def test_integer_and_string_key_collision_is_rejected(
    language: Language,
) -> None:
    """String-keyed target maps cannot preserve both YAML keys."""
    with pytest.raises(
        expected_exception=MixedDictKeysError,
        match="stringifies distinct dict keys 1 and '1' as '1'",
    ):
        literalize(
            source='1: integer\n"1": string\n',
            input_format=InputFormat.YAML,
            language=language,
        )


@pytest.mark.parametrize(
    argnames="language",
    argvalues=[Bash(), Perl(), Tcl(), Raku(), Hcl()],
)
def test_noncolliding_mixed_keys_remain_supported(
    language: Language,
) -> None:
    """Mixed key types remain valid when their target spellings differ."""
    result = literalize(
        source='1: integer\n"2": string\n',
        input_format=InputFormat.YAML,
        language=language,
    )
    assert "integer" in result.code
    assert "string" in result.code
