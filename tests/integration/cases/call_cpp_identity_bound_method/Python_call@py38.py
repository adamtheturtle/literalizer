class _ThingType:
    def go(self, *_args: object, **_kwargs: object) -> object: ...
thing = _ThingType()
item = (
    1,
    2,
)
thing.go(value=item)
