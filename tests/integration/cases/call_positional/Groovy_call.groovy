class _ThrottlerType { def check(user_id, ts) { null } }
def throttler = new _ThrottlerType()
def emit(_arg) { null }
emit(throttler.check("user_1", 1000.0))
emit(throttler.check("user_2", 2000.5))
