import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_datetime_negative_fractional_offset_Scala {
val my_data = ZonedDateTime.of(2000, 1, 1, 0, 0, 0, 0, ZoneId.of("-05:30"))
}
