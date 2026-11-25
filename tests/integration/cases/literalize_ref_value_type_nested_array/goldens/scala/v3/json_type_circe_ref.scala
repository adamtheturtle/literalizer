import io.circe.Json
object Fixture_literalize_ref_value_type_nested_array_Scala_json_type_circe_ref {
val shared: Json = Json.arr(
    Json.fromInt(1),
    Json.fromInt(2),
)
val my_data: Json = Json.arr(
    shared,
    Json.fromInt(42),
)
}
