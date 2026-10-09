object Fixture_v_record_ordered_map_fields_Scala_heterogeneous_strategy_record {
case class Record0(numbers: scala.collection.immutable.ListMap[String, Any], words: scala.collection.immutable.ListMap[String, Any], nested: scala.collection.immutable.ListMap[String, Any], empty: scala.collection.immutable.ListMap[String, Any], flag: Boolean, nested_maps: scala.collection.immutable.ListMap[String, Any], empty_nested_maps: scala.collection.immutable.ListMap[String, Any])
val my_data = Record0(
    numbers = scala.collection.immutable.ListMap(
        "first" -> 1,
    ),
    words = scala.collection.immutable.ListMap(
        "first" -> "s",
    ),
    nested = scala.collection.immutable.ListMap(
        "first" -> List[Int](
            1,
            2,
        ),
    ),
    empty = scala.collection.immutable.ListMap(),
    flag = true,
    nested_maps = scala.collection.immutable.ListMap(
        "first" -> scala.collection.immutable.ListMap(
            "nested" -> 1,
        ),
    ),
    empty_nested_maps = scala.collection.immutable.ListMap(
        "first" -> scala.collection.immutable.ListMap(),
    ),
)
}
