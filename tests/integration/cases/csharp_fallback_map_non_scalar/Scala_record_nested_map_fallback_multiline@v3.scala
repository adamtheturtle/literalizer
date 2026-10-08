object Fixture_csharp_fallback_map_non_scalar_Scala_record_nested_map_fallback_multiline {
case class Record0(name: String, payload: Map[String, Any])
val my_data = List(
    Record0(
        name = "one",
        payload = Map[String, Any](
            "scalar" -> 1,
            "items" -> List[Int](
                2,
                3,
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
