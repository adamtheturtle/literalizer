object Fixture_inconsistent_string_dict_shapes_in_seq_Scala_combined {
var my_data = List[Map[String, String]](
    Map[String, String]("first" -> "Alice", "last" -> "Smith"),
    Map[String, String]("first" -> "Bob", "middle" -> "Quincy"),
)
my_data = List[Map[String, String]](
    Map[String, String]("first" -> "Alice", "last" -> "Smith"),
    Map[String, String]("first" -> "Bob", "middle" -> "Quincy"),
)
}
