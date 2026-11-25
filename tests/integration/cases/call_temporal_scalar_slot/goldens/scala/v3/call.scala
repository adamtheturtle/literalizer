import java.time.LocalTime
import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_call_temporal_scalar_slot_Scala_call {
def process(value: Any = null): Any = null
process(value = LocalTime.of(9, 30))
process(value = ZonedDateTime.of(2024, 1, 15, 0, 0, 0, 0, ZoneId.of("UTC")))
process(value = 1)
}
