object Fixture_literalize_ref_nested_escaped_key_Scala_ref {
val foo = Map[String, String](
    "_" -> "_",
)
val my_data = Map(
    "mapping" -> Map("value" -> foo),
    "items" -> List[Map[String, Int]](Map("other" -> 1), foo),
)
}
