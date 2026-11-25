import io.circe.Json
object Fixture_ragged_map_sequence_values_Scala_json_type_circe {
val my_data: Json = Json.obj(
    "a" -> Json.arr(Json.obj("item" -> Json.arr(Json.fromInt(1)))),
    "b" -> Json.arr(Json.obj("item" -> Json.arr(Json.fromInt(2), Json.fromInt(3)))),
)
}
