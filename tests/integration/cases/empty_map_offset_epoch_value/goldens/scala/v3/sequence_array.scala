import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_empty_map_offset_epoch_value_Scala_sequence_array {
val my_data = Array[Map[String, ZonedDateTime]](
    Map[String, ZonedDateTime]("timestamp" -> ZonedDateTime.of(2040, 1, 1, 3, 0, 0, 0, ZoneId.of("+03:00"))),
    Map[String, ZonedDateTime](),
)
}
