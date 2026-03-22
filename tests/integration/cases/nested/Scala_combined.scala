object Declaration {
  val my_data = Map(
      "users" -> List(Map("name" -> "Bob", "tags" -> Array[String]("admin", "user")), Map("name" -> "Carol", "tags" -> Array[String]("guest"))),
  )
}
object Assignment {
  var my_data: Any = null
  my_data = Map(
      "users" -> List(Map("name" -> "Bob", "tags" -> Array[String]("admin", "user")), Map("name" -> "Carol", "tags" -> Array[String]("guest"))),
  )
}
