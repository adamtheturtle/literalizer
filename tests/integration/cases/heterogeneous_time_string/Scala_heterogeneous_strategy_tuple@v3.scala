import java.time.LocalTime
object Fixture_heterogeneous_time_string_Scala_heterogeneous_strategy_tuple {
case class Record0(vals: (LocalTime, String))
val my_data = Record0(
    vals = (
        LocalTime.of(9, 30),
        "hello",
    ),
)
}
