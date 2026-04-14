class _ThrottlerType { fun check(user_id: Any? = null, ts: Any? = null): Any? = null }
val throttler = _ThrottlerType()
fun emit(_arg: Any? = null): Any? = null
emit(throttler.check("user_1", 1000.0))
emit(throttler.check("user_2", 2000.5))
