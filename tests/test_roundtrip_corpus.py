"""The shared round-trip corpus retains adversarial string coverage."""

import json

from scripts import roundtrip_common


def test_adversarial_strings_are_in_shared_roundtrip_corpus() -> None:
    """Keep syntax-sensitive and C0 characters in the shared document."""
    corpus: dict[str, object] = json.loads(s=roundtrip_common.read_input())
    interpolation = corpus["string_interpolation"]
    assert isinstance(interpolation, str)
    for token in ("$", "`", "@", "#{"):
        assert token in interpolation

    controls = corpus["string_controls"]
    assert isinstance(controls, str)
    assert controls == "bell \x07f escape \x1b0 unit-separator \x1f9"
    assert corpus["string_nul"] == "before\0after"
