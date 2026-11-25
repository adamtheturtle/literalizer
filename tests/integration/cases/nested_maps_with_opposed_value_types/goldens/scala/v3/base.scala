object Fixture_nested_maps_with_opposed_value_types_Scala {
val my_data = List[Map[String, Map[String, Any]]](
    Map("input" -> Map("name" -> "alice", "city" -> "paris"), "expected" -> Map("count" -> 1, "total" -> 2)),
    Map("input" -> Map("name" -> 10, "city" -> 20), "expected" -> Map("count" -> "done", "total" -> "pending")),
)
}
