object Fixture_deep_nesting_Scala {
val my_data = Map(
    "level1" -> Map("level2" -> Map("level3" -> Map("level4" -> Map("value" -> "deep", "items" -> List[String]("a", "b"))), "sibling" -> 42), "tags" -> List[Map[String, Any]](Map("name" -> "tag1", "meta" -> Map("priority" -> 1, "labels" -> List[String]("x", "y"))))),
)
}
