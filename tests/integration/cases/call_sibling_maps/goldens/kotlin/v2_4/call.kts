fun process(value: Any? = null): Any? = listOf<Any?>(value)
process(value = mapOf<String, Any?>("value" to 1))
process(value = mapOf<String, Any?>("value" to "hello"))
