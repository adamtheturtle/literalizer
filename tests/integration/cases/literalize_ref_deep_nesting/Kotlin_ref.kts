val deep = mapOf<String, String>(
    "_" to "_",
)
val my_data = mapOf<String, Any?>(
    "a" to mapOf<String, Any?>("b" to mapOf<String, Any?>("c" to deep)),
)
