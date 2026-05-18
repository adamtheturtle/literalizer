fun process(value: Any? = null): Any? = null
fun emit(_call: Any? = null, _zip: Any? = null): Any? = null
emit(process(value = "hello"), mapOf<String, Int>("a" to 1, "b" to 2))
emit(process(value = 42), mapOf<String, Int>("c" to 3, "d" to 4))
