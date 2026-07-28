fun process(data: Any? = null): Any? = null
val my_list = mapOf<String, String>(
    "unused" to "value",
)
process(data = listOf<Any?>(listOf<Map<String, Map<String, String>>>(mapOf<String, Map<String, String>>("inner" to my_list))))
