import java.time.LocalTime
object Fixture_time_list_Scala {
val my_data = Map[String, List[LocalTime]](
    "times" -> List[LocalTime](LocalTime.of(9, 30), LocalTime.of(17, 45), LocalTime.of(23, 59, 59)),
)
}
