object Fixture_cpp_record_in_variant_Scala_heterogeneous_strategy_record {
case class Record1(k: List[Boolean])
case class Record0(h: List[Any])
val my_data = Record0(
    h = List(
        1,
        "a",
        List(
            2,
            "b",
        ),
        Record1(
            k = List[Boolean](
                true,
            ),
        ),
    ),
)
}
