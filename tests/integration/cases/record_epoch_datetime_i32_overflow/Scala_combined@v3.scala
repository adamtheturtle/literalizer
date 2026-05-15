import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_record_epoch_datetime_i32_overflow_Scala_combined {
var my_data = Map[String, ZonedDateTime](
    "within_i32" -> ZonedDateTime.of(2024, 1, 15, 12, 0, 0, 0, ZoneId.of("UTC")),
    "beyond_i32" -> ZonedDateTime.of(2099, 6, 15, 8, 30, 0, 0, ZoneId.of("UTC")),
)
my_data = Map[String, ZonedDateTime](
    "within_i32" -> ZonedDateTime.of(2024, 1, 15, 12, 0, 0, 0, ZoneId.of("UTC")),
    "beyond_i32" -> ZonedDateTime.of(2099, 6, 15, 8, 30, 0, 0, ZoneId.of("UTC")),
)
}
