import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_sibling_maps_in_sequence_rendered_epoch_Scala_type_hints_safe {
val my_data = List[Map[String, Any]](
    Map("k" -> ZonedDateTime.of(2040, 1, 1, 0, 0, 0, 0, ZoneId.of("Z"))),
    Map("k" -> 1),
)
}
