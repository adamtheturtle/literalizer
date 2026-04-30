object Fixture_literalize_ref_deep_nesting_Scala {
val my_data = Map(
    "a" -> Map("b" -> Map("c" -> Map[String, String]("$ref" -> "deep"))),
)
}
