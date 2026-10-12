import io.circe.Json
object Fixture_call_zig_json_nested_ref_array_Scala_json_type_circe_call {
def consume(value: Any = null): Any = null
val shared: Json = Json.arr(
    Json.fromInt(1),
    Json.fromInt(2),
)
consume(value = Json.arr(shared, Json.fromInt(42)))
}
