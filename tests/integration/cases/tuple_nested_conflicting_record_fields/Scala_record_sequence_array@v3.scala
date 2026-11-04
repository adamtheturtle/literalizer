object Fixture_tuple_nested_conflicting_record_fields_Scala_record_sequence_array {
case class Record1(pair: Array[Any])
case class Record0(outer: Record1)
val my_data = Array(
    Record0(outer = Record1(pair = Array[Any](1, "first"))),
    Record0(outer = Record1(pair = Array[Any](false, "second"))),
)
}
