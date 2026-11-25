fun process(value: Any? = null, extra: Any? = null): Any? = listOf<Any?>(value, extra)
process(value = 1, extra = "hello")
process(value = "two", extra = false)
process(value = 3.5, extra = null)
