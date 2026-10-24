import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_datetime_extreme_offset_boundaries_Scala_sequence_seq {
val my_data = Seq(
    ZonedDateTime.of(2020, 6, 16, 11, 59, 0, 0, ZoneId.of("UTC")),
    ZonedDateTime.of(2020, 6, 15, 12, 0, 0, 0, ZoneId.of("-18:00")),
    ZonedDateTime.of(2020, 6, 15, 12, 0, 0, 0, ZoneId.of("+18:00")),
    ZonedDateTime.of(2020, 6, 14, 12, 1, 0, 0, ZoneId.of("UTC")),
)
}
