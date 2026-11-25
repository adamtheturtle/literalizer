def process(*_args: object, **_kwargs: object) -> object: ...
process(value=1, extra="hello")
process(value="two", extra=False)
process(value=3.5, extra=None)
