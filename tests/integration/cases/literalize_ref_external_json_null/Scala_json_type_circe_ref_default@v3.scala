import io.circe.Json
object Fixture_literalize_ref_external_json_null_Scala_json_type_circe_ref_default {
def consume_widget(arg_value: Any = null): Any = null
val item: Json = Json.Null
var my_data: Json = Json.Null
consume_widget(arg_value = my_data)
my_data = item
consume_widget(arg_value = my_data)
}
