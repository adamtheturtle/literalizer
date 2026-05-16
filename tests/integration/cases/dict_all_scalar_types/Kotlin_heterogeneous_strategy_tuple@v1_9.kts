import java.time.LocalDate
import java.time.LocalDateTime
data class Record0(val s: String, val i: Int, val f: Double, val b: Boolean, val n: Any?, val d: LocalDate, val dt: LocalDateTime, val by: String)
val my_data = Record0(
    s = "string",
    i = 1,
    f = 1.5,
    b = true,
    n = null,
    d = LocalDate.of(2024, 1, 15),
    dt = LocalDateTime.of(2024, 1, 15, 12, 0, 0),
    by = "48656c6c6f",
)
