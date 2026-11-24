import io.circe.Json
object Fixture_call_json_repeated_null_Scala_json_type_circe_call {
def consume(value: Any = null): Any = null
val shared: Json = Json.Null
consume(value = Json.obj("left" -> shared, "nested" -> Json.arr(shared)))
}
