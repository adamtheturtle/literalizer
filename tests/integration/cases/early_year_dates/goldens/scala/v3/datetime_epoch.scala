import java.time.LocalDate
object Fixture_early_year_dates_Scala_datetime_epoch {
val my_data = Map(
    "date" -> LocalDate.of(99, 5, 27),
    "naive" -> -62135551800L,
    "recent" -> 1716804000L,
)
}
