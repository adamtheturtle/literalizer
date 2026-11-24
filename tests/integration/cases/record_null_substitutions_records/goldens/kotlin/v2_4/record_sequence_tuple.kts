data class Record0(val due_date: Int, val parent_id: Int, val assignee: String)
val my_data = listOf<Record0>(
    Record0(due_date = -1, parent_id = -1, assignee = ""),
    Record0(due_date = 10, parent_id = 20, assignee = "alice"),
)
