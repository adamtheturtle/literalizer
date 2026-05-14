from __future__ import annotations
class _Http_clientType:
    def fetch(self, *_args: object, **_kwargs: object) -> object: ...
class _My_appType:
    http_client = _Http_clientType()
my_app = _My_appType()
my_app.http_client.fetch(payload="hello")
my_app.http_client.fetch(payload=42)
my_app.http_client.fetch(payload=True)
