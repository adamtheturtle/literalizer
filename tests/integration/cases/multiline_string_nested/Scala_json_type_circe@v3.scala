import io.circe.Json
object Fixture_multiline_string_nested_Scala_json_type_circe {
val my_data: Json = Json.obj(
    "outer" -> Json.arr(Json.arr(Json.fromString("nested first line\n  indented\n\nnested last line\n"))),
)
}
