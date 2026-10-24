import java.time.ZoneId
import java.time.ZonedDateTime
import scala.collection.immutable.ListMap
object Fixture_millisecond_datetime_Scala_dict_format_list_map {
val my_data = ListMap[String, ZonedDateTime](
    "half" -> ZonedDateTime.of(1979, 5, 27, 7, 32, 0, 500000000, ZoneId.of("UTC")),
    "milli" -> ZonedDateTime.of(1979, 5, 27, 7, 32, 0, 100000000, ZoneId.of("UTC")),
    "max_milli" -> ZonedDateTime.of(1979, 5, 27, 7, 32, 0, 999000000, ZoneId.of("UTC")),
    "whole" -> ZonedDateTime.of(1979, 5, 27, 7, 32, 0, 0, ZoneId.of("UTC")),
)
}
