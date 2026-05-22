import io.circe.Json
object Fixture_nested_mixed_inner_Scala_json_type_circe_nested_mixed {
val my_data: Json = Json.arr(
    Json.arr(Json.fromInt(1), Json.fromString("a")),
    Json.arr(Json.fromInt(2), Json.fromString("b")),
)
}
