import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_v_empty_map_epoch_offset_value_Scala {
val my_data = List[Map[String, ZonedDateTime]](
    Map[String, ZonedDateTime]("timestamp" -> ZonedDateTime.of(2040, 1, 1, 3, 0, 0, 0, ZoneId.of("+03:00"))),
    Map[String, ZonedDateTime](),
)
}
