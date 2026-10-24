import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_empty_map_epoch_value_Scala_sequence_array {
val my_data = Array[Map[String, ZonedDateTime]](
    Map[String, ZonedDateTime]("timestamp" -> ZonedDateTime.of(2020, 1, 1, 0, 0, 0, 0, ZoneId.of("Z"))),
    Map[String, ZonedDateTime](),
)
}
