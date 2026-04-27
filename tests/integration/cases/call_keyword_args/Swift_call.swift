class _throttlerType { @discardableResult func check(user_id: Any = 0, ts: Any = 0) -> Any { 0 } }
let throttler = _throttlerType()
@discardableResult func emit(_ _arg: Any = 0) -> Any { 0 }
emit(throttler.check(user_id: "user_1", ts: 1000.0));
emit(throttler.check(user_id: "user_2", ts: 2000.5));
