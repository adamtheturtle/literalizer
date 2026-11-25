object Fixture_deep_list_cousin_empty_map_Scala {
val my_data = List[Map[String, List[Map[String, Map[String, Int]]]]](
    Map("items" -> List[Map[String, Map[String, Int]]](Map("inner" -> Map[String, Int]("x" -> 1)), Map("inner" -> Map[String, Int]()))),
    Map("items" -> List[Map[String, Map[String, Int]]](Map("inner" -> Map[String, Int]("x" -> 2)), Map("inner" -> Map[String, Int]()))),
)
}
