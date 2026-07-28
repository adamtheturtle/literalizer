def process(*_args: object, **_kwargs: object) -> object: ...
known_value = True
unknown_value = True
process(known_value=known_value, nested_missing=(unknown_value,))
