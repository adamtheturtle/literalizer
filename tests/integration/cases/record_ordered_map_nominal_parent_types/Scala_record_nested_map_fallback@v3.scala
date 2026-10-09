object Fixture_record_ordered_map_nominal_parent_types_Scala_record_nested_map_fallback {
case class Record2(x: Int)
case class Record1(values: scala.collection.immutable.ListMap[String, Any], flag: Boolean)
case class Record3(y: String)
case class Record0(first: Record1, second: Record1)
val my_data = Record0(
    first = Record1(
        values = scala.collection.immutable.ListMap(
            "item" -> Record2(
                x = 1,
            ),
        ),
        flag = true,
    ),
    second = Record1(
        values = scala.collection.immutable.ListMap(
            "item" -> Record3(
                y = "s",
            ),
        ),
        flag = false,
    ),
)
}
