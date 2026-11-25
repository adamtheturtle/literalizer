import io.circe.Json
object Fixture_multiline_string_scalar_Scala_json_type_circe {
val my_data: Json = Json.fromString("\nroot first line\n  indented\n\nroot last line\n")
}
