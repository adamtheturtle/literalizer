val my_data = listOf<Map<String, Map<String, Any?>>>(
    mapOf<String, Map<String, Any?>>("input" to mapOf<String, Any?>("name" to "alice", "city" to "paris"), "expected" to mapOf<String, Any?>("count" to 1, "total" to 2)),
    mapOf<String, Map<String, Any?>>("input" to mapOf<String, Any?>("name" to 10, "city" to 20), "expected" to mapOf<String, Any?>("count" to "done", "total" to "pending")),
)
