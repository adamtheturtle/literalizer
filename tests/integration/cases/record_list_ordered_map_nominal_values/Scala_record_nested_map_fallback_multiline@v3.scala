object Fixture_record_list_ordered_map_nominal_values_Scala_record_nested_map_fallback_multiline {
case class Record1(x: Int)
case class Record0(values: List[Any], flag: Boolean)
val my_data = Record0(
    values = List(
        scala.collection.immutable.ListMap(
            "inner" -> Record1(
                x = 1,
            ),
        ),
        scala.collection.immutable.ListMap(
            "inner" -> Record1(
                x = 2,
            ),
        ),
    ),
    flag = true,
)
}
