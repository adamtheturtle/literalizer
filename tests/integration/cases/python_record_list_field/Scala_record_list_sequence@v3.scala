object Fixture_python_record_list_field_Scala_record_list_sequence {
case class Record1(a: Int)
case class Record0(items: List[Any])
val my_data = Record0(
    items = List(
        Record1(
            a = 1,
        ),
    ),
)
}
