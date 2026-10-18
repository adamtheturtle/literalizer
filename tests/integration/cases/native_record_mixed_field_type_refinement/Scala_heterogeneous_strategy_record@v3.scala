object Fixture_native_record_mixed_field_type_refinement_Scala_heterogeneous_strategy_record {
case class Record2(value: Int)
case class Record1(items: List[Any])
case class Record3(value: String)
case class Record0(first: Record1, second: Record1)
val my_data = Record0(
    first = Record1(
        items = List(
            1,
            Record2(
                value = 2,
            ),
        ),
    ),
    second = Record1(
        items = List(
            1,
            Record3(
                value = "s",
            ),
        ),
    ),
)
}
