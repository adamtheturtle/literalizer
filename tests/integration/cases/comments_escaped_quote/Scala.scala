object Check {
val my_data: Any = Map[String, String](
    "key" -> "value \" # not a comment",  // real
)
}
