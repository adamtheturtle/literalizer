import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_native_datetime_offsets_Scala {
val my_data = Map[String, List[ZonedDateTime]](
    "stamps" -> List[ZonedDateTime](ZonedDateTime.of(2001, 2, 3, 4, 5, 6, 0, ZoneId.of("UTC+00:00:01")), ZonedDateTime.of(2001, 2, 3, 4, 5, 6, 0, ZoneId.of("UTC-00:00:01")), ZonedDateTime.of(2001, 2, 3, 4, 5, 6, 0, ZoneId.of("UTC+00:00:00.000001")), ZonedDateTime.of(2001, 2, 3, 4, 5, 6, 0, ZoneId.of("UTC-00:00:00.000001")), ZonedDateTime.of(2001, 2, 3, 4, 5, 6, 0, ZoneId.of("UTC+05:30:15.000001")), ZonedDateTime.of(2001, 2, 3, 4, 5, 6, 0, ZoneId.of("UTC-05:30:15.000001"))),
)
}
