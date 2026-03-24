import java.time.LocalDate
import java.time.ZoneId
import java.time.ZonedDateTime
object Check {
val my_data: Any = Map(
    "date" -> LocalDate.of(2024, 1, 15),
    "datetime" -> ZonedDateTime.of(2024, 1, 15, 12, 30, 0, 0, ZoneId.of("+00:00")),
)
}
