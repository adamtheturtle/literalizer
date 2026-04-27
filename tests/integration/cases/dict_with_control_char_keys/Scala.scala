object Fixture_dict_with_control_char_keys_scala {
val my_data = Map[String, String](
    "key\nwith\nnewlines" -> "value1",
    "key\twith\ttabs" -> "value2",
    "" -> "value3",
)
}
