import io.circe.Json
object Fixture_escaped_mapping_keys_Scala_json_type_circe {
val my_data: Json = Json.obj(
    "quote\"backslash\\" -> Json.fromInt(1),
    "line\nbreak" -> Json.fromInt(2),
    "$(literal)${text}" -> Json.fromInt(3),
    "RStr prefix" -> Json.fromInt(4),
)
}
