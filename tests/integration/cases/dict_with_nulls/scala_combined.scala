object Declaration {
  val my_data = Map[String, AnyRef](
      "name" -> "Alice",
      "score" -> null,
      "age" -> 30,
  )
}
object Assignment {
  var my_data: Any = null
  my_data = Map[String, AnyRef](
      "name" -> "Alice",
      "score" -> null,
      "age" -> 30,
  )
}
