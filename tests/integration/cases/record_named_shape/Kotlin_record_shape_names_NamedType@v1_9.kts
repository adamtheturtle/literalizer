data class NamedType(val id: Int, val description: String, val is_done: Boolean, val blocks: IntArray)
val my_data = listOf<Any?>(
    NamedType(id = 100, description = "first task", is_done = false, blocks = intArrayOf(102, 103)),
    NamedType(id = 101, description = "second task", is_done = true, blocks = intArrayOf(100)),
)
