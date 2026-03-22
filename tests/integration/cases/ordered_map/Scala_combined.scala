object Declaration {
  val my_data = scala.collection.immutable.ListMap(
      "name" -> "Alice",
      "age" -> 30,
      "active" -> true,
  )
}
object Assignment {
  var my_data: Any = null
  my_data = scala.collection.immutable.ListMap(
      "name" -> "Alice",
      "age" -> 30,
      "active" -> true,
  )
}
