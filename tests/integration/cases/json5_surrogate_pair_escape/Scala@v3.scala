object Fixture_json5_surrogate_pair_escape_Scala {
val my_data = Map(
    "astral" -> "😀",
    "mixed" -> "a😀b",
    "count" -> 2,
    "list" -> List("😀", 1),
    "nested" -> Map[String, String]("inner" -> "😀"),
)
}
