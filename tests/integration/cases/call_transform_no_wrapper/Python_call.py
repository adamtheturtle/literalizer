class _ApiType:
    def request(self, *_args: object, **_kwargs: object) -> object: ...
class _ClientType:
    api = _ApiType()
client = _ClientType()
client.api.request(data="hello")
client.api.request(data=42)
client.api.request(data=True)
