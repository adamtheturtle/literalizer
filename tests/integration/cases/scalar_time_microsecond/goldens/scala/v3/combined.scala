import java.time.LocalTime
object Fixture_scalar_time_microsecond_Scala_combined {
var my_data = Map[String, LocalTime](
    "exact_millisecond" -> LocalTime.of(9, 30, 15, 123000000),
    "sub_millisecond" -> LocalTime.of(9, 30, 15, 123456000),
)
my_data = Map[String, LocalTime](
    "exact_millisecond" -> LocalTime.of(9, 30, 15, 123000000),
    "sub_millisecond" -> LocalTime.of(9, 30, 15, 123456000),
)
}
