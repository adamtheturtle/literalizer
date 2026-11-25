import java.time.LocalTime
import scala.collection.immutable.ListMap
object Fixture_scalar_time_microsecond_Scala_dict_format_list_map {
val my_data = ListMap[String, LocalTime](
    "exact_millisecond" -> LocalTime.of(9, 30, 15, 123000000),
    "sub_millisecond" -> LocalTime.of(9, 30, 15, 123456000),
)
}
