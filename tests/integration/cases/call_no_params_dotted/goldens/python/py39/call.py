class _ThrottlerType:
    def check(self, *_args: object, **_kwargs: object) -> object: ...
throttler = _ThrottlerType()
throttler.check()
throttler.check()
