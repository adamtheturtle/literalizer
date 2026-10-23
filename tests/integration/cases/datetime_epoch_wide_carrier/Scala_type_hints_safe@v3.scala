import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_datetime_epoch_wide_carrier_Scala_type_hints_safe {
val my_data = Map[String, ZonedDateTime](
    "within_i32" -> ZonedDateTime.of(2024, 1, 15, 12, 0, 0, 0, ZoneId.of("UTC")),
    "beyond_i32" -> ZonedDateTime.of(2099, 6, 15, 8, 30, 0, 0, ZoneId.of("UTC")),
)
}
