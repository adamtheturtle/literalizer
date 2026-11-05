import java.time.LocalTime
import scala.collection.immutable.ListMap
object Fixture_time_dict_Scala_dict_format_list_map {
val my_data = ListMap[String, LocalTime](
    "morning" -> LocalTime.of(9, 30),
    "afternoon" -> LocalTime.of(14, 15),
    "evening" -> LocalTime.of(23, 59, 59),
)
}
