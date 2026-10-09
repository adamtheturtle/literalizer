object Fixture_v_record_ordered_map_epoch_Scala_record_epoch_i32_overflow {
case class Record0(values: scala.collection.immutable.ListMap[String, Any], flag: Boolean, nested_values: scala.collection.immutable.ListMap[String, Any], list_values: scala.collection.immutable.ListMap[String, Any])
val my_data = Record0(
    values = scala.collection.immutable.ListMap(
        "first" -> 2208988800L,
    ),
    flag = true,
    nested_values = scala.collection.immutable.ListMap(
        "first" -> scala.collection.immutable.ListMap(
            "nested" -> 2208988800L,
        ),
    ),
    list_values = scala.collection.immutable.ListMap(
        "first" -> List[Long](
            2208988800L,
        ),
    ),
)
}
