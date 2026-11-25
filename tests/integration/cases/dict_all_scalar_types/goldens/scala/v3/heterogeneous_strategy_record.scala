import java.time.LocalDate
import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_dict_all_scalar_types_Scala_heterogeneous_strategy_record {
case class Record0(s: String, i: Int, f: Double, b: Boolean, n: Any, d: LocalDate, dt: ZonedDateTime, by: String)
val my_data = Record0(
    s = "string",
    i = 1,
    f = 1.5,
    b = true,
    n = null,
    d = LocalDate.of(2024, 1, 15),
    dt = ZonedDateTime.of(2024, 1, 15, 12, 0, 0, 0, ZoneId.of("UTC")),
    by = "48656c6c6f",
)
}
