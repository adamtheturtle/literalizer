object Declaration {
  val my_data = List[AnyRef](
      42,
      3.14,
      true,
      false,
      "hello \"world\"",
  )
}
object Assignment {
  var my_data: Any = null
  my_data = List[AnyRef](
      42,
      3.14,
      true,
      false,
      "hello \"world\"",
  )
}
