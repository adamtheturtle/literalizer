import java.time.LocalTime
import java.time.LocalDate
import java.time.ZoneId
import java.time.ZonedDateTime
import scala.collection.immutable.ListMap
object Fixture_roc_native_record_temporal_Scala_dict_format_list_map {
val my_data = ListMap(
    "birthday" -> LocalDate.of(2024, 1, 15),
    "meeting" -> LocalTime.of(9, 30),
    "event_time" -> ZonedDateTime.of(2024, 1, 15, 12, 30, 0, 0, ZoneId.of("UTC")),
)
}
