object Fixture_record_sequence_mixture_controls_Scala_record_sequence_seq {
case class Record0(x: Int)
val my_data = Seq(
    Seq(Seq(1), Record0(x = 1)),
    Seq(Record0(x = 1), Record0(x = 2)),
    Seq(Seq(), Seq(Record0(x = 1))),
    Seq(Seq(), Seq()),
)
}
