object Fixture_tuple_record_sequence_Scala_heterogeneous_strategy_record {
case class Record0(call: String, args: List[Any])
val my_data = List(
    Record0(call = "send", args = List(1, "email", "a@gmail.com", 100)),
    Record0(call = "recv", args = List(2, "sms", "b@example.com", 200)),
)
}
