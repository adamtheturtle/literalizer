import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_datetime_list_Scala_sequence_seq {
val my_data = Seq(
    ZonedDateTime.of(2024, 1, 15, 12, 30, 0, 123456000, ZoneId.of("+00:00")),
    ZonedDateTime.of(2024, 6, 1, 8, 0, 0, 0, ZoneId.of("+00:00")),
)
}
