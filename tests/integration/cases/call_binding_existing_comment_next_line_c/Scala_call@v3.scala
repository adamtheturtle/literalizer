object Fixture_call_binding_existing_comment_next_line_c_Scala_call {
def make_widget(count: Any = null): Any = null
var my_data = make_widget(count = 42)
make_widget(count = my_data)
my_data = make_widget(count = my_data)
// note
make_widget(count = my_data)
}
