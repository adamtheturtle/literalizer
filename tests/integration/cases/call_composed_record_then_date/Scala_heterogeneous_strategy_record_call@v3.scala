import java.time.LocalDate
object Fixture_call_composed_record_then_date_Scala_heterogeneous_strategy_record_call {
case class Record0(a: Int)
def consume(stamp: Any = null, value: Any = null): Any = null
val item = Record0(
    a = 1,
)
val stamp = LocalDate.of(2001, 2, 3)
consume(stamp = stamp, value = item)
}
