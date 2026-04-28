import json
type ThrottlerType = object
proc check(self: ThrottlerType; args: varargs[untyped]): untyped = 0
var throttler: ThrottlerType
proc emit(args: varargs[untyped]) = discard
emit(throttler.check("user_1", 1000.0))
emit(throttler.check("user_2", 2000.5))
