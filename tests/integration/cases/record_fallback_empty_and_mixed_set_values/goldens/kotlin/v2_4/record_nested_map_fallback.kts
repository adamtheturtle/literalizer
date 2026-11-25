data class Record0(val name: String, val payload: Map<String, Any?>)
val my_data = listOf<Record0>(
    Record0(name = "one", payload = mapOf<String, Any?>("scalar" to 1, "empty" to setOf<Any?>(), "mixed" to setOf<Any?>(2, "word"))),
    Record0(name = "two", payload = mapOf<String, Any?>("other" to 2)),
)
