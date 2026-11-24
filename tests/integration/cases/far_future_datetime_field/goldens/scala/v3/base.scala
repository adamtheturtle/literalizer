import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_far_future_datetime_field_Scala {
val my_data = Map[String, ZonedDateTime](
    "ts" -> ZonedDateTime.of(3000, 12, 31, 23, 59, 59, 999999000, ZoneId.of("Z")),
)
}
