class _ThingType:
    def go(self, *_args: object, **_kwargs: object) -> object: ...
thing = _ThingType()
thing.go(before=(), populated=(1,), after=())
thing.go(before=("text",), populated=(2,), after=())
thing.go(before=(), populated=("text",), after=())
thing.go(before=("text",), populated=(2,), after=(3,))
