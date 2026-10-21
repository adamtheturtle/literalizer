import io.circe.Json
object Fixture_string_unicode_Scala_json_type_circe {
val my_data: Json = Json.arr(
    Json.fromString("café"),
    Json.fromString("中文"),
    Json.fromString("😀"),
)
}
