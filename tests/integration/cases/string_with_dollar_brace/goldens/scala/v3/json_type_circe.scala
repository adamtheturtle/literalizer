import io.circe.Json
object Fixture_string_with_dollar_brace_Scala_json_type_circe {
val my_data: Json = Json.arr(
    Json.fromString("prefix ${HOME} suffix"),
    Json.fromString("${interpolated}"),
)
}
