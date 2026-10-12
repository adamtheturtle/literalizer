object Fixture_kotlin_record_primitive_arrays_Scala_heterogeneous_strategy_record {
case class Record0(flags: List[Boolean], values: List[Double], ints: List[Int], text: List[String], nested_flags: List[List[Boolean]], nested_values: List[List[Double]])
val my_data = Record0(
    flags = List[Boolean](
        true,
        false,
    ),
    values = List[Double](
        1.5,
        -2.25,
    ),
    ints = List[Int](
        1,
        2,
    ),
    text = List[String](
        "a",
    ),
    nested_flags = List[List[Boolean]](
        List[Boolean](
            true,
        ),
        List[Boolean](
            false,
        ),
    ),
    nested_values = List[List[Double]](
        List[Double](
            1.5,
        ),
        List[Double](
            2.25,
        ),
    ),
)
}
