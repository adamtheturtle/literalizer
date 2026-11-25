object Fixture_record_tuple_integer_widths_Scala_record_sequence_array {
case class Record0(narrow_pair: Array[Int], wide_pair: Array[Long], wide_triple: Array[Long], beyond_pair: Array[BigInt], beyond_triple: Array[BigInt], mixed_triple: Array[Any])
val my_data = Record0(
    narrow_pair = Array[Int](
        1,
        2,
    ),
    wide_pair = Array[Long](
        1,
        1099511627776L,
    ),
    wide_triple = Array[Long](
        1,
        2,
        1099511627776L,
    ),
    beyond_pair = Array[BigInt](
        BigInt("1"),
        BigInt("18446744073709551616"),
    ),
    beyond_triple = Array[BigInt](
        BigInt("1"),
        BigInt("2"),
        BigInt("18446744073709551616"),
    ),
    mixed_triple = Array[Any](
        1,
        "text",
        true,
    ),
)
}
