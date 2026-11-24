import io.circe.Json
object Fixture_utf8_string_sibling_lines_Scala_json_type_circe {
val my_data: Json = Json.arr(
    Json.fromString("中中中中中中中中中中中中中中中中中中中中"),
    Json.fromString("é'é'é'é'é'é'é'é'é'é'"),
    Json.fromString("🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂"),
)
}
