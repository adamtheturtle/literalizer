object Fixture_record_primitive_sequence_fields_Scala_record_sequence_seq {
case class Record0(flags: Seq[Any], values: Seq[Any], ints: Seq[Any], text: Seq[Any], nested_flags: Seq[Any], nested_values: Seq[Any])
val my_data = Record0(
    flags = Seq(
        true,
        false,
    ),
    values = Seq(
        1.5,
        -2.25,
    ),
    ints = Seq(
        1,
        2,
    ),
    text = Seq(
        "a",
    ),
    nested_flags = Seq(
        Seq(
            true,
        ),
        Seq(
            false,
        ),
    ),
    nested_values = Seq(
        Seq(
            1.5,
        ),
        Seq(
            2.25,
        ),
    ),
)
}
