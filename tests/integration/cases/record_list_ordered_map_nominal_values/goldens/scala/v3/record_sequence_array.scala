object Fixture_record_list_ordered_map_nominal_values_Scala_record_sequence_array {
case class Record1(x: Int)
case class Record0(values: Array[Any], flag: Boolean)
val my_data = Record0(
    values = Array[Any](
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
