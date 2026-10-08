object Fixture_zig_record_fallback_set_values_Scala_record_nested_map_fallback {
case class Record0(name: String, payload: Map[String, Any])
val my_data = List(
    Record0(name = "one", payload = Map[String, Any]("scalar" -> 1, "items" -> Set[Int](2, 3))),
    Record0(name = "two", payload = Map[String, Any]("other" -> 2)),
)
}
