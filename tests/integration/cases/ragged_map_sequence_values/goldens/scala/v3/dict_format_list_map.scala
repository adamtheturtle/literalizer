import scala.collection.immutable.ListMap
object Fixture_ragged_map_sequence_values_Scala_dict_format_list_map {
val my_data = ListMap(
    "a" -> List[Map[String, List[Int]]](ListMap[String, List[Int]]("item" -> List[Int](1))),
    "b" -> List[Map[String, List[Int]]](ListMap[String, List[Int]]("item" -> List[Int](2, 3))),
)
}
