object Fixture_record_named_nested_record_Scala_record_shape_names_Task {
case class Task(id: Int, description: String, is_done: Boolean, blocks: List[Int])
case class Record0(project: String, lead_task: Task)
val my_data = Record0(
    project = "alpha",
    lead_task = Task(
        id = 100,
        description = "first task",
        is_done = false,
        blocks = List[Int](
            102,
            103,
        ),
    ),
)
}
