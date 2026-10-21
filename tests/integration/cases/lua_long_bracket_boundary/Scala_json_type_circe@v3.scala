import io.circe.Json
object Fixture_lua_long_bracket_boundary_Scala_json_type_circe {
val my_data: Json = Json.arr(
    Json.fromString("]"),
    Json.fromString("a]"),
    Json.fromString("a]="),
    Json.fromString("a]b"),
)
}
