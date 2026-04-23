class _ThrottlerType { def check(Object... _args) { null } }
def throttler = new _ThrottlerType()
def emit(Object... _args) { null }
emit(throttler.check(user_id: "user_1", ts: 1000.0))
emit(throttler.check(user_id: "user_2", ts: 2000.5))
