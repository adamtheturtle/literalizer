object Fixture_d_record_fallback_empty_array_Scala_record_nested_map_fallback {
case class Record0(name: String, payload: Map[String, Any])
val my_data = List(
    Record0(name = "one", payload = Map[String, Any]("scalar" -> 1, "items" -> List())),
    Record0(name = "two", payload = Map[String, Any]("other" -> 2)),
)
}
