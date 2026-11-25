import java.time.LocalTime
object Fixture_time_dict_Scala {
val my_data = Map[String, LocalTime](
    "morning" -> LocalTime.of(9, 30),
    "afternoon" -> LocalTime.of(14, 15),
    "evening" -> LocalTime.of(23, 59, 59),
)
}
