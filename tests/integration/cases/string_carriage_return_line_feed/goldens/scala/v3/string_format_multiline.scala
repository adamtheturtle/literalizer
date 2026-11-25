object Fixture_string_carriage_return_line_feed_Scala_string_format_multiline {
val my_data = Map[String, String](
    """cr""" -> "a\rb",
    """crlf""" -> "a\r\nb",
    """lf""" -> """a
b""",
)
}
