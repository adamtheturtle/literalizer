import json
type ThrottlerType = object
proc check(self: ThrottlerType, a: varargs[string]) {.used.} = discard
let throttler {.used.} = ThrottlerType()
proc print(a: varargs[string]) {.used.} = discard
print(throttler.check(user_id = "user_1", ts = 1000.0))
print(throttler.check(user_id = "user_2", ts = 2000.5))
