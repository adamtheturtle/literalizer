import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_v_empty_map_epoch_value_Scala {
val my_data = List[Map[String, ZonedDateTime]](
    Map[String, ZonedDateTime]("timestamp" -> ZonedDateTime.of(2020, 1, 1, 0, 0, 0, 0, ZoneId.of("Z"))),
    Map[String, ZonedDateTime](),
)
}
