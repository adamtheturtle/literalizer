import io.circe.Json
object Fixture_ordered_map_Scala_json_type_circe_ordered_map {
val my_data: Json = Json.obj(
    "name" -> Json.fromString("Alice"),
    "age" -> Json.fromInt(30),
    "active" -> Json.True,
)
}
