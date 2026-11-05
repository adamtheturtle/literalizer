import io.circe.Json
object Fixture_time_dict_Scala_json_type_circe {
val my_data: Json = Json.obj(
    "morning" -> Json.fromString("09:30:00"),
    "afternoon" -> Json.fromString("14:15:00"),
    "evening" -> Json.fromString("23:59:59"),
)
}
