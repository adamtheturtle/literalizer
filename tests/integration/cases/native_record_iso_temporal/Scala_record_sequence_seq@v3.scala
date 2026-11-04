import java.time.LocalTime
import java.time.LocalDate
import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_native_record_iso_temporal_Scala_record_sequence_seq {
case class Record0(birthday: LocalDate, moment: ZonedDateTime, at: LocalTime)
val my_data = Record0(
    birthday = LocalDate.of(2024, 1, 15),
    moment = ZonedDateTime.of(2024, 1, 15, 12, 30, 0, 0, ZoneId.of("UTC")),
    at = LocalTime.of(9, 30),
)
}
