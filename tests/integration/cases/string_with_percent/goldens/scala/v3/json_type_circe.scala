import io.circe.Json
object Fixture_string_with_percent_Scala_json_type_circe {
val my_data: Json = Json.arr(
    Json.fromString("100% done"),
    Json.fromString("%(name) is here"),
)
}
