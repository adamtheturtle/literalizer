object Fixture_json5_comment_lexemes_Scala {
val my_data = Map[String, String](
    // heading
    "a" -> "single ' // data",
    "b" -> "linecontinuation",
    "c" -> "\\",  // actual comment
    "d" -> "  ",  // final comment
)
}
