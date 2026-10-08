import scala.collection.immutable.ListMap
object Fixture_opt_in_record_nested_Scala_dict_format_list_map {
val my_data = ListMap(
    "owner" -> ListMap("name" -> "Ada", "active" -> false),
    "members" -> List[Map[String, Any]](ListMap("name" -> "Ada", "score" -> 1.5), ListMap("name" -> "Bob", "score" -> 2.5)),
)
}
