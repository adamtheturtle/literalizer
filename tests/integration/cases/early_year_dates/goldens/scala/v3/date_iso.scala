import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_early_year_dates_Scala_date_iso {
val my_data = Map(
    "date" -> "0099-05-27",
    "naive" -> ZonedDateTime.of(1, 1, 1, 12, 30, 0, 0, ZoneId.of("UTC")),
    "recent" -> ZonedDateTime.of(2024, 5, 27, 10, 0, 0, 0, ZoneId.of("UTC")),
)
}
