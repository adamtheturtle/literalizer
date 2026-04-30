object Fixture_call_ref_nested_in_list_Scala {
val my_data = List(
    List(List(Map[String, String]("$ref" -> "my_var"), 42, "static")),
    List(List(Map[String, String]("$ref" -> "my_other"), 7, "label")),
)
}
