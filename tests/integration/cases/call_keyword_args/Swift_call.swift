class _throttlerType { func check(_ a: Any...) -> Any { 0 } }
let throttler = _throttlerType()
func print(_ a: Any...) -> Any { 0 }
print(throttler.check(user_id: "user_1", ts: 1000.0))
print(throttler.check(user_id: "user_2", ts: 2000.5))
