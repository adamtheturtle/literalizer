import io.circe.Json
object Fixture_dict_escaped_quote_key_Scala_json_type_circe {
val my_data: Json = Json.obj(
    "a\"b" -> Json.fromInt(1),
)
}
