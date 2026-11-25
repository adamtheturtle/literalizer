object Fixture_record_wide_int_Scala_heterogeneous_strategy_record_separator_underscore {
case class Record0(quantity: Int, big: BigInt, ratio: Double, label: String, ok: Boolean)
val my_data = Record0(
    quantity = 1_000_000,
    big = BigInt("18446744073709551615"),
    ratio = 2.5,
    label = "tag",
    ok = true,
)
}
