import io.circe.Json
object Fixture_call_nim_dotted_mixed_empty_arguments_Scala_json_type_circe_call {
class _ThingType { def go(before: Any = null, populated: Any = null, after: Any = null): Any = null }
val thing = new _ThingType
thing.go(before = Json.arr(), populated = Json.arr(Json.fromInt(1)), after = Json.arr())
thing.go(before = Json.arr(Json.fromString("text")), populated = Json.arr(Json.fromInt(2)), after = Json.arr())
thing.go(before = Json.arr(), populated = Json.arr(Json.fromString("text")), after = Json.arr())
thing.go(before = Json.arr(Json.fromString("text")), populated = Json.arr(Json.fromInt(2)), after = Json.arr(Json.fromInt(3)))
}
