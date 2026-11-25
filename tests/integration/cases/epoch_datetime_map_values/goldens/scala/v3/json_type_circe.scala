import io.circe.Json
object Fixture_epoch_datetime_map_values_Scala_json_type_circe {
val my_data: Json = Json.obj(
    "within_i32" -> Json.fromString("2024-01-15T12:00:00"),
    "beyond_i32" -> Json.fromString("2099-06-15T08:30:00"),
)
}
