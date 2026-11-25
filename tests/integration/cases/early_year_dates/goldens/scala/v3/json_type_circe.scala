import io.circe.Json
object Fixture_early_year_dates_Scala_json_type_circe {
val my_data: Json = Json.obj(
    "date" -> Json.fromString("0099-05-27"),
    "naive" -> Json.fromString("0001-01-01T12:30:00"),
    "recent" -> Json.fromString("2024-05-27T10:00:00"),
)
}
