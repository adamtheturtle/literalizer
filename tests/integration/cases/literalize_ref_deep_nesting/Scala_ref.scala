object Fixture_literalize_ref_deep_nesting_Scala_ref {
val deep = Map[String, String](
    "_" -> "_",
)
val my_data = Map(
    "a" -> Map("b" -> Map("c" -> deep)),
)
}
