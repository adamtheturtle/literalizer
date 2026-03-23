object Declaration {
  val my_data = Map(
      "users" -> List(Map("name" -> "Bob", "tags" -> List[String]("admin", "user")), Map("name" -> "Carol", "tags" -> List[String]("guest"))),
  )
}
object Assignment {
  var my_data: Any = null
  my_data = Map(
      "users" -> List(Map("name" -> "Bob", "tags" -> List[String]("admin", "user")), Map("name" -> "Carol", "tags" -> List[String]("guest"))),
  )
}
