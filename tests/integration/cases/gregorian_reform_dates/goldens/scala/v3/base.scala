import java.time.LocalDate
import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_gregorian_reform_dates_Scala {
val my_data = Map(
    "ancient_date" -> LocalDate.of(1500, 3, 1),
    "modern_date" -> LocalDate.of(2024, 1, 15),
    "before_date" -> LocalDate.of(1582, 10, 4),
    "gap_date" -> LocalDate.of(1582, 10, 10),
    "transition_date" -> LocalDate.of(1582, 10, 15),
    "after_date" -> LocalDate.of(1582, 10, 16),
    "before_naive" -> ZonedDateTime.of(1582, 10, 4, 12, 30, 0, 1000, ZoneId.of("UTC")),
    "gap_naive" -> ZonedDateTime.of(1582, 10, 10, 12, 30, 0, 500000000, ZoneId.of("UTC")),
    "transition_positive" -> ZonedDateTime.of(1582, 10, 15, 0, 30, 0, 0, ZoneId.of("+18:00")),
    "transition_negative" -> ZonedDateTime.of(1582, 10, 15, 23, 30, 0, 0, ZoneId.of("-18:00")),
    "after_positive" -> ZonedDateTime.of(1582, 10, 16, 0, 30, 0, 0, ZoneId.of("+18:00")),
)
}
