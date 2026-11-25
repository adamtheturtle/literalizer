class _ThingType:
    def Before(self, *_args: object, **_kwargs: object) -> object: ...
thing = _ThingType()
thing.Before(value=1)
