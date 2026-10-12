class _HttpClientType:
    def fetch(self, *_args: object, **_kwargs: object) -> object: ...
class _MyAppType:
    http_client = _HttpClientType()
my_app = _MyAppType()
my_app.http_client.fetch(payload="hello")
my_app.http_client.fetch(payload=42)
my_app.http_client.fetch(payload=True)
