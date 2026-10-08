val actual = 42
val my_data = listOf<Any?>(
    mapOf<String, Any?>("\$ref" to 1),
    mapOf<String, Any?>("\$ref" to null),
    actual,
)
