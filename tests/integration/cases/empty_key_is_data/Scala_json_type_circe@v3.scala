import io.circe.Json
object Fixture_empty_key_is_data_Scala_json_type_circe {
val my_data: Json = Json.arr(
    Json.obj("" -> Json.fromString("external_value")),
)
}
