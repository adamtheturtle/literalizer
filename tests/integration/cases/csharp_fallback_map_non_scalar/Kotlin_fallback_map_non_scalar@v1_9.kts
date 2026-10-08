data class Record0(val name: String, val payload: Map<String, Int>)
val my_data = listOf<Record0>(
    Record0(name = "one", payload = mapOf<String, Int>("scalar" to 1, "items" to intArrayOf(2, 3))),
    Record0(name = "two", payload = mapOf<String, Int>("other" to 2)),
)
