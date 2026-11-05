fun process(value: Any? = null): Any? = listOf<Any?>(value)
fun emit(_call: Any? = null, _zip: Any? = null): Any? = listOf<Any?>(_call, _zip)
emit(process(value = "hello"), mapOf<String, Int>("a" to 1, "b" to 2))
emit(process(value = 42), mapOf<String, Int>("c" to 3, "d" to 4))
