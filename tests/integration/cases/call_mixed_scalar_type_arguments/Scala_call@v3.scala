import java.time.LocalDate
import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_call_mixed_scalar_type_arguments_Scala_call {
def capture(nan_value: Any = null, positive_infinity: Any = null, negative_infinity: Any = null, finite_value: Any = null, date_value: Any = null, datetime_value: Any = null, text_value: Any = null): Any = null
capture(nan_value = Double.NaN, positive_infinity = Double.PositiveInfinity, negative_infinity = Double.NegativeInfinity, finite_value = 1.25, date_value = LocalDate.of(2024, 1, 15), datetime_value = ZonedDateTime.of(2024, 1, 15, 12, 34, 56, 0, ZoneId.of("UTC")), text_value = "[ordinary text]")
}
