object Declaration {
  val my_data = List[AnyRef](
      Array[Int](1, 2),
      Array[String]("a", "b"),
  )
}
object Assignment {
  var my_data: Any = null
  my_data = List[AnyRef](
      Array[Int](1, 2),
      Array[String]("a", "b"),
  )
}
