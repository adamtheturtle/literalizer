import io.circe.Json
object Fixture_bidi_formatting_string_with_nul_Scala_json_type_circe {
val my_data: Json = Json.obj(
    "v" -> Json.fromString("a‪\u0000é😀b"),
)
}
