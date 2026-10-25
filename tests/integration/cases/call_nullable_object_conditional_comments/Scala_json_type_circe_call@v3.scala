import io.circe.Json
object Fixture_call_nullable_object_conditional_comments_Scala_json_type_circe_call {
def make_widget(count: Any = null): Any = null
val my_data = if (make_widget(count = Json.fromInt(42)) != null)
    make_widget(count = Json.fromInt(42)) // inner
else null // trailing
}
