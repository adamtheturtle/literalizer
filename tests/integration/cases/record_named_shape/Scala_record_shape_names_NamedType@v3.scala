object Fixture_record_named_shape_Scala_record_shape_names_NamedType {
case class NamedType(id: Int, description: String, is_done: Boolean, blocks: List[Int])
val my_data = List(
    NamedType(id = 100, description = "first task", is_done = false, blocks = List[Int](102, 103)),
    NamedType(id = 101, description = "second task", is_done = true, blocks = List[Int](100)),
)
}
