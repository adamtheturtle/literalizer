object Declaration {
  val my_data = List(
      Map("name" -> "Alice", "age" -> 30),
      Map("name" -> "Bob", "age" -> 25),
  )
}
object Assignment {
  var my_data: Any = null
  my_data = List(
      Map("name" -> "Alice", "age" -> 30),
      Map("name" -> "Bob", "age" -> 25),
  )
}
