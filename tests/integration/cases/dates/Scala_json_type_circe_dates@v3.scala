import io.circe.Json
object Fixture_dates_Scala_json_type_circe_dates {
val my_data: Json = Json.obj(
    "date" -> Json.fromString("2024-01-15"),
    "datetime" -> Json.fromString("2024-01-15T12:30:00+00:00"),
)
}
