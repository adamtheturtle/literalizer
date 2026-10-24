object Fixture_call_binding_existing_multiple_comments_Scala_type_hints_safe_call {
def make_widget(count: Any = null): Any = null
def consume_widget(count: Any = null): Any = null
var my_data = make_widget(count = 42)
consume_widget(count = my_data)
my_data = make_widget(count = 42) // note
// extra
consume_widget(count = my_data)
}
