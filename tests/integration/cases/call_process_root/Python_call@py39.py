class _ApiType:
    def fetch(self, *_args: object, **_kwargs: object) -> object: ...
class _ProcessType:
    api = _ApiType()
process = _ProcessType()
process.api.fetch(data={"data": "hello"})
process.api.fetch(data={"data": 42})
process.api.fetch(data={"data": True})
