object Fixture_literalize_ref_nul_string_value_Scala_ref {
val shared = "a\u0000b"
val my_data = Map[String, String](
    "value" -> shared,
)
}
