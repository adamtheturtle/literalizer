data class Record0(val name: String, val input: Map<String, Any?>, val expected: Map<String, Any?>)
val my_data = listOf<Any?>(
    Record0(
        name = "test_1",
        input = mapOf<String, Any?>(
            "type" to "create",
            "pr_id" to "pr_1",
            "draft" to true,
            "missing" to null,
        ),
        expected = mapOf<String, Any?>(
            "pr_id" to "pr_1",
            "status" to "draft",
        ),
    ),
    Record0(
        name = "test_2",
        input = mapOf<String, Any?>(
            "type" to "publish",
            "pr_id" to "pr_1",
        ),
        expected = mapOf<String, Any?>(
            "error" to "invalid_operation",
        ),
    ),
)
