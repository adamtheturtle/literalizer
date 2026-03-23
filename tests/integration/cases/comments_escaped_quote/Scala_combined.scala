object Declaration {
  val my_data = Map[String, String](
      "key" -> "value \" # not a comment",  // real
  )
}
object Assignment {
  var my_data: Any = null
  my_data = Map[String, String](
      "key" -> "value \" # not a comment",  // real
  )
}
