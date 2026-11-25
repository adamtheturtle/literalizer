import io.circe.Json
object Fixture_nested_positional_empty_list_cousins_Scala_json_type_circe {
val my_data: Json = Json.arr(
    Json.arr(Json.arr(), Json.arr()),
    Json.arr(Json.arr(Json.fromInt(1)), Json.arr(Json.fromInt(1))),
)
}
