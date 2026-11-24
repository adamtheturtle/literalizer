import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_gregorian_reform_dates_Scala_date_iso {
val my_data = Map(
    "ancient_date" -> "1500-03-01",
    "modern_date" -> "2024-01-15",
    "before_date" -> "1582-10-04",
    "gap_date" -> "1582-10-10",
    "transition_date" -> "1582-10-15",
    "after_date" -> "1582-10-16",
    "before_naive" -> ZonedDateTime.of(1582, 10, 4, 12, 30, 0, 1000, ZoneId.of("UTC")),
    "gap_naive" -> ZonedDateTime.of(1582, 10, 10, 12, 30, 0, 500000000, ZoneId.of("UTC")),
    "transition_positive" -> ZonedDateTime.of(1582, 10, 15, 0, 30, 0, 0, ZoneId.of("+18:00")),
    "transition_negative" -> ZonedDateTime.of(1582, 10, 15, 23, 30, 0, 0, ZoneId.of("-18:00")),
    "after_positive" -> ZonedDateTime.of(1582, 10, 16, 0, 30, 0, 0, ZoneId.of("+18:00")),
)
}
