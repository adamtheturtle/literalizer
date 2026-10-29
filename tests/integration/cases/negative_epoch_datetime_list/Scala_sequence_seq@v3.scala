import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_negative_epoch_datetime_list_Scala_sequence_seq {
val my_data = Seq(
    ZonedDateTime.of(1960, 1, 1, 0, 0, 0, 0, ZoneId.of("Z")),
)
}
