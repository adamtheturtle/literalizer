import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_sibling_map_rendered_epoch_reversed_Scala_type_hints_safe {
val my_data = Map(
    "b" -> Map("k" -> 1),
    "a" -> Map("k" -> ZonedDateTime.of(2040, 1, 1, 0, 0, 0, 0, ZoneId.of("Z"))),
)
}
