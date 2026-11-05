import java.time.LocalTime
import scala.collection.immutable.ListMap
object Fixture_time_list_Scala_dict_format_list_map {
val my_data = ListMap[String, List[LocalTime]](
    "times" -> List[LocalTime](LocalTime.of(9, 30), LocalTime.of(17, 45), LocalTime.of(23, 59, 59)),
)
}
