import java.time.LocalDate
import java.time.LocalDateTime
val my_data = mapOf<String, Any?>(
    "date" to LocalDate.of(99, 5, 27),
    "naive" to LocalDateTime.of(1, 1, 1, 12, 30, 0),
    "recent" to LocalDateTime.of(2024, 5, 27, 10, 0, 0),
)
