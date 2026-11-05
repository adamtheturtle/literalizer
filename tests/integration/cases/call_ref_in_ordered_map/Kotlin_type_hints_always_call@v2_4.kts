fun process(a: Any? = null): Any? = listOf<Any?>(a)
val big_list: Array<String> = arrayOf(
    "x",
)
process(a = linkedMapOf<String, Any?>("m" to big_list))
