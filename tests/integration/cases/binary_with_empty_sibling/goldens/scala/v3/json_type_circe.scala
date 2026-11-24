import io.circe.Json
object Fixture_binary_with_empty_sibling_Scala_json_type_circe {
val my_data: Json = Json.arr(
    Json.fromString("48656c6c6f"),
    Json.arr(),
)
}
