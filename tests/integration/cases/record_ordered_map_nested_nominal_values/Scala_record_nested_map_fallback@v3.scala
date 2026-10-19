object Fixture_record_ordered_map_nested_nominal_values_Scala_record_nested_map_fallback {
case class Record1(x: Int)
case class Record0(values: scala.collection.immutable.ListMap[String, Any], flag: Boolean)
val my_data = Record0(
    values = scala.collection.immutable.ListMap(
        "outer" -> scala.collection.immutable.ListMap(
            "inner" -> Record1(
                x = 1,
            ),
        ),
    ),
    flag = true,
)
}
