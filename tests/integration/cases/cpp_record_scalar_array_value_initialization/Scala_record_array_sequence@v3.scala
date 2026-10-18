object Fixture_cpp_record_scalar_array_value_initialization_Scala_record_array_sequence {
case class Record0(numbers: Array[Int], nested_numbers: Array[Array[Int]], words: Array[String], flag: Boolean)
val my_data = Record0(
    numbers = Array[Int](
        1,
        2,
    ),
    nested_numbers = Array[Array[Int]](
        Array[Int](
            3,
            4,
        ),
        Array[Int](
            5,
            6,
        ),
    ),
    words = Array[String](
        "s",
    ),
    flag = true,
)
}
