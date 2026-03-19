object Declaration {
  val my_data = List[AnyRef](
      List[AnyRef](1, "a"),
      List[AnyRef](2, "b"),
  )
}
object Assignment {
  var my_data: Any = null
  my_data = List[AnyRef](
      List[AnyRef](1, "a"),
      List[AnyRef](2, "b"),
  )
}
