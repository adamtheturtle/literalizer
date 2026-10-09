object Fixture_python_ordered_map_multiline_whitespace_Scala_string_format_multiline_list {
val my_data = scala.collection.immutable.ListMap(
    """  leading
key  """ -> """  leading
value
  """,
    """next
	key""" -> List[String]("""
first
""", """ last
 """),
)
}
