object Fixture_mixed_nested_collection_types_Scala {
val my_data = Map(
    "lists" -> List(List[Int](1), List[String]("x"), List()),
    "maps" -> List(Map("x" -> 1), Map("x" -> "s")),
    "empties" -> Map[String, List[Int]]("a" -> List[Int](1), "b" -> List[Int]()),
)
}
