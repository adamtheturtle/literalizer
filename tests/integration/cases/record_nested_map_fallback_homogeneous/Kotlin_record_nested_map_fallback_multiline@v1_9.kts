data class Record1(val kind: String, val pr_id: String)
data class Record0(val name: String, val input: Record1, val expected: Map<String, String>)
val my_data = listOf<Any?>(
    Record0(
        name = "test_1",
        input = Record1(
            kind = "create",
            pr_id = "pr_1",
        ),
        expected = mapOf<String, String>(
            "pr_id" to "pr_1",
            "status" to "draft",
        ),
    ),
    Record0(
        name = "test_2",
        input = Record1(
            kind = "publish",
            pr_id = "pr_1",
        ),
        expected = mapOf<String, String>(
            "error" to "invalid_operation",
        ),
    ),
)
