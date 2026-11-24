import java.time.LocalDate
val my_data = mapOf<String, Any?>(
    "ancient_date" to LocalDate.of(1500, 3, 1),
    "modern_date" to LocalDate.of(2024, 1, 15),
    "before_date" to LocalDate.of(1582, 10, 4),
    "gap_date" to LocalDate.of(1582, 10, 10),
    "transition_date" to LocalDate.of(1582, 10, 15),
    "after_date" to LocalDate.of(1582, 10, 16),
    "before_naive" to "1582-10-04T12:30:00.000001",
    "gap_naive" to "1582-10-10T12:30:00.500000",
    "transition_positive" to "1582-10-15T00:30:00+18:00",
    "transition_negative" to "1582-10-15T23:30:00-18:00",
    "after_positive" to "1582-10-16T00:30:00+18:00",
)
