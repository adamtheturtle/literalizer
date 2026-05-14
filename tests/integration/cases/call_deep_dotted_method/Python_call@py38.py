from __future__ import annotations
class _ClientType:
    def post(self, *_args: object, **_kwargs: object) -> object: ...
class _ApiType:
    client = _ClientType()
class _ObjType:
    api = _ApiType()
obj = _ObjType()
obj.api.client.post(data="hello")
obj.api.client.post(data=42)
obj.api.client.post(data=True)
