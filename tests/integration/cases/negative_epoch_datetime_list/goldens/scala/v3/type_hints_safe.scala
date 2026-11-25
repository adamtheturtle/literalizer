import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_negative_epoch_datetime_list_Scala_type_hints_safe {
val my_data = List[ZonedDateTime](
    ZonedDateTime.of(1960, 1, 1, 0, 0, 0, 0, ZoneId.of("Z")),
)
}
