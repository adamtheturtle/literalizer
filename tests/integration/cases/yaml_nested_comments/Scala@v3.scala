object Fixture_yaml_nested_comments_Scala {
val my_data = Map(
    "a" -> Map[String, Int](
        // inner note
        "b" -> 1,  // inline b
    ),
    "list" -> List[Int](
        1,  // first
        2,  // second
    ),
)
}
