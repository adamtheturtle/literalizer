fun process(a: Any? = null, b: Any? = null): Any? = listOf<Any?>(a, b)
val big_list = arrayOf(
    "x",
)
process(a = mapOf<String, Array<String>>("k" to big_list), b = 2)
