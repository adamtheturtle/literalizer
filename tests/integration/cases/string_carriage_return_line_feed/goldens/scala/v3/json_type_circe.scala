import io.circe.Json
object Fixture_string_carriage_return_line_feed_Scala_json_type_circe {
val my_data: Json = Json.obj(
    "cr" -> Json.fromString("a\rb"),
    "crlf" -> Json.fromString("a\r\nb"),
    "lf" -> Json.fromString("a\nb"),
)
}
