import io.circe.Json
object Fixture_dict_with_list_value_Scala_json_type_circe_combined {
var my_data: Json = Json.obj(
    "name" -> Json.fromString("Alice"),
    "scores" -> Json.arr(Json.fromInt(10), Json.fromInt(20), Json.fromInt(30)),
)
my_data = Json.obj(
    "name" -> Json.fromString("Alice"),
    "scores" -> Json.arr(Json.fromInt(10), Json.fromInt(20), Json.fromInt(30)),
)
}
