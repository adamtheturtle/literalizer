import io.circe.Json
object Fixture_call_json_nested_ref_object_Scala_json_type_circe_call {
def consume(value: Any = null): Any = null
val shared: Json = Json.arr(
    Json.fromInt(1),
    Json.fromInt(2),
)
consume(value = Json.obj("field" -> shared, "nested" -> Json.arr(shared, Json.obj())))
}
