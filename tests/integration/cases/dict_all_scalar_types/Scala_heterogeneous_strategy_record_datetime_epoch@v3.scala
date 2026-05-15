import java.time.LocalDate
object Fixture_dict_all_scalar_types_Scala_heterogeneous_strategy_record_datetime_epoch {
case class Record0(s: String, i: Int, f: Double, b: Boolean, n: Any, d: LocalDate, dt: Int, by: String)
val my_data = Record0(
    s = "string",
    i = 1,
    f = 1.5,
    b = true,
    n = null,
    d = LocalDate.of(2024, 1, 15),
    dt = 1705320000,
    by = "48656c6c6f",
)
}
