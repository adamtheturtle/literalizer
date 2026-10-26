object Fixture_nested_numeric_and_mixed_sequences_Scala {
val my_data = Map(
    "numbers" -> List(1, 2),
    "nested" -> Map[String, List[Int]]("inner" -> List[Int](3)),
    "mixed" -> List(4, "five"),
)
}
