object Declaration {
  val my_data = Map[String, String](
      "key\nwith\nnewlines" -> "value1",
      "key\twith\ttabs" -> "value2",
      "" -> "value3",
  )
}
object Assignment {
  var my_data: Any = null
  my_data = Map[String, String](
      "key\nwith\nnewlines" -> "value1",
      "key\twith\ttabs" -> "value2",
      "" -> "value3",
  )
}
