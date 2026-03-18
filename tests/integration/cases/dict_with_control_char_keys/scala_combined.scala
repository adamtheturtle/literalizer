object Declaration {
  val my_data = Map(
      "key\nwith\nnewlines" -> "value1",
      "key	with	tabs" -> "value2",
  )
}
object Assignment {
  var my_data: Any = null
  my_data = Map(
      "key\nwith\nnewlines" -> "value1",
      "key	with	tabs" -> "value2",
  )
}
