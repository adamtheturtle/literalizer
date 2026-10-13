class _ThrottlerType { fun check(@Suppress("UNUSED_PARAMETER") user_id: Any? = null, @Suppress("UNUSED_PARAMETER") ts: Any? = null): Any? = null }
val throttler = _ThrottlerType()
fun emit(@Suppress("UNUSED_PARAMETER") _arg: Any? = null): Any? = null
emit(throttler.check("user_1", 1000.0))
emit(throttler.check("user_2", 2000.5))
