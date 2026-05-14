from __future__ import annotations
class _ThrottlerType:
    def check(self, *_args: object, **_kwargs: object) -> object: ...
throttler = _ThrottlerType()
def emit(*_args: object, **_kwargs: object) -> object: ...
emit(throttler.check(user_id="user_1", ts=1000.0))
emit(throttler.check(user_id="user_2", ts=2000.5))
