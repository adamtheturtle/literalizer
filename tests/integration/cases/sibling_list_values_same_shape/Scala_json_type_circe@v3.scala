import io.circe.Json
object Fixture_sibling_list_values_same_shape_Scala_json_type_circe {
val my_data: Json = Json.obj(
    "test" -> Json.arr(Json.fromInt(5), Json.arr(Json.fromString("compile"), Json.fromString("test"))),
    "package" -> Json.arr(Json.fromInt(7), Json.arr(Json.fromString("link"), Json.fromString("test"))),
)
}
