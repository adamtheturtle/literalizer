object Declaration {
  val my_data = Map[String, AnyRef](
      "level1" -> Map[String, AnyRef]("level2" -> Map[String, AnyRef]("level3" -> Map[String, AnyRef]("level4" -> Map[String, AnyRef]("value" -> "deep", "items" -> Array[String]("a", "b"))), "sibling" -> 42), "tags" -> List[AnyRef](Map[String, AnyRef]("name" -> "tag1", "meta" -> Map[String, AnyRef]("priority" -> 1, "labels" -> Array[String]("x", "y"))))),
  )
}
object Assignment {
  var my_data: Any = null
  my_data = Map[String, AnyRef](
      "level1" -> Map[String, AnyRef]("level2" -> Map[String, AnyRef]("level3" -> Map[String, AnyRef]("level4" -> Map[String, AnyRef]("value" -> "deep", "items" -> Array[String]("a", "b"))), "sibling" -> 42), "tags" -> List[AnyRef](Map[String, AnyRef]("name" -> "tag1", "meta" -> Map[String, AnyRef]("priority" -> 1, "labels" -> Array[String]("x", "y"))))),
  )
}
