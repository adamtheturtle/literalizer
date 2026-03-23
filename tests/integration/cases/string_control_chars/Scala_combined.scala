object Declaration {
  val my_data = Array[String](
      "line1\r\nline2",
      "line1\rline2",
      "",
  )
}
object Assignment {
  var my_data: Any = null
  my_data = Array[String](
      "line1\r\nline2",
      "line1\rline2",
      "",
  )
}
