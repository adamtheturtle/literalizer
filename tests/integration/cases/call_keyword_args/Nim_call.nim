import json
type ThrottlerType_ = object
proc check(self: ThrottlerType_; _args: varargs[untyped]): untyped = 0
var throttler: ThrottlerType_
proc emit(_args: varargs[untyped]) = discard
emit(throttler.check("user_1", 1000.0))
emit(throttler.check("user_2", 2000.5))
