class _AppType:
    def go(self, *_args: object, **_kwargs: object) -> object: ...
app = _AppType()
app.go(first_value=(1,), second_value=(2,))
