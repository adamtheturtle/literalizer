object Fixture_tuple_record_field_Scala_heterogeneous_strategy_tuple {
case class Record0(call: String, args: (Int, String, String, Int))
val my_data = Record0(
    call = "send",
    args = (
        1,
        "email",
        "a@gmail.com",
        100,
    ),
)
}
