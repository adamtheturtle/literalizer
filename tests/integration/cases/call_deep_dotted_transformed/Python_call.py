from __future__ import annotations
class _ClientType:
    def fetch(self, *_args: object, **_kwargs: object) -> object: ...
class _AppType:
    client = _ClientType()
app = _AppType()
def emit(*_args: object, **_kwargs: object) -> object: ...
emit(app.client.fetch(payload="hello"))
emit(app.client.fetch(payload=42))
emit(app.client.fetch(payload=True))
