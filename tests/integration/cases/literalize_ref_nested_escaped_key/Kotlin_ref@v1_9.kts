val foo = mapOf<String, String>(
    "_" to "_",
)
val my_data = mapOf<String, Any?>(
    "items" to listOf<Map<String, Int>>(mapOf<String, Any?>("other" to 1), foo),
    "mapping" to mapOf<String, Map<String, String>>("value" to foo),
)
