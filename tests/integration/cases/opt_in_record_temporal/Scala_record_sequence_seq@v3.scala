import java.time.LocalTime
import java.time.LocalDate
import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_opt_in_record_temporal_Scala_record_sequence_seq {
case class Record0(event_date: LocalDate, event_time: LocalTime, event_datetime: ZonedDateTime)
val my_data = Record0(
    event_date = LocalDate.of(2024, 1, 15),
    event_time = LocalTime.of(12, 30),
    event_datetime = ZonedDateTime.of(2024, 1, 15, 12, 30, 0, 0, ZoneId.of("UTC")),
)
}
