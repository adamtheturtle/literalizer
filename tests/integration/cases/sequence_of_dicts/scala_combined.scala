object Declaration {
  val my_data = List[AnyRef](
      Map[String, AnyRef]("name" -> "Alice", "age" -> 30),
      Map[String, AnyRef]("name" -> "Bob", "age" -> 25),
  )
}
object Assignment {
  var my_data: Any = null
  my_data = List[AnyRef](
      Map[String, AnyRef]("name" -> "Alice", "age" -> 30),
      Map[String, AnyRef]("name" -> "Bob", "age" -> 25),
  )
}
