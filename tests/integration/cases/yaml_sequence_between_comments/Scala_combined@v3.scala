object Fixture_yaml_sequence_between_comments_Scala_combined {
var my_data = List[Map[String, String]](
    Map[String, String]("item" -> "existing"),
    // This comment describes the next item.
    Map[String, String]("item" -> "next"),
)
my_data = List[Map[String, String]](
    Map[String, String]("item" -> "existing"),
    // This comment describes the next item.
    Map[String, String]("item" -> "next"),
)
}
