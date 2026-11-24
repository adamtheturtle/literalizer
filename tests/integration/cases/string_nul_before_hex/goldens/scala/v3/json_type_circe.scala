import io.circe.Json
object Fixture_string_nul_before_hex_Scala_json_type_circe {
val my_data: Json = Json.obj(
    "x" -> Json.fromString("before\u0000after"),
)
}
