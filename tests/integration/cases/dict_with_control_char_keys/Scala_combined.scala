object Fixture_dict_with_control_char_keys_Scala_combined {
var my_data = Map[String, String](
    "key\nwith\nnewlines" -> "value1",
    "key\twith\ttabs" -> "value2",
    "" -> "value3",
)
my_data = Map[String, String](
    "key\nwith\nnewlines" -> "value1",
    "key\twith\ttabs" -> "value2",
    "" -> "value3",
)
}
