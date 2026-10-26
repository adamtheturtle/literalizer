fun process(data: Any? = null): Any? = listOf<Any?>(data)
val untypedValue = listOf<Any?>()
process(data = listOf<Any?>(untypedValue, untypedValue))
