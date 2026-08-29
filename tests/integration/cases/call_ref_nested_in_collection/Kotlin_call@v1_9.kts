fun process(a: Any? = null, b: Any? = null): Any? = null
val big_list = arrayOf(
    "x",
)
process(a = mapOf<String, Array<String>>("k" to big_list), b = linkedMapOf<String, Any?>("m" to big_list))
