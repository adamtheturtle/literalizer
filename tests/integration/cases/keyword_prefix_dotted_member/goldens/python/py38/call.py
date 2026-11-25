class _ThingType:
    def first_value(self, *_args: object, **_kwargs: object) -> object: ...
thing = _ThingType()
thing.first_value(value=1)
