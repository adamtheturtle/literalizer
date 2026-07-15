import io.circe.Json
object Fixture_json_string_escaping_Scala_json_type_circe_string_escaping {
val my_data: Json = Json.fromString("a\"b\tcé")
}
