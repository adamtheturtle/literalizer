import io.circe.Json
object Fixture_literalize_ref_external_json_array_assignment_Scala_json_type_circe_ref_default {
def consume_widget(arg_value: Any = null): Any = null
val shared: Json = Json.arr(
    Json.fromInt(1),
    Json.fromInt(2),
)
var my_data: Json = Json.arr(
    Json.fromInt(0),
)
consume_widget(arg_value = my_data)
my_data = shared
consume_widget(arg_value = my_data)
}
