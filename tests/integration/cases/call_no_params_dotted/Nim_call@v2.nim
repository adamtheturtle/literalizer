type ThrottlerType = object
template check(self: ThrottlerType; args: varargs[untyped]) = discard
var throttler: ThrottlerType
throttler.check()
throttler.check()
