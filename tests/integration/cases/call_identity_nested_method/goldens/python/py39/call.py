class _ThingType:
    def go(self, *_args: object, **_kwargs: object) -> object: ...
class _OuterType:
    thing = _ThingType()
outer = _OuterType()
outer.thing.go()
