import io.circe.Json
object Fixture_call_scalar_args_Scala_json_type_circe_call {
def process(value: Any = null): Any = null
process(value = Json.fromString("hello"))
process(value = Json.fromInt(42))
process(value = Json.True)
}
