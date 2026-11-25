import io.circe.Json
object Fixture_ordered_map_proto_key_Scala_json_type_circe {
val my_data: Json = Json.obj(
    "__proto__" -> Json.obj("x" -> Json.fromInt(1)),
    "ordinary" -> Json.fromInt(2),
)
}
