import io.circe.Json
object Fixture_dict_with_nulls_Scala_json_type_circe_nulls {
val my_data: Json = Json.obj(
    "name" -> Json.fromString("Alice"),
    "score" -> Json.Null,
    "age" -> Json.fromInt(30),
)
}
