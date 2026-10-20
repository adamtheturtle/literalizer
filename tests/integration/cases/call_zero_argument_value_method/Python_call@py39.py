class _ThingType:
    def go(self, *_args: object, **_kwargs: object) -> object: ...
thing = _ThingType()
thing.go()
