class _ThrottlerType { fun check(user_id: Any? = null, ts: Any? = null): Any? = null }
val throttler = _ThrottlerType()
fun emit(_arg: Any? = null): Any? = null
emit(throttler.check(user_id = "user_1", ts = 1000.0))
emit(throttler.check(user_id = "user_2", ts = 2000.5))
