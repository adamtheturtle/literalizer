import io.circe.Json
object Fixture_call_csharp_json_repeated_scalar_Scala_json_type_circe_call {
def consume(value: Any = null): Any = null
val shared: Json = Json.fromInt(42)
consume(value = Json.arr(shared, shared))
}
