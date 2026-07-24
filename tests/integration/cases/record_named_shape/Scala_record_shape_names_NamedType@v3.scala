object Fixture_record_named_shape_Scala_record_shape_names_NamedType {
case class NamedType(id: Int, label: String, enabled: Boolean, related_ids: List[Int])
val my_data = List(
    NamedType(id = 100, label = "first item", enabled = false, related_ids = List[Int](102, 103)),
    NamedType(id = 101, label = "second item", enabled = true, related_ids = List[Int](100)),
)
}
