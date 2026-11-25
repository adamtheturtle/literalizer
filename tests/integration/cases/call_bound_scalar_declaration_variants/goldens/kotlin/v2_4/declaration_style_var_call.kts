fun consume(value: Any? = null): Any? = listOf<Any?>(value)
var shared = 42
consume(value = shared)
