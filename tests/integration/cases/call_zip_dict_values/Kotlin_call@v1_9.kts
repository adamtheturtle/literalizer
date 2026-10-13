fun process(@Suppress("UNUSED_PARAMETER") value: Any? = null): Any? = null
fun emit(@Suppress("UNUSED_PARAMETER") _call: Any? = null, @Suppress("UNUSED_PARAMETER") _zip: Any? = null): Any? = null
emit(process(value = "hello"), mapOf<String, Int>("a" to 1, "b" to 2))
emit(process(value = 42), mapOf<String, Int>("c" to 3, "d" to 4))
