import java.time.LocalTime
import java.time.LocalDate
import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_native_record_temporal_Scala_record_sequence_array {
case class Record0(birthday: LocalDate, meeting: LocalTime, event_time: ZonedDateTime)
val my_data = Record0(
    birthday = LocalDate.of(2024, 1, 15),
    meeting = LocalTime.of(9, 30),
    event_time = ZonedDateTime.of(2024, 1, 15, 12, 30, 0, 0, ZoneId.of("UTC")),
)
}
