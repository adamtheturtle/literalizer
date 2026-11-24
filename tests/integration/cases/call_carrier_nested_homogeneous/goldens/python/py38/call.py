class _ClientType:
    def go(self, *_args: object, **_kwargs: object) -> object: ...
class _AppType:
    client = _ClientType()
app = _AppType()
app.client.go(first_value=(1,), second_value=(2,))
