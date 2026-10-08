class _OuterType:
    def inner(self, *_args: object, **_kwargs: object) -> object: ...
outer = _OuterType()
outer.inner(outer=1, n=2)
