import io.circe.Json
object Fixture_multiline_string_nested_list_Scala_json_type_circe {
val my_data: Json = Json.arr(
    Json.arr(Json.fromString("\nfirst line\n  indented\n\nlast line\n")),
)
}
