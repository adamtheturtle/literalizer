import java.time.ZoneId
import java.time.ZonedDateTime
object Declaration {
  val my_data = ZonedDateTime.of(2024, 1, 15, 12, 30, 45, 123456000, ZoneId.of("UTC"))
}
object Assignment {
  var my_data: Any = null
  my_data = ZonedDateTime.of(2024, 1, 15, 12, 30, 45, 123456000, ZoneId.of("UTC"))
}
