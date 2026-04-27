object Fixture_comments_escaped_quote_scala_combined {
var my_data = Map[String, String](
    "key" -> "value \" # not a comment",  // real
)
my_data = Map[String, String](
    "key" -> "value \" # not a comment",  // real
)
}
