from __future__ import annotations
class _ClientType:
    def fetch(self, *_args: object, **_kwargs: object) -> object: ...
class _AppType:
    client = _ClientType()
app = _AppType()
app.client.fetch(payload="hello")
app.client.fetch(payload=42)
app.client.fetch(payload=True)
