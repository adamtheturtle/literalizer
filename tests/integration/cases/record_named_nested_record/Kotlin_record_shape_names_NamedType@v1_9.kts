data class NamedType(val id: Int, val description: String, val is_done: Boolean, val blocks: IntArray)
data class Record0(val project: String, val lead_task: NamedType)
val my_data = Record0(
    project = "alpha",
    lead_task = NamedType(
        id = 100,
        description = "first task",
        is_done = false,
        blocks = intArrayOf(
            102,
            103,
        ),
    ),
)
