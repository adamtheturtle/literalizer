import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_sibling_maps_in_sequence_rendered_epoch_Scala_sequence_array {
val my_data = Array[Map[String, Any]](
    Map("k" -> ZonedDateTime.of(2040, 1, 1, 0, 0, 0, 0, ZoneId.of("Z"))),
    Map("k" -> 1),
)
}
