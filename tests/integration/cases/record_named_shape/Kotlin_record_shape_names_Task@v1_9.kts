data class Task(val id: Int, val description: String, val is_done: Boolean, val blocks: IntArray)
val my_data = listOf<Any?>(
    Task(id = 100, description = "first task", is_done = false, blocks = intArrayOf(102, 103)),
    Task(id = 101, description = "second task", is_done = true, blocks = intArrayOf(100)),
)
