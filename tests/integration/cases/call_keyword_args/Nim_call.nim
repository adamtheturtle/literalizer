type ThrottlerType = object
proc check[T0, T1](self: ThrottlerType; user_id: T0; ts: T1): int {.discardable.} = 0
var throttler: ThrottlerType
template emit(args: varargs[untyped]) = discard
emit(throttler.check("user_1", 1000.0))
emit(throttler.check("user_2", 2000.5))
