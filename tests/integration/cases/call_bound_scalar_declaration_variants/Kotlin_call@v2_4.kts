fun consume(value: Any? = null): Any? = listOf<Any?>(value)
val shared = 42
consume(value = shared)
