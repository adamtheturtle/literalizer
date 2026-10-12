import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_v_sibling_map_rendered_datetime_Scala {
val my_data = Map(
    "a" -> Map("k" -> ZonedDateTime.of(2020, 1, 1, 0, 0, 0, 0, ZoneId.of("Z"))),
    "b" -> Map("k" -> "string"),
)
}
