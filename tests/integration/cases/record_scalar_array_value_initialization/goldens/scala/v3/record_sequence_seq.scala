object Fixture_record_scalar_array_value_initialization_Scala_record_sequence_seq {
case class Record0(numbers: Seq[Any], nested_numbers: Seq[Any], words: Seq[Any], flag: Boolean)
val my_data = Record0(
    numbers = Seq(
        1,
        2,
    ),
    nested_numbers = Seq(
        Seq(
            3,
            4,
        ),
        Seq(
            5,
            6,
        ),
    ),
    words = Seq(
        "s",
    ),
    flag = true,
)
}
