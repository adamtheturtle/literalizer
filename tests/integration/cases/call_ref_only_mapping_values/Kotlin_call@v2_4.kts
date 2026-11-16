fun consume(value: Any? = null): Any? = listOf<Any?>(value)
val item = 42
consume(value = mapOf<String, Int>("field" to item))
