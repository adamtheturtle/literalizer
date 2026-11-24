import io.circe.Json
object Fixture_call_plain_mixed_empty_arguments_Scala_json_type_circe_call {
def make_widget(before: Any = null, populated: Any = null, after: Any = null): Any = null
make_widget(before = Json.arr(), populated = Json.arr(Json.fromInt(1)), after = Json.arr())
make_widget(before = Json.arr(Json.fromString("text")), populated = Json.arr(Json.fromInt(2)), after = Json.arr())
make_widget(before = Json.arr(), populated = Json.arr(Json.fromString("text")), after = Json.arr())
make_widget(before = Json.arr(Json.fromString("text")), populated = Json.arr(Json.fromInt(2)), after = Json.arr(Json.fromInt(3)))
}
