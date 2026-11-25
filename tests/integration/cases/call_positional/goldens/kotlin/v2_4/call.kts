class _ThrottlerType { fun check(user_id: Any? = null, ts: Any? = null): Any? = listOf<Any?>(user_id, ts) }
val throttler = _ThrottlerType()
fun emit(_arg: Any? = null): Any? = listOf<Any?>(_arg)
emit(throttler.check("user_1", 1000.0))
emit(throttler.check("user_2", 2000.5))
