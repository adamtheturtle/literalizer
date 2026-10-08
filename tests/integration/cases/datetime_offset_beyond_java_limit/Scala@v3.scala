import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_datetime_offset_beyond_java_limit_Scala {
val my_data = ZonedDateTime.of(2020, 6, 15, 12, 0, 0, 0, ZoneId.of("+23:59"))
}
