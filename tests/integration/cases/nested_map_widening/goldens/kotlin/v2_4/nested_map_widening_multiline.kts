val my_data = listOf<Map<String, Map<String, Any?>>>(
    mapOf<String, Map<String, Any?>>(
        "input" to mapOf<String, Any?>(
            "kind" to "add",
            "item_id" to "item_1",
            "urgent" to true,
        ),
        "expected" to mapOf<String, Any?>(
            "item_id" to "item_1",
            "state" to "pending",
        ),
    ),
    mapOf<String, Map<String, Any?>>(
        "input" to mapOf<String, Any?>(
            "kind" to "remove",
            "item_id" to "item_9",
        ),
        "expected" to mapOf<String, Any?>(
            "error" to "not_found",
        ),
    ),
)
