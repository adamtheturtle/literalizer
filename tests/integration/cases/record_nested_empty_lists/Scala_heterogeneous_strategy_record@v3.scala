object Fixture_record_nested_empty_lists_Scala_heterogeneous_strategy_record {
case class Record0(a: List[List[Int]], b: List[List[Int]])
val my_data = Record0(
    a = List[List[Int]](
        List[Int](
            1,
            2,
        ),
        List[Int](
            3,
        ),
    ),
    b = List[List[Int]](
        List[Int](),
        List[Int](
            1,
        ),
    ),
)
}
