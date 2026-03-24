object Declaration {
  val my_data = Map[String, String](
      "key" -> "\"bang!\"",  // real
  )
}
object Assignment {
  var my_data: Any = null
  my_data = Map[String, String](
      "key" -> "\"bang!\"",  // real
  )
}
