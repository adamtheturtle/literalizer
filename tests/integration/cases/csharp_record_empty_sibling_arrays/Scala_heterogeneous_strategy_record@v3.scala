object Fixture_csharp_record_empty_sibling_arrays_Scala_heterogeneous_strategy_record {
case class Record1(item: Int)
case class Record2(item: Any)
case class Record0(integers: List[List[Map[String, Int]]], nulls: List[List[Map[String, Any]]], nested: List[List[List[Map[String, Int]]]], reversed: List[List[Map[String, Int]]])
val my_data = Record0(
    integers = List[List[Map[String, Int]]](
        List(),
        List(
            Record1(
                item = 1,
            ),
        ),
    ),
    nulls = List[List[Map[String, Any]]](
        List(),
        List(
            Record2(
                item = null,
            ),
        ),
    ),
    nested = List[List[List[Map[String, Int]]]](
        List[List[Map[String, Int]]](
            List(),
            List(
                Record1(
                    item = 2,
                ),
            ),
        ),
        List[List[Map[String, Int]]](
            List(
                Record1(
                    item = 3,
                ),
            ),
            List(),
        ),
    ),
    reversed = List[List[Map[String, Int]]](
        List(
            Record1(
                item = 4,
            ),
        ),
        List(),
    ),
)
}
