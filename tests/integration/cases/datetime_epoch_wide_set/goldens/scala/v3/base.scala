import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_datetime_epoch_wide_set_Scala {
val my_data = Set[ZonedDateTime](
    ZonedDateTime.of(2099, 6, 15, 8, 30, 0, 0, ZoneId.of("UTC")),
)
}
