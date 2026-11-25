object Fixture_record_two_shapes_Scala_heterogeneous_strategy_tuple {
case class Record1(count: Int, rate: Int)
case class Record2(retries: Int, timeout: Int)
case class Record0(metrics: Record1, flags: Record2)
val my_data = Record0(
    metrics = Record1(
        count = 100,
        rate = 50,
    ),
    flags = Record2(
        retries = 3,
        timeout = 30,
    ),
)
}
