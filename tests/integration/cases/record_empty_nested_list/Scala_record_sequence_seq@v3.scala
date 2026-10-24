object Fixture_record_empty_nested_list_Scala_record_sequence_seq {
case class Record0(a: Seq[Any], b: Seq[Any])
val my_data = Record0(
    a = Seq(
        Seq(
            1,
            2,
        ),
        Seq(
            3,
        ),
    ),
    b = Seq(
        Seq(),
        Seq(
            1,
        ),
    ),
)
}
