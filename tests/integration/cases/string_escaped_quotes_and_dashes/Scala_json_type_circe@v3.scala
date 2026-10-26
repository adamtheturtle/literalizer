import io.circe.Json
object Fixture_string_escaped_quotes_and_dashes_Scala_json_type_circe {
val my_data: Json = Json.fromString("hello \"world\" -- not a comment")
}
