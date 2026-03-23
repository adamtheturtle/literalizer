object Check {
val x: Any = Map[String, String](
    "key" -> "value \" # not a comment",  // real
)
}
