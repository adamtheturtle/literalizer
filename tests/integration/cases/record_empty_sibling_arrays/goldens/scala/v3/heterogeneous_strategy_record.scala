object Fixture_record_empty_sibling_arrays_Scala_heterogeneous_strategy_record {
case class Record1(item: Int)
case class Record2(item: Any)
case class Record0(integers: List[Any], nulls: List[Any], nested: List[Any], reversed: List[Any])
val my_data = Record0(
    integers = List(
        List(),
        List(
            Record1(
                item = 1,
            ),
        ),
    ),
    nulls = List(
        List(),
        List(
            Record2(
                item = null,
            ),
        ),
    ),
    nested = List(
        List(
            List(),
            List(
                Record1(
                    item = 2,
                ),
            ),
        ),
        List(
            List(
                Record1(
                    item = 3,
                ),
            ),
            List(),
        ),
    ),
    reversed = List(
        List(
            Record1(
                item = 4,
            ),
        ),
        List(),
    ),
)
}
