import io.circe.Json
object Fixture_long_string_before_list_comma_Scala_json_type_circe {
val my_data: Json = Json.arr(
    Json.fromString("This long string keeps its structural comma beyond the Fortran wrapping window without a safe split."),
    Json.fromInt(1),
)
}
