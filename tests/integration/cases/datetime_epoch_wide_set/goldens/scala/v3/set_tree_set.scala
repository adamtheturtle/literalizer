import java.time.ZoneId
import java.time.ZonedDateTime
import scala.collection.immutable.TreeSet
object Fixture_datetime_epoch_wide_set_Scala_set_tree_set {
val my_data = TreeSet[ZonedDateTime](
    ZonedDateTime.of(2099, 6, 15, 8, 30, 0, 0, ZoneId.of("UTC")),
)
}
