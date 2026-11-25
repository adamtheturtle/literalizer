object Fixture_record_primitive_sequence_fields_Scala_record_sequence_array {
case class Record0(flags: Array[Boolean], values: Array[Double], ints: Array[Int], text: Array[String], nested_flags: Array[Array[Boolean]], nested_values: Array[Array[Double]])
val my_data = Record0(
    flags = Array[Boolean](
        true,
        false,
    ),
    values = Array[Double](
        1.5,
        -2.25,
    ),
    ints = Array[Int](
        1,
        2,
    ),
    text = Array[String](
        "a",
    ),
    nested_flags = Array[Array[Boolean]](
        Array[Boolean](
            true,
        ),
        Array[Boolean](
            false,
        ),
    ),
    nested_values = Array[Array[Double]](
        Array[Double](
            1.5,
        ),
        Array[Double](
            2.25,
        ),
    ),
)
}
