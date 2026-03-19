object Declaration {
  val my_data = Map[String, AnyRef](
      "name" -> "Alice",
      "age" -> 30,
      "active" -> true,
      "score" -> null,
  )
}
object Assignment {
  var my_data: Any = null
  my_data = Map[String, AnyRef](
      "name" -> "Alice",
      "age" -> 30,
      "active" -> true,
      "score" -> null,
  )
}
