import io.circe.Json
object Fixture_nested_empty_map_sibling_Scala_json_type_circe {
val my_data: Json = Json.arr(
    Json.obj("mapping" -> Json.obj()),
    Json.obj(),
)
}
