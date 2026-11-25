import scala.collection.immutable.ListMap
object Fixture_toml_nested_comments_Scala_dict_format_list_map {
val my_data = ListMap(
    // About the first dotted key.
    // About the second dotted key.
    "dotted" -> ListMap[String, Int]("first" -> 1, "second" -> 2),
    "plain" -> 3,  // About the plain key.
    // Before the first entry.
    // Before the second entry.
    "entries" -> List[Map[String, String]](ListMap[String, String]("name" -> "one"), ListMap[String, String]("name" -> "two")),
    // Inside the table.
    "table" -> ListMap[String, Int]("inner" -> 4),
)
}
