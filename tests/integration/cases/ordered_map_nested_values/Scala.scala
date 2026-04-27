object Fixture_ordered_map_nested_values_scala {
val my_data = scala.collection.immutable.ListMap(
    "name" -> "Alice",
    "scores" -> Map[String, String]("1" -> "first", "2" -> "second"),
)
}
