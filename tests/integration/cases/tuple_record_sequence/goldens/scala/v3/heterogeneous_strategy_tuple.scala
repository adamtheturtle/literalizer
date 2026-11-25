object Fixture_tuple_record_sequence_Scala_heterogeneous_strategy_tuple {
case class Record0(call: String, args: (Int, String, String, Int))
val my_data = List(
    Record0(call = "send", args = (1, "email", "a@gmail.com", 100)),
    Record0(call = "recv", args = (2, "sms", "b@example.com", 200)),
)
}
