import java.time.LocalDate
object Fixture_gregorian_reform_dates_Scala_datetime_iso {
val my_data = Map(
    "ancient_date" -> LocalDate.of(1500, 3, 1),
    "modern_date" -> LocalDate.of(2024, 1, 15),
    "before_date" -> LocalDate.of(1582, 10, 4),
    "gap_date" -> LocalDate.of(1582, 10, 10),
    "transition_date" -> LocalDate.of(1582, 10, 15),
    "after_date" -> LocalDate.of(1582, 10, 16),
    "before_naive" -> "1582-10-04T12:30:00.000001",
    "gap_naive" -> "1582-10-10T12:30:00.500000",
    "transition_positive" -> "1582-10-15T00:30:00+18:00",
    "transition_negative" -> "1582-10-15T23:30:00-18:00",
    "after_positive" -> "1582-10-16T00:30:00+18:00",
)
}
