object Declaration {
  val my_data = Map(
      "a" -> Map[String, Int]("x" -> 1),
      "b" -> 2,
  )
}
object Assignment {
  var my_data: Any = null
  my_data = Map(
      "a" -> Map[String, Int]("x" -> 1),
      "b" -> 2,
  )
}
