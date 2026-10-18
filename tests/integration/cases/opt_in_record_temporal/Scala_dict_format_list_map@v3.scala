import java.time.LocalTime
import java.time.LocalDate
import java.time.ZoneId
import java.time.ZonedDateTime
import scala.collection.immutable.ListMap
object Fixture_opt_in_record_temporal_Scala_dict_format_list_map {
val my_data = ListMap(
    "event_date" -> LocalDate.of(2024, 1, 15),
    "event_time" -> LocalTime.of(12, 30),
    "event_datetime" -> ZonedDateTime.of(2024, 1, 15, 12, 30, 0, 0, ZoneId.of("UTC")),
)
}
