object Fixture_call_binding_existing_next_line_comment_seeded_Scala_call {
def make_widget(count: Any = null): Any = null
def consume_widget(count: Any = null): Any = null
var my_data = make_widget(count = 42)
consume_widget(count = my_data)
my_data = make_widget(count = my_data)
// note
consume_widget(count = my_data)
}
