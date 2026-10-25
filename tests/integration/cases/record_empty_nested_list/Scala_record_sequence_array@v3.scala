object Fixture_record_empty_nested_list_Scala_record_sequence_array {
case class Record0(a: Array[Array[Int]], b: Array[Array[Int]])
val my_data = Record0(
    a = Array[Array[Int]](
        Array[Int](
            1,
            2,
        ),
        Array[Int](
            3,
        ),
    ),
    b = Array[Array[Int]](
        Array.empty[Int],
        Array[Int](
            1,
        ),
    ),
)
}
