import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_empty_map_nested_epoch_value_Scala_sequence_seq {
val my_data = Seq(
    Map("nested" -> Map[String, Seq[ZonedDateTime]]("times" -> Seq(ZonedDateTime.of(1900, 1, 1, 0, 0, 0, 0, ZoneId.of("Z"))))),
    Map(),
)
}
