object Fixture_cpp_mixed_sibling_maps_Scala {
val my_data = List(
    List(Map("a" -> 1), Map("a" -> null), 42),
    List(Map("a" -> 1), Map("a" -> "s"), 42),
    List[Map[String, Any]](Map("a" -> 1), Map("a" -> null)),
    List[Map[String, Any]](Map("a" -> 1), Map("a" -> "s")),
)
}
