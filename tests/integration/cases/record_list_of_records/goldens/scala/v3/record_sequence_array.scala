object Fixture_record_list_of_records_Scala_record_sequence_array {
case class Record1(id: Int, label: String)
case class Record0(name: String, items: Array[Any])
val my_data = Record0(
    name = "box",
    items = Array(
        Record1(
            id = 1,
            label = "first",
        ),
        Record1(
            id = 2,
            label = "second",
        ),
    ),
)
}
