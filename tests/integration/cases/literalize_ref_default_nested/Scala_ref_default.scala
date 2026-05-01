object Fixture_literalize_ref_default_nested_Scala_ref_default {
val my_var = Map[String, String](
    "_" -> "_",
)
val item_var = Map[String, String](
    "_" -> "_",
)
val my_data = Map(
    "key" -> my_var,
    "items" -> List[Map[String, String]](item_var, Map[String, String]("fallback" -> "value")),
)
}
