object Fixture_deep_cousin_empty_map_Scala {
val my_data = List[Map[String, Map[String, Map[String, Int]]]](
    Map("outer" -> Map("inner" -> Map[String, Int]("x" -> 1))),
    Map("outer" -> Map("inner" -> Map())),
)
}
