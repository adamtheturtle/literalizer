object Fixture_escaped_mapping_keys_Scala_type_hints_safe {
val my_data = Map[String, Int](
    "quote\"backslash\\" -> 1,
    "line\nbreak" -> 2,
    "$(literal)${text}" -> 3,
    "RStr prefix" -> 4,
)
}
