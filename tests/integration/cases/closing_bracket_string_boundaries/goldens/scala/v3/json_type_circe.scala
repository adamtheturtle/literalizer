import io.circe.Json
object Fixture_closing_bracket_string_boundaries_Scala_json_type_circe {
val my_data: Json = Json.arr(
    Json.fromString("]"),
    Json.fromString("a]"),
    Json.fromString("a]="),
    Json.fromString("a]b"),
)
}
