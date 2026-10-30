"""The shared semantic verifier preserves JSON value distinctions."""

import pytest

from scripts.roundtrip_common import verify


@pytest.mark.parametrize(
    argnames=("expected_json", "produced_json"),
    argvalues=[
        ('{"value": true}', '{"value": 1}'),
        ('{"value": 1}', '{"value": true}'),
        ('{"value": false}', '{"value": 0}'),
        ('{"value": 0}', '{"value": false}'),
        ('{"value": [true]}', '{"value": [1.0]}'),
        ('{"value": [0.0]}', '{"value": [false]}'),
        (
            '{"value": {"nested": [1, false]}}',
            '{"value": {"nested": [true, 0]}}',
        ),
        (
            '{"value": {"nested": [true, 0]}}',
            '{"value": {"nested": [1, false]}}',
        ),
        ('{"value": [1, 2]}', '{"value": [2, 1]}'),
        ('{"value": [1]}', '{"value": [1, 2]}'),
        ('{"value": null}', '{"value": 0}'),
        ('{"value": "true"}', '{"value": true}'),
        ('{"value": {"a": 1}}', '{"value": {"b": 1}}'),
    ],
)
def test_roundtrip_mismatch(
    expected_json: str,
    produced_json: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Changed JSON values fail with the existing mismatch diagnostic."""
    with pytest.raises(expected_exception=SystemExit) as exc_info:
        verify(
            label="negative-control",
            produced_json=produced_json,
            exclude_keys=(),
            expected_json=expected_json,
        )
    assert exc_info.value.code == 1
    assert "negative-control: round-trip mismatch" in capsys.readouterr().err


@pytest.mark.parametrize(
    argnames=("expected_json", "produced_json", "exclude_keys"),
    argvalues=[
        (
            '{"value": [true, false, 0, 1]}',
            '{"value": [true, false, 0, 1]}',
            (),
        ),
        ('{"value": 1}', '{"value": 1.0}', ()),
        ('{"value": [0.0, 1.0]}', '{"value": [0, 1]}', ()),
        (
            '{"a": {"x": false, "y": [1]}, "b": null}',
            '{"b": null, "a": {"y": [1.0], "x": false}}',
            (),
        ),
        (
            '{"keep": true, "skip": 1}',
            '{"keep": true, "skip": false}',
            ("skip",),
        ),
        ('{"keep": true}', '{"keep": true, "skip": 0}', ("skip",)),
    ],
)
def test_roundtrip_equivalent(
    expected_json: str,
    produced_json: str,
    exclude_keys: tuple[str, ...],
) -> None:
    """Retain numeric equivalence, object ordering and key exclusions."""
    verify(
        label="passing-control",
        produced_json=produced_json,
        exclude_keys=exclude_keys,
        expected_json=expected_json,
    )
