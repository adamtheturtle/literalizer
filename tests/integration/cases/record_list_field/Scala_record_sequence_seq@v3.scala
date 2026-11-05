object Fixture_record_list_field_Scala_record_sequence_seq {
case class Record1(a: Int)
case class Record0(items: Seq[Any])
val my_data = Record0(
    items = Seq(
        Record1(
            a = 1,
        ),
    ),
)
}
