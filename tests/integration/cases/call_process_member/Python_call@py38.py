class _ProcessType:
    def fetch(self, *_args: object, **_kwargs: object) -> object: ...
class _AppType:
    process = _ProcessType()
app = _AppType()
app.process.fetch(data={"data": "hello"})
app.process.fetch(data={"data": 42})
app.process.fetch(data={"data": True})
