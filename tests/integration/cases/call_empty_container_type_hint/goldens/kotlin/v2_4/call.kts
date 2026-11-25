fun process(values: Any? = null, count: Any? = null): Any? = listOf<Any?>(values, count)
process(values = listOf<Any?>(1, mapOf<String, Any?>()), count = 42)
