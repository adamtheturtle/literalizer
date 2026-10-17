fun process(data: Any? = null): Any? = listOf<Any?>(data)
val myVar = 42
process(data = listOf<Any?>(myVar, 42, "static"))
