object Fixture_nested_mixed_dict_Scala_heterogeneous_strategy_record {
case class Record1(a: Int, b: String, c: Any)
case class Record0(outer: Record1)
val my_data = Record0(
    outer = Record1(
        a = 1,
        b = "x",
        c = null,
    ),
)
}
