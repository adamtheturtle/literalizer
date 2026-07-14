val deep = mapOf<String, String>(
    "_" to "_",
)
val my_data = mapOf<String, Map<String, Map<String, Map<String, String>>>>(
    "a" to mapOf<String, Map<String, Map<String, String>>>("b" to mapOf<String, Map<String, String>>("c" to deep)),
)
