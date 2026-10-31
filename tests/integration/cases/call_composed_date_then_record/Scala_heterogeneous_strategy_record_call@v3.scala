import java.time.LocalDate
object Fixture_call_composed_date_then_record_Scala_heterogeneous_strategy_record_call {
case class Record0(a: Int)
def consume(stamp: Any = null, value: Any = null): Any = null
val stamp = LocalDate.of(2001, 2, 3)
val item = Record0(
    a = 1,
)
consume(stamp = stamp, value = item)
}
