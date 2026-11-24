fun process(data: Any? = null): Any? = listOf<Any?>(data)
val untypedValue = arrayOf<Any?>()
process(data = arrayOf<Any?>(untypedValue, untypedValue))
