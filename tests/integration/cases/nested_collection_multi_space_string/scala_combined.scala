object Declaration {
  val my_data = List[AnyRef](
      Map[String, AnyRef]("key" -> "hello   world", "value" -> 1),
  )
}
object Assignment {
  var my_data: Any = null
  my_data = List[AnyRef](
      Map[String, AnyRef]("key" -> "hello   world", "value" -> 1),
  )
}
