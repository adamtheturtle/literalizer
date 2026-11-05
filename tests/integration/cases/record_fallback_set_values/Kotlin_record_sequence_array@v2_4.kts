data class Record0(val name: String, val payload: Map<String, Any?>)
val my_data = listOf<Record0>(
    Record0(name = "one", payload = mapOf<String, Any?>("scalar" to 1, "items" to setOf<Int>(2, 3))),
    Record0(name = "two", payload = mapOf<String, Any?>("other" to 2)),
)
