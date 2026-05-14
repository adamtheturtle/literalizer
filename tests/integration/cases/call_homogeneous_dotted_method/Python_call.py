from __future__ import annotations
class _ClientType:
    def fetch(self, *_args: object, **_kwargs: object) -> object: ...
class _AppType:
    client = _ClientType()
app = _AppType()
app.client.fetch(value="hello")
app.client.fetch(value="world")
