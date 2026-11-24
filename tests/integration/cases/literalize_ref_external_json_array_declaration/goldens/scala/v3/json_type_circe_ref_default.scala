import io.circe.Json
object Fixture_literalize_ref_external_json_array_declaration_Scala_json_type_circe_ref_default {
def consume_widget(arg_value: Any = null): Any = null
val shared: Json = Json.arr(
    Json.fromInt(1),
    Json.fromInt(2),
)
val my_data: Json = shared
consume_widget(arg_value = my_data)
}
