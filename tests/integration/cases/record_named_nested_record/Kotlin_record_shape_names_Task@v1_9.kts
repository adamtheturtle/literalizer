data class Task(val id: Int, val description: String, val is_done: Boolean, val blocks: IntArray)
data class Record0(val project: String, val lead_task: Task)
val my_data = Record0(
    project = "alpha",
    lead_task = Task(
        id = 100,
        description = "first task",
        is_done = false,
        blocks = intArrayOf(
            102,
            103,
        ),
    ),
)
