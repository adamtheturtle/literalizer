object Fixture_record_tuple_integer_widths_Scala_record_sequence_seq {
case class Record0(narrow_pair: Seq[Any], wide_pair: Seq[Any], wide_triple: Seq[Any], beyond_pair: Seq[Any], beyond_triple: Seq[Any], mixed_triple: Seq[Any])
val my_data = Record0(
    narrow_pair = Seq(
        1,
        2,
    ),
    wide_pair = Seq(
        1,
        1099511627776L,
    ),
    wide_triple = Seq(
        1,
        2,
        1099511627776L,
    ),
    beyond_pair = Seq(
        BigInt("1"),
        BigInt("18446744073709551616"),
    ),
    beyond_triple = Seq(
        BigInt("1"),
        BigInt("2"),
        BigInt("18446744073709551616"),
    ),
    mixed_triple = Seq(
        1,
        "text",
        true,
    ),
)
}
