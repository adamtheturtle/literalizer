import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_datetime_epoch_negative_set_Scala_type_hints_safe {
val my_data = Set[ZonedDateTime](
    ZonedDateTime.of(1969, 12, 31, 23, 59, 59, 0, ZoneId.of("Z")),
)
}
