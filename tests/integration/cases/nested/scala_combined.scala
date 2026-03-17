object Declaration {
  val my_data = Map(
      "users" -> List(Map("name" -> "Bob", "tags" -> List("admin", "user")), Map("name" -> "Carol", "tags" -> List("guest"))),
  )
}
object Assignment {
  var my_data: Any = null
  my_data = Map(
      "users" -> List(Map("name" -> "Bob", "tags" -> List("admin", "user")), Map("name" -> "Carol", "tags" -> List("guest"))),
  )
}
