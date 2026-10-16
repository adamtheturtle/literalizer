object Fixture_csharp_record_sequence_mixture_controls_Scala_heterogeneous_strategy_record {
case class Record0(x: Int)
val my_data = List(
    List(List[Int](1), Record0(x = 1)),
    List(Record0(x = 1), Record0(x = 2)),
    List[List[Map[String, Int]]](List(), List(Record0(x = 1))),
    List(List(), List()),
)
}
