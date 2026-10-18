import scala.collection.immutable.ListMap
object Fixture_roc_native_record_list_Scala_dict_format_list_map {
val my_data = List[Map[String, Any]](
    ListMap("name" -> "Ada", "active" -> true, "count" -> 1, "score" -> 1.5, "missing" -> null, "scores" -> List[Int](1, 2), "child" -> ListMap[String, Int]("age" -> 3)),
    ListMap("name" -> "Bob", "active" -> false, "count" -> 2, "score" -> 2.5, "missing" -> null, "scores" -> List[Int](4), "child" -> ListMap[String, Int]("age" -> 5)),
)
}
