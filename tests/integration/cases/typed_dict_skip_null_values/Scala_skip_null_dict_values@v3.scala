object Fixture_typed_dict_skip_null_values_Scala_skip_null_dict_values {
val my_data = Map(
    "divergent" -> List[Map[String, Any]](Map("b" -> 1), Map("a" -> "hello")),
    "matching" -> List[Map[String, Any]](Map[String, Int]("n" -> 1), Map[String, Int]("n" -> 2)),
)
}
