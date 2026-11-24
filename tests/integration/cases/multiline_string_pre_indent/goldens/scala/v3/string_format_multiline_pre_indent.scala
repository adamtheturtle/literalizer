object Fixture_multiline_string_pre_indent_Scala_string_format_multiline_pre_indent {

    def main(args: Array[String]): Unit = {
    val my_data = """
first line
  indented

last line
"""
        assert(my_data == "\nfirst line\n  indented\n\nlast line\n")
    }
}
