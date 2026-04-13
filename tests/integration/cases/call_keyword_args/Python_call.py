class _ThrottlerType:
    def check(self, *, user_id: object, ts: object) -> object: ...
throttler = _ThrottlerType()
print(throttler.check(user_id="user_1", ts=1000.0))
print(throttler.check(user_id="user_2", ts=2000.5))
