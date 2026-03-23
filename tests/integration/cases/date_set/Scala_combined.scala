import java.time.LocalDate
object Declaration {
  val my_data = Set[LocalDate](
      LocalDate.of(2024, 1, 15),
      LocalDate.of(2024, 6, 1),
  )
}
object Assignment {
  var my_data: Any = null
  my_data = Set[LocalDate](
      LocalDate.of(2024, 1, 15),
      LocalDate.of(2024, 6, 1),
  )
}
