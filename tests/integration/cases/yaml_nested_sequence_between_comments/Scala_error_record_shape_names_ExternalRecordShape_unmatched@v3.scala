object Fixture_yaml_nested_sequence_between_comments_Scala_error_record_shape_names_ExternalRecordShape_unmatched {
val my_data = List(
    List(
        Map[String, String]("item" -> "existing"),
        "kept",
        // This comment trails the first pair.
    ),
    List(Map[String, String]("item" -> "next"), "also kept"),
    // This comment describes the last pair.
    List(Map[String, String]("item" -> "last"), "kept too"),
)
}
