import java.time.LocalTime
object Fixture_heterogeneous_time_string_Scala_heterogeneous_strategy_record {
case class Record0(vals: List[Any])
val my_data = Record0(
    vals = List(
        LocalTime.of(9, 30),
        "hello",
    ),
)
}
