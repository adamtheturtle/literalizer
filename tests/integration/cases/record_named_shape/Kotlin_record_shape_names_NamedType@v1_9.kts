data class NamedType(val id: Int, val label: String, val enabled: Boolean, val related_ids: IntArray)
val my_data = listOf<Any?>(
    NamedType(id = 100, label = "first item", enabled = false, related_ids = intArrayOf(102, 103)),
    NamedType(id = 101, label = "second item", enabled = true, related_ids = intArrayOf(100)),
)
