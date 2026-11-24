object Fixture_mixed_sibling_maps_Scala_sequence_array {
val my_data = Array[Any](
    Array[Any](Map("a" -> 1), Map("a" -> null), 42),
    Array[Any](Map("a" -> 1), Map("a" -> "s"), 42),
    Array[Map[String, Any]](Map("a" -> 1), Map("a" -> null)),
    Array[Map[String, Any]](Map("a" -> 1), Map("a" -> "s")),
)
}
