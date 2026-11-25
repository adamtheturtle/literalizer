import io.circe.Json
object Fixture_dict_proto_key_Scala_json_type_circe {
val my_data: Json = Json.obj(
    "__proto__" -> Json.obj("x" -> Json.fromInt(1)),
    "n" -> Json.obj("__proto__" -> Json.fromInt(3)),
    "y" -> Json.fromInt(2),
)
}
