fun process(data: Any? = null): Any? = listOf<Any?>(data)
val item = arrayOf<Any?>(
    1,
    2,
)
process(data = arrayOf<Any?>(item, item))
