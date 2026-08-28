object Fixture_toml_nested_comments_Scala {
val my_data = Map(
    // About the first dotted key.
    // About the second dotted key.
    "dotted" -> Map[String, Int]("first" -> 1, "second" -> 2),
    "plain" -> 3,  // About the plain key.
    // Inside the table.
    "table" -> Map[String, Int]("inner" -> 4),
    // Before the first entry.
    // Before the second entry.
    "entries" -> List[Map[String, String]](Map[String, String]("name" -> "one"), Map[String, String]("name" -> "two")),
)
}
