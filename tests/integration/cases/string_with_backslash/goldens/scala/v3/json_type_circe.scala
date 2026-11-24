import io.circe.Json
object Fixture_string_with_backslash_Scala_json_type_circe {
val my_data: Json = Json.arr(
    Json.fromString("C:\\path\\to\\file"),
    Json.fromString("back\\\\slash"),
    Json.fromString("hello \\\"world\\\""),
    Json.fromString("path\\to \"# file"),
    Json.fromString("trailing\\"),
    Json.fromString("both \"quotes''' here"),
    Json.fromString("line1\\nline2\nwith newline"),
)
}
