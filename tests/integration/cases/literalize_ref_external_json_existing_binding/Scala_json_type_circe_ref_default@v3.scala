import io.circe.Json
object Fixture_literalize_ref_external_json_existing_binding_Scala_json_type_circe_ref_default {
def consume_widget(arg_value: Any = null): Any = null
var my_data: Json = Json.obj(
    "a" -> Json.fromInt(0),
)
consume_widget(arg_value = my_data)
my_data = Json.obj(
    "a" -> Json.fromInt(1),
)
consume_widget(arg_value = my_data)
}
