import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_scalar_datetime_non_utc_Scala {
val my_data = ZonedDateTime.of(2024, 1, 15, 18, 0, 0, 0, ZoneId.of("+05:30"))
}
