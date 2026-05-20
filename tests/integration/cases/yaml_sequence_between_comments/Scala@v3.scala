object Fixture_yaml_sequence_between_comments_Scala {
val my_data = List[Map[String, String]](
    Map[String, String]("item" -> "existing"),
    // This comment describes the next item.
    Map[String, String]("item" -> "next"),
)
}
