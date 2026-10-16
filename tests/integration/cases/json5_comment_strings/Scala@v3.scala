object Fixture_json5_comment_strings_Scala {
val my_data = List[String](
    // strings stay data
    "https://example.org/a/*b*/",  // URL annotation
    "escaped quote: \" // still data",
    "backslash: \\",  // outside the string
    "/* not a comment */",
)
}
