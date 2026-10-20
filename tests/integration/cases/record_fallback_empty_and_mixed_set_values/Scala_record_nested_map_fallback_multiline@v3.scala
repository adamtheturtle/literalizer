object Fixture_record_fallback_empty_and_mixed_set_values_Scala_record_nested_map_fallback_multiline {
case class Record0(name: String, payload: Map[String, Any])
val my_data = List(
    Record0(
        name = "one",
        payload = Map[String, Any](
            "scalar" -> 1,
            "empty" -> Set(),
            "mixed" -> Set(
                2,
                "word",
            ),
        ),
    ),
    Record0(
        name = "two",
        payload = Map[String, Any](
            "other" -> 2,
        ),
    ),
)
}
