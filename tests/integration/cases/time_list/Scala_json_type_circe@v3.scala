import io.circe.Json
object Fixture_time_list_Scala_json_type_circe {
val my_data: Json = Json.obj(
    "times" -> Json.arr(Json.fromString("09:30:00"), Json.fromString("17:45:00"), Json.fromString("23:59:59")),
)
}
