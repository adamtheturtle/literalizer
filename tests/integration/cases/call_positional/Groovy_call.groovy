class _ThrottlerType { def check(Object... _args) { null } }
def throttler = new _ThrottlerType()
def emit(Object... _args) { null }
emit(throttler.check("user_1", 1000.0))
emit(throttler.check("user_2", 2000.5))
