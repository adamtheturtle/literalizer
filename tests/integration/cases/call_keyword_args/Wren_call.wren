class Throttler_ {
    construct new() {}
    check(user_id, ts) {}
}
var throttler = Throttler_.new()
class Emit_ {
    construct new() {}
    call(arg) {}
}
var emit = Emit_.new()
emit(throttler.check("user_1", 1000.0))
emit(throttler.check("user_2", 2000.5))
