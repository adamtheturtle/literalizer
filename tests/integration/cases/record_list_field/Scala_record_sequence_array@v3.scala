object Fixture_record_list_field_Scala_record_sequence_array {
case class Record1(a: Int)
case class Record0(items: Array[Any])
val my_data = Record0(
    items = Array(
        Record1(
            a = 1,
        ),
    ),
)
}
