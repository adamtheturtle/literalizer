import java.time.LocalDate
object Declaration {
  val my_data = List[LocalDate](
      LocalDate.of(2024, 1, 15),
      LocalDate.of(2024, 2, 20),
  )
}
object Assignment {
  var my_data: Any = null
  my_data = List[LocalDate](
      LocalDate.of(2024, 1, 15),
      LocalDate.of(2024, 2, 20),
  )
}
