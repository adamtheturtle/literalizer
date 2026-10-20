def consume(*_args: object, **_kwargs: object) -> object: ...
my_null = None
regular_null = None
consume(value=my_null)
consume(value=regular_null)
