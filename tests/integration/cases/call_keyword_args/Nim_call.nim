type ThrottlerType = object
template check(self: ThrottlerType; args: varargs[untyped]): untyped {.discardable.} = 0
var throttler: ThrottlerType
template emit(args: varargs[untyped]) = discard
emit(throttler.check("user_1", 1000.0))
emit(throttler.check("user_2", 2000.5))
