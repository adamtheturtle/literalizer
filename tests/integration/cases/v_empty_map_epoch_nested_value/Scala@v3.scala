import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_v_empty_map_epoch_nested_value_Scala {
val my_data = List[Map[String, Map[String, List[ZonedDateTime]]]](
    Map("nested" -> Map[String, List[ZonedDateTime]]("times" -> List[ZonedDateTime](ZonedDateTime.of(1900, 1, 1, 0, 0, 0, 0, ZoneId.of("Z"))))),
    Map(),
)
}
