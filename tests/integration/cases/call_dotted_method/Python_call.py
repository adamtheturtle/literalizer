class _ClientType:
    def send(self, *_args: object, **_kwargs: object) -> object: ...
class _NsType:
    client = _ClientType()
ns = _NsType()
ns.client.send(payload="hello")
ns.client.send(payload=42)
ns.client.send(payload=True)
