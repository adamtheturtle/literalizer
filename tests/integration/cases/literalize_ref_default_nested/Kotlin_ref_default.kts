val item_var = mapOf<String, String>(
    "_" to "_",
)
val my_data = mapOf<String, Any?>(
    "items" to listOf<Map<String, String>>(item_var, mapOf<String, String>("fallback" to "value")),
)
