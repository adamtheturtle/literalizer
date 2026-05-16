object Fixture_record_named_shape_Scala_record_shape_names_Task {
case class Task(id: Int, description: String, is_done: Boolean, blocks: List[Int])
val my_data = List(
    Task(id = 100, description = "first task", is_done = false, blocks = List[Int](102, 103)),
    Task(id = 101, description = "second task", is_done = true, blocks = List[Int](100)),
)
}
