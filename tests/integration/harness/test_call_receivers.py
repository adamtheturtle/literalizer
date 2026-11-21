"""Native integer receiver coverage."""

from literalizer.languages import ALL_LANGUAGES
from tests.integration.call_receivers import integer_receiver_syntax


def test_every_stateful_integer_signature_has_native_syntax() -> None:
    """Native syntax tables cannot silently sample capable backends."""
    assert set(integer_receiver_syntax()) == {
        cls.language_id
        for cls in ALL_LANGUAGES
        if cls.supports_stateful_free_call_consumers
    }
