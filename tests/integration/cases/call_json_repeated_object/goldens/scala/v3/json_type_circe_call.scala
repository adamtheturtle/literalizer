import io.circe.Json
object Fixture_call_json_repeated_object_Scala_json_type_circe_call {
def consume(value: Any = null): Any = null
val shared: Json = Json.obj(
    "value" -> Json.arr(Json.fromInt(1), Json.fromInt(2)),
)
consume(value = Json.obj("left" -> shared, "right" -> shared))
}
