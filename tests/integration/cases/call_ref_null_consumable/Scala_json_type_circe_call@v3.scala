import io.circe.Json
object Fixture_call_ref_null_consumable_Scala_json_type_circe_call {
def consume(value: Any = null): Any = null
val my_null: Json = Json.Null
val regular_null: Json = Json.Null
consume(value = my_null)
consume(value = regular_null)
}
