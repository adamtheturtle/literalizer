import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_empty_map_nested_epoch_value_Scala_sequence_array {
val my_data = Array[Map[String, Any]](
    Map("nested" -> Map[String, Array[ZonedDateTime]]("times" -> Array[ZonedDateTime](ZonedDateTime.of(1900, 1, 1, 0, 0, 0, 0, ZoneId.of("Z"))))),
    Map(),
)
}
