import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_fractional_epoch_boundaries_Scala {
val my_data = List[ZonedDateTime](
    ZonedDateTime.of(1970, 1, 1, 0, 0, 0, 1000, ZoneId.of("+00:00")),
    ZonedDateTime.of(1969, 12, 31, 23, 59, 59, 500000000, ZoneId.of("+00:00")),
    ZonedDateTime.of(1970, 1, 1, 0, 0, 1, 0, ZoneId.of("+00:00")),
)
}
