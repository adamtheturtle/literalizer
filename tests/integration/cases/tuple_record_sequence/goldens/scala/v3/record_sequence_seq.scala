object Fixture_tuple_record_sequence_Scala_record_sequence_seq {
case class Record0(call: String, args: Seq[Any])
val my_data = Seq(
    Record0(call = "send", args = Seq(1, "email", "a@gmail.com", 100)),
    Record0(call = "recv", args = Seq(2, "sms", "b@example.com", 200)),
)
}
