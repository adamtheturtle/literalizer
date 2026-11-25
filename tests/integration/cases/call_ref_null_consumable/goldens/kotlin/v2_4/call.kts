fun consume(value: Any? = null): Any? = listOf<Any?>(value)
val my_null = null
val regular_null = null
consume(value = my_null)
consume(value = regular_null)
