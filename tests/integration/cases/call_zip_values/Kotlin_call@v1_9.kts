fun process(@Suppress("UNUSED_PARAMETER") value: Any? = null): Any? = null
fun emit(@Suppress("UNUSED_PARAMETER") _call: Any? = null, @Suppress("UNUSED_PARAMETER") _zip: Any? = null): Any? = null
emit(process(value = "hello"), true)
emit(process(value = 42), false)
