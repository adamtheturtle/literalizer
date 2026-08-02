object Fixture_multiline_string_nested_Scala_string_format_multiline_nested {
val my_data = Map[String, List[List[String]]](
    """outer""" -> List[List[String]](List[String]("""nested first line
  indented

nested last line
""")),
)
}
