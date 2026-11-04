object Fixture_tuple_nested_conflicting_record_fields_Scala_record_sequence_seq {
case class Record1(pair: Seq[Any])
case class Record0(outer: Record1)
val my_data = Seq(
    Record0(outer = Record1(pair = Seq(1, "first"))),
    Record0(outer = Record1(pair = Seq(false, "second"))),
)
}
