import java.time.ZoneId
import java.time.ZonedDateTime
import scala.collection.immutable.TreeSet
object Fixture_datetime_epoch_negative_set_Scala_set_tree_set {
val my_data = TreeSet[ZonedDateTime](
    ZonedDateTime.of(1969, 12, 31, 23, 59, 59, 0, ZoneId.of("Z")),
)
}
