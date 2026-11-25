object Fixture_tuple_conflicting_record_fields_Scala_record_sequence_seq {
case class Record0(a: Seq[Any])
val my_data = Seq(
    Record0(a = Seq(1, "x")),
    Record0(a = Seq(2, 3)),
)
}
