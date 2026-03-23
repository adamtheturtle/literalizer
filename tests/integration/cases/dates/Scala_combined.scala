import java.time.LocalDate
import java.time.LocalDateTime
object Declaration {
  val my_data = Map(
      "date" -> LocalDate.of(2024, 1, 15),
      "datetime" -> LocalDateTime.of(2024, 1, 15, 12, 30, 0),
  )
}
object Assignment {
  var my_data: Any = null
  my_data = Map(
      "date" -> LocalDate.of(2024, 1, 15),
      "datetime" -> LocalDateTime.of(2024, 1, 15, 12, 30, 0),
  )
}
