import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_sml_negative_epoch_Scala_sequence_array {
val my_data = Array[ZonedDateTime](
    ZonedDateTime.of(1960, 1, 1, 0, 0, 0, 0, ZoneId.of("Z")),
)
}
