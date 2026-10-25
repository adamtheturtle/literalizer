import io.circe.Json
object Fixture_call_dotted_empty_result_binding_Scala_json_type_circe_call {
class _ThingType { def go(value: Any = null): Any = null }
val thing = new _ThingType
val my_data = thing.go(value = Json.arr())
}
