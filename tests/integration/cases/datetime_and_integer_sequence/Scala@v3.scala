import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_datetime_and_integer_sequence_Scala {
val my_data = List(
    ZonedDateTime.of(2000, 1, 1, 1, 2, 3, 0, ZoneId.of("UTC")),
    1,
)
}
